class SlackApiError(Exception):
    pass


class ExternalSlackAPI:
    """API de un tercero. No se modifica: se envuelve con un adaptador.

    Simula heterogeneidad real: recibe 'channel' y 'text', valida por su cuenta,
    y devuelve 'ok: False' con un codigo de error en vez de lanzar excepcion.
    """

    def __init__(self, token, base_url="https://slack.com/api"):
        self._token = token
        self._base_url = base_url
        self._canales = ["#proyectos", "#QA", "#incidentes"]

    def post_to_channel(self, channel, text):
        if not isinstance(channel, str) or not channel.startswith("#"):
            return {"ok": False, "error": "channel_not_found"}
        if len(text) > 3000:
            return {"ok": False, "error": "msg_too_long"}
        return {
            "ok": True,
            "channel": channel,
            "ts": f"1758{len(text):06d}.000100",
            "text": text,
        }

    def list_channels(self):
        return {"ok": True, "channels": list(self._canales)}
