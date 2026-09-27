from patterns.strategy.report_strategy import ReportStrategy


class DetailedTasksReport(ReportStrategy):
    nombre = "Detalle de tareas"

    def generate(self, project) -> str:
        lineas = [
            "REPORTE: DETALLE DE TAREAS",
            "=" * 46,
            f"Proyecto: {project.nombre} ({project.id})",
            "",
        ]
        if not project.tareas:
            lineas.append("(el proyecto no tiene tareas)")
            return "\n".join(lineas)
        for tarea in sorted(project.tareas, key=lambda t: (t.prioridad, t.id)):
            quien = tarea.responsable.nombre if tarea.responsable else "sin asignar"
            lineas.append(f"[{tarea.estado}] {tarea.id}  P{tarea.prioridad}  {tarea.titulo}")
            lineas.append(f"    responsable : {quien}")
            lineas.append(f"    limite      : {tarea.fecha_limite or '-'}")
            lineas.append(f"    etiquetas   : {','.join(tarea.etiquetas) or '-'}")
            lineas.append(f"    depende de  : {','.join(tarea.dependencias) or '-'}")
            if tarea.motivo_bloqueo:
                lineas.append(f"    motivo      : {tarea.motivo_bloqueo}")
            lineas.append("")
        return "\n".join(lineas)
