from patterns.strategy.report_strategy import ReportStrategy


class WorkloadReport(ReportStrategy):
    nombre = "Carga de trabajo"

    def generate(self, project) -> str:
        lineas = [
            "REPORTE: CARGA DE TRABAJO POR RESPONSABLE",
            "=" * 46,
            f"Proyecto: {project.nombre} ({project.id})",
            "",
        ]
        if not project.tareas:
            lineas.append("(el proyecto no tiene tareas)")
            return "\n".join(lineas)
        grupos = {}
        for tarea in project.tareas:
            clave = tarea.responsable.nombre if tarea.responsable else "SIN ASIGNAR"
            grupos.setdefault(clave, []).append(tarea)
        for nombre in sorted(grupos):
            tareas = grupos[nombre]
            por_estado = {}
            for tarea in tareas:
                por_estado[tarea.estado] = por_estado.get(tarea.estado, 0) + 1
            carga_prioritaria = sum(1 for t in tareas if t.prioridad <= 2)
            detalle = ", ".join(f"{estado}={n}" for estado, n in por_estado.items())
            lineas.append(f"{nombre}: {len(tareas)} tarea(s), {carga_prioritaria} de alta prioridad [{detalle}]")
            for tarea in sorted(tareas, key=lambda t: t.prioridad):
                linea = f"    {tarea.id} P{tarea.prioridad} [{tarea.estado}] {tarea.titulo}"
                if tarea.esta_en("Blocked"):
                    linea += f"  ({tarea.motivo_bloqueo or 'sin motivo'})"
                lineas.append(linea)
            lineas.append("")
        return "\n".join(lineas)
