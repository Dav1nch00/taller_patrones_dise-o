from __future__ import annotations

from typing import TYPE_CHECKING

from domain.domain_event import TIPO_ESTADO_CAMBIADO
from domain.team_member import TeamMember
from patterns.state.task_state import TaskNotMutableError
from patterns.state.to_do_state import ToDoState
from patterns.state.workflow import Workflow

if TYPE_CHECKING:
    from domain.project import Project
    from patterns.state.task_state import TaskState


class Task:
    """Entidad que delega su comportamiento en el TaskState actual.

    No contiene ningun condicional sobre el estado: cada accion se resuelve en
    la subclase de TaskState, y la tabla del Workflow decide si la transicion
    esta permitida. Los hechos se publican en el Project, que es el sujeto
    unico del Observer.
    """

    def __init__(
        self,
        id,
        titulo,
        descripcion="",
        prioridad=3,
        responsable=None,
        fecha_limite="",
        etiquetas=None,
        dependencias=None,
        proyecto=None,
        workflow=None,
    ):
        self._id = id
        self._titulo = titulo
        self._descripcion = descripcion
        self._prioridad = int(prioridad)
        self._responsable = responsable
        self._fecha_limite = fecha_limite
        self._etiquetas = list(etiquetas or [])
        self._dependencias = list(dependencias or [])
        self._proyecto = proyecto
        self._workflow = workflow or self._workflow_del_proyecto()
        self._state = ToDoState()
        self._motivo_bloqueo = ""

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def prioridad(self):
        return self._prioridad

    @property
    def responsable(self):
        return self._responsable

    @property
    def fecha_limite(self):
        return self._fecha_limite

    @property
    def etiquetas(self):
        return list(self._etiquetas)

    @property
    def dependencias(self):
        return list(self._dependencias)

    @property
    def estado(self):
        return self._state.name

    @property
    def motivo_bloqueo(self):
        return self._motivo_bloqueo

    @property
    def workflow(self):
        return self._workflow

    @property
    def proyecto(self):
        return self._proyecto

    def set_proyecto(self, proyecto):
        self._proyecto = proyecto

    def set_workflow(self, workflow):
        self._workflow = workflow

    def esta_en(self, nombre_estado):
        return self._state.name == nombre_estado

    def change_state(self, nuevo_estado, accion, detalle=""):
        estado_actual = self._state.name
        esperado = self._workflow.destino(estado_actual, accion)
        if esperado != nuevo_estado.name:
            raise self._workflow.error_de_configuracion(
                estado_actual, accion, esperado, nuevo_estado.name
            )
        self._state = nuevo_estado
        if nuevo_estado.name == "Blocked":
            self._motivo_bloqueo = detalle
        elif nuevo_estado.name == "InProgress":
            self._motivo_bloqueo = ""
        self._publicar(
            TIPO_ESTADO_CAMBIADO,
            f"Tarea {self._id} '{self._titulo}': {estado_actual} -> {nuevo_estado.name}"
            + (f" | {detalle}" if detalle else ""),
        )

    def start(self):
        self._state.start(self)

    def submit_for_review(self):
        self._state.submit_for_review(self)

    def approve(self):
        self._state.approve(self)

    def reject(self):
        self._state.reject(self)

    def block(self, motivo=""):
        self._state.block(self, motivo)

    def unblock(self):
        self._state.unblock(self)

    def editar(
        self,
        titulo=None,
        prioridad=None,
        responsable=None,
        fecha_limite=None,
        etiquetas=None,
    ):
        if not self._state.is_mutable():
            raise TaskNotMutableError(
                f"La tarea completada {self._id} '{self._titulo}' no puede modificarse."
            )
        if titulo is not None:
            self._titulo = titulo
        if prioridad is not None:
            self._prioridad = int(prioridad)
        if responsable is not None:
            if not isinstance(responsable, TeamMember):
                raise TypeError("El responsable debe ser un TeamMember.")
            self._responsable = responsable
        if fecha_limite is not None:
            self._fecha_limite = fecha_limite
        if etiquetas is not None:
            self._etiquetas = list(etiquetas)
        return self

    def asignar(self, responsable):
        if not isinstance(responsable, TeamMember):
            raise TypeError("El responsable debe ser un TeamMember.")
        if not self._state.is_mutable():
            raise TaskNotMutableError(
                f"La tarea completada {self._id} '{self._titulo}' no puede reasignarse."
            )
        self._responsable = responsable
        return (
            f"Tarea {self._id} '{self._titulo}' asignada a "
            f"{responsable.nombre} ({responsable.rol})."
        )

    def _publicar(self, tipo, mensaje):
        if self._proyecto is not None:
            self._proyecto.publicar(tipo, mensaje, self)

    def _workflow_del_proyecto(self):
        if self._proyecto is not None:
            return self._proyecto.workflow
        return Workflow("estandar")

    def __str__(self):
        quien = self._responsable.nombre if self._responsable else "sin asignar"
        return (
            f"Task(id={self._id}, titulo={self._titulo}, state={self._state.name}, "
            f"prioridad={self._prioridad}, responsable={quien})"
        )
