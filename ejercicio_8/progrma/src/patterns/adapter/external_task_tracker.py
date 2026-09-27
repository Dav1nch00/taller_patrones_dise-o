from abc import ABC, abstractmethod


class ExternalTaskTracker(ABC):
    """Interfaz uniforme para una herramienta externa de seguimiento.

    No es un canal de notificacion sino un destino de datos: recibe la entidad de
    negocio completa y la publica donde el equipo trabaja. Por eso tiene su propia
    interfaz y no encaja en ExternalGateway.
    """

    @abstractmethod
    def publish_task(self, task) -> dict:
        pass
