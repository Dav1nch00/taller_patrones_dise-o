class SmtpDeliveryError(Exception):
    pass


class ExternalSmtpEmailAPI:
    """API de un tercero. No se modifica: se envuelve con un adaptador.

    Simula heterogeneidad real: los parametros se llaman distinto que en Slack,
    el exito se informa con un codigo numerico 'status', y los errores se lanzan
    como excepcion en vez de devolverse en el dict.
    """

    def __init__(self, host, port=587, remitente="no-reply@correo.legacy.corp"):
        self._host = host
        self._port = port
        self._remitente = remitente
        self._envios = 0
        self._last_body = ""

    def send_mail(self, to_address, subject, body):
        if not isinstance(to_address, str) or "@" not in to_address:
            raise SmtpDeliveryError(f"Direccion de correo invalida: {to_address!r}")
        if not str(subject).strip():
            raise SmtpDeliveryError("El asunto no puede ir vacio.")
        self._envios += 1
        self._last_body = body
        return {
            "status": 250,
            "message_id": f"<{self._envios:04d}.{abs(hash(to_address)) % 10**6}@{self._host}>",
            "accepted_recipients": [to_address],
            "queued_at": "2026-09-26T10:15:00",
        }

    def get_last_body(self):
        return self._last_body
