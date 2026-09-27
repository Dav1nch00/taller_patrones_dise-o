from datetime import date

from patterns.strategy.report_strategy import ReportStrategy


class DeadlineRiskReport(ReportStrategy):
    nombre = "Riesgo por fecha limite"

    DIAS_AVISO = 7

    def generate(self, project) -> str:
        hoy = date.today()
        lineas = [
            "REPORTE: RIESGO POR FECHA LIMITE",
            "=" * 46,
            f"Proyecto: {project.nombre} ({project.id})",
            f"Corte   : {hoy.isoformat()}  (aviso: {self.DIAS_AVISO} dias)",
            "",
        ]
        vencidas, en_riesgo, con_margen, sin_fecha = [], [], [], []
        for tarea in project.tareas:
            if tarea.esta_en("Done"):
                continue
            limite = self._a_fecha(tarea.fecha_limite)
            if limite is None:
                sin_fecha.append(tarea)
                continue
            dias = (limite - hoy).days
            if dias < 0:
                vencidas.append((tarea, dias))
            elif dias <= self.DIAS_AVISO:
                en_riesgo.append((tarea, dias))
            else:
                con_margen.append((tarea, dias))
        self._seccion(lineas, "VENCIDAS", vencidas, "Vencio hace {dias} dias")
        self._seccion(lineas, "EN RIESGO", en_riesgo, "Vence en {dias} dias")
        self._seccion(lineas, "CON MARGEN", con_margen, "Vence en {dias} dias")
        if sin_fecha:
            lineas += ["SIN FECHA LIMITE (requieren priorizacion):"]
            for tarea in sin_fecha:
                lineas.append(f"  [{tarea.estado}] P{tarea.prioridad} {tarea.id} {tarea.titulo}")
        return "\n".join(lineas)

    def _seccion(self, lineas, titulo, elementos, plantilla):
        if not elementos:
            return
        lineas += [f"{titulo}:"]
        for tarea, dias in sorted(elementos, key=lambda par: par[1]):
            quien = tarea.responsable.nombre if tarea.responsable else "sin asignar"
            lineas.append(
                f"  {tarea.id} [{tarea.estado}] {tarea.titulo} "
                f"-> {plantilla.format(dias=abs(dias))} | {quien}"
            )
        lineas.append("")

    def _a_fecha(self, texto):
        if not texto:
            return None
        try:
            return date.fromisoformat(texto)
        except ValueError:
            return None
