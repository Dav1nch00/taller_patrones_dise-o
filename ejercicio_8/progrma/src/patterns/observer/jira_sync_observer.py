from domain.domain_event import TIPO_ESTADO_CAMBIADO, TIPO_TAREA_CREADA
from domain.task import Task
from patterns.adapter.external_task_tracker import ExternalTaskTracker
from patterns.observer.event_observer import EventObserver


class JiraSyncObserver(EventObserver):
    """Mantiene sincronizada la herramienta externa de seguimiento.

    No es un canal de notificacion: consume la entidad real (event.origen) para
    publicarla. Solo reacciona a los tipos de evento que tienen sentido como issue
    y descarta el resto de forma explicita. Si crea o actualiza el issue lo
    decide el adaptador, no este observador.
    """

    canal = "jira"

    TIPOS_SINCRONIZABLES = (TIPO_TAREA_CREADA, TIPO_ESTADO_CAMBIADO)

    def __init__(self, tracker):
        if not isinstance(tracker, ExternalTaskTracker):
            raise TypeError("JiraSyncObserver requiere un ExternalTaskTracker.")
        self._tracker = tracker

    def update(self, event) -> dict:
        if event.tipo not in self.TIPOS_SINCRONIZABLES:
            return {"transport": self.canal, "omitido": f"tipo '{event.tipo}' no se sincroniza"}
        if not isinstance(event.origen, Task):
            return {"transport": self.canal, "omitido": "el evento no proviene de una tarea"}
        respuesta = self._tracker.publish_task(event.origen)
        print(
            f"  [JIRA]   -> {respuesta['clave']} ({respuesta['accion']}) <- {event.tipo} | "
            f"{event.origen.id} {event.origen.titulo} | {event.origen.estado}"
        )
        return respuesta
