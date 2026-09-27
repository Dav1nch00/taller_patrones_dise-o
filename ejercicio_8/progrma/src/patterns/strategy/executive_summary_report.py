from patterns.state.workflow import ESTADOS_CONOCIDOS
from patterns.strategy.report_strategy import ReportStrategy


class ExecutiveSummaryReport(ReportStrategy):
    nombre = "Resumen ejecutivo"

    def generate(self, project) -> str:
        conteo = project.tareas_por_estado()
        total = len(project.tareas)
        lineas = [
            "REPORTE: RESUMEN EJECUTIVO",
            "=" * 46,
            f"Proyecto : {project.nombre} ({project.id})",
            f"Tipo     : {project.tipo}",
            f"Flujo    : {project.workflow.nombre}",
            f"Tareas   : {total}",
            f"Progreso : {project.progreso()}%",
            "",
            "Distribucion por estado:",
        ]
        for estado in ESTADOS_CONOCIDOS:
            cantidad = conteo[estado]
            lineas.append(f"  {estado:<12}{cantidad:>3}  {'#' * cantidad}")
        lineas += [
            "",
            f"Pendientes de completar : {total - conteo['Done']}",
            f"En revision             : {conteo['InReview']}",
            f"Bloqueadas              : {conteo['Blocked']}",
        ]
        bloqueadas = [t for t in project.tareas if t.esta_en("Blocked")]
        if bloqueadas:
            lineas += ["", "Detalle de bloqueos:"]
            for tarea in bloqueadas:
                lineas.append(f"  {tarea.id} {tarea.titulo}: {tarea.motivo_bloqueo or 'sin motivo'}")
        return "\n".join(lineas)
