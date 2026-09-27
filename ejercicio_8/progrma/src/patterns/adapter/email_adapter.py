from patterns.adapter.external_gateway import ExternalGateway
from patterns.adapter.external_smtp_email_api import ExternalSmtpEmailAPI, SmtpDeliveryError


class EmailAdapter(ExternalGateway):
    """Traduce ExternalGateway a la interfaz de ExternalSmtpEmailAPI.

    La API falla lanzando SmtpDeliveryError y confirma con un 'status' numerico;
    la interfaz devuelve un dict. Aqui se captura la excepcion del tercero para
    que el observador no tenga que conocerla, y se normaliza la respuesta.
    """

    def __init__(self, api, remitente="notificaciones@plataforma.corp"):
        self._api = api
        self._remitente = remitente

    @property
    def remitente(self):
        return self._remitente

    def send(self, destinatario, asunto, cuerpo) -> dict:
        try:
            respuesta = self._api.send_mail(destinatario, asunto, cuerpo)
        except SmtpDeliveryError as error:
            raise RuntimeError(f"El servidor de correo rechazo el envio: {error}") from error
        if respuesta.get("status", 0) >= 400:
            raise RuntimeError(f"El servidor de correo devolvio status {respuesta['status']}.")
        return {
            "transport": "smtp",
            "destinatario_resuelto": respuesta.get("accepted_recipients", [destinatario])[0],
            "referencia": respuesta.get("message_id"),
            "respuesta_externa": respuesta,
        }
