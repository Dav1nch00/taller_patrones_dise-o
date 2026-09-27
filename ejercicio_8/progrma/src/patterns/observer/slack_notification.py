from domain.domain_event import (
    TIPO_ESTADO_CAMBIADO,
    TIPO_FLUJO_RECONFIGURADO,
    TIPO_TAREA_ASIGNADA,
    TIPO_TAREA_CREADA,
)
from patterns.adapter.external_gateway import ExternalGateway
from patterns.observer.event_observer import EventObserver


class SlackNotification(EventObserver):
    """Notifica por Slack usando un ExternalGateway.

    Si el evento trae una tarea con responsable, menciona su usuario de Slack en
    el canal por defecto; si no, publica en el canal destino. La decision de
    canal y el formato del texto los toma SlackAdapter, no esta clase.
    """

    canal = "slack"

    TITULOS = {
        TIPO_TAREA_CREADA: "Nueva tarea",
        TIPO_TAREA_ASIGNADA: "Tarea asignada",
        TIPO_ESTADO_CAMBIADO: "Cambio de estado",
        TIPO_FLUJO_RECONFIGURADO: "Flujo reconfigurado",
    }

    def __init__(self, gateway, canal_por_defecto=None):
        if not isinstance(gateway, ExternalGateway):
            raise TypeError("SlackNotification requiere un ExternalGateway.")
        self._gateway = gateway
        self._canal_por_defecto = canal_por_defecto or getattr(
            gateway, "canal_por_defecto", "#proyectos"
        )

    def update(self, event) -> dict:
        destinatario = self._destinatario(event)
        respuesta = self._gateway.send(destinatario, self._asunto(event), self._cuerpo(event))
        print(
            f"  [SLACK]  -> {respuesta['destinatario_resuelto']} | "
            f"{event.mensaje} | ts={respuesta['referencia']}"
        )
        return respuesta

    def _destinatario(self, event):
        responsable = getattr(event.origen, "responsable", None)
        if responsable is not None:
            return responsable.slack_user
        return self._canal_por_defecto

    def _asunto(self, event):
        return f"{self.TITULOS.get(event.tipo, event.tipo)}: {event.proyecto.nombre}"

    def _cuerpo(self, event):
        origen = event.origen
        quien = getattr(origen, "responsable", None)
        lineas = [f"Proyecto: {event.proyecto.nombre} ({event.proyecto.id})"]
        if quien is not None:
            lineas.append(f"Responsable: {quien.nombre} ({quien.rol})")
        lineas.append(f"Detalle: {event.mensaje}")
        return "\n".join(lineas)
