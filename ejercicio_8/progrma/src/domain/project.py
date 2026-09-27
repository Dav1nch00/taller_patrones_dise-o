from __future__ import annotations

from typing import TYPE_CHECKING

from domain.domain_event import (
    TIPO_FLUJO_RECONFIGURADO,
    TIPO_TAREA_ASIGNADA,
    TIPO_TAREA_CREADA,
    DomainEvent,
)
from domain.task import Task
from patterns.state.workflow import ESTADOS_CONOCIDOS, Workflow

if TYPE_CHECKING:
    from patterns.observer.event_observer import EventObserver
    from patterns.strategy.report_strategy import ReportStrategy


class Project:
    """Sujeto unico del Observer y contenedor de las tareas del proyecto.

    El proyecto impone su Workflow a cada tarea que incorpora, de modo que la
    tabla de transiciones vive en un solo lugar y se puede reconfigurar en
    caliente para todas las tareas a la vez.
    """

    def __init__(self, id, nombre, tipo, descripcion="", workflow=None, report_strategy=None):
        self._id = id
        self._nombre = nombre
        self._tipo = tipo
        self._descripcion = descripcion
        self._workflow = workflow or Workflow("estandar")
        self._report_strategy = report_strategy
        self._tareas = []
        self._observers = []

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def workflow(self):
        return self._workflow

    @property
    def report_strategy(self):
        return self._report_strategy

    @property
    def tareas(self):
        return list(self._tareas)

    @property
    def observers(self):
        return list(self._observers)

    def add_task(self, tarea):
        if not isinstance(tarea, Task):
            raise TypeError("El proyecto solo admite tareas del dominio.")
        if any(t.id == tarea.id for t in self._tareas):
            raise ValueError(f"El proyecto ya tiene una tarea con id {tarea.id}.")
        tarea.set_proyecto(self)
        tarea.set_workflow(self._workflow)
        self._tareas.append(tarea)
        self.publicar(
            TIPO_TAREA_CREADA,
            f"Proyecto {self._nombre}: creada la tarea {tarea.id} '{tarea.titulo}'.",
            tarea,
        )
        return tarea

    def asignar_tarea(self, tarea, responsable):
        self._exigir_tarea(tarea)
        mensaje = tarea.asignar(responsable)
        self.publicar(TIPO_TAREA_ASIGNADA, f"{mensaje} Proyecto: {self._nombre}.", tarea)
        return mensaje

    def configurar_flujo(self, workflow):
        self._workflow = workflow
        for tarea in self._tareas:
            tarea.set_workflow(workflow)
        self.publicar(
            TIPO_FLUJO_RECONFIGURADO,
            f"Proyecto {self._nombre}: flujo cambiado a '{workflow.nombre}' "
            f"para {len(self._tareas)} tarea(s).",
        )

    def set_report_strategy(self, report_strategy):
        self._report_strategy = report_strategy

    def generate_report(self):
        if self._report_strategy is None:
            raise RuntimeError(
                f"El proyecto {self._nombre} no tiene estrategia de reporte asignada."
            )
        return self._report_strategy.generate(self)

    def tareas_por_estado(self):
        conteo = {estado: 0 for estado in ESTADOS_CONOCIDOS}
        for tarea in self._tareas:
            conteo[tarea.estado] = conteo.get(tarea.estado, 0) + 1
        return conteo

    def progreso(self):
        if not self._tareas:
            return 0.0
        completadas = sum(1 for t in self._tareas if t.esta_en("Done"))
        return round(100.0 * completadas / len(self._tareas), 1)

    def buscar_tarea(self, tarea_id):
        for tarea in self._tareas:
            if tarea.id == tarea_id:
                return tarea
        return None

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def publicar(self, tipo, mensaje, origen=None):
        evento = DomainEvent(tipo, mensaje, origen or self, self)
        for observer in list(self._observers):
            observer.update(evento)
        return evento

    def _exigir_tarea(self, tarea):
        if tarea not in self._tareas:
            raise ValueError(f"La tarea {tarea.id} no pertenece al proyecto {self._nombre}.")

    def __str__(self):
        conteo = self.tareas_por_estado()
        detalle = ", ".join(f"{estado}={conteo[estado]}" for estado in ESTADOS_CONOCIDOS)
        return (
            f"Project(id={self._id}, nombre={self._nombre}, tipo={self._tipo}, "
            f"flujo={self._workflow.nombre}, tareas={len(self._tareas)} [{detalle}])"
        )
