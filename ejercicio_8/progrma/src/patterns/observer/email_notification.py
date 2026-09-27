from domain.domain_event import (
    TIPO_ESTADO_CAMBIADO,
    TIPO_FLUJO_RECONFIGURADO,
    TIPO_TAREA_ASIGNADA,
    TIPO_TAREA_CREADA,
)
from patterns.adapter.external_gateway import ExternalGateway
from patterns.observer.event_observer import EventObserver


class EmailNotification(EventObserver):
    """Notifica por correo usando un ExternalGateway.

    No conoce ExternalSmtpEmailAPI: si el canal de correo se cambia por otro
    proveedor, se cambia el adaptador inyectado y esta clase no se toca.
    """

    canal = "correo"

    TITULOS = {
        TIPO_TAREA_CREADA: "Nueva tarea",
        TIPO_TAREA_ASIGNADA: "Tarea asignada",
        TIPO_ESTADO_CAMBIADO: "Cambio de estado",
        TIPO_FLUJO_RECONFIGURADO: "Flujo del proyecto reconfigurado",
    }

    def __init__(self, gateway, remitente_por_defecto=None):
        if not isinstance(gateway, ExternalGateway):
            raise TypeError("EmailNotification requiere un ExternalGateway.")
        self._gateway = gateway
        self._remitente_por_defecto = remitente_por_defecto

    def update(self, event) -> dict:
        destinatario = self._destinatario(event)
        if not destinatario:
            return {"transport": self.canal, "omitido": "sin destinatario para este evento"}
        respuesta = self._gateway.send(destinatario, self._asunto(event), self._cuerpo(event))
        print(
            f"  [CORREO] -> {respuesta['destinatario_resuelto']} | "
            f"{event.mensaje} | id={respuesta['referencia']}"
        )
        return respuesta

    def _destinatario(self, event):
        responsable = getattr(event.origen, "responsable", None)
        if responsable is not None:
            return responsable.email
        return self._remitente_por_defecto

    def _asunto(self, event):
        return f"[{event.proyecto.nombre}] {self.TITULOS.get(event.tipo, event.tipo)}"

    def _cuerpo(self, event):
        origen = event.origen
        return "\n".join(
            [
                f"Proyecto: {event.proyecto.nombre} ({event.proyecto.id})",
                f"Evento  : {event.tipo}",
                f"Detalle : {event.mensaje}",
                f"Origen  : {origen.id if hasattr(origen, 'id') else event.proyecto.id}",
            ]
        )
