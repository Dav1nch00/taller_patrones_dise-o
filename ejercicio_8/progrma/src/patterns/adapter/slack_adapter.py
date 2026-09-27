from patterns.adapter.external_gateway import ExternalGateway
from patterns.adapter.external_slack_api import ExternalSlackAPI


class SlackAdapter(ExternalGateway):
    """Traduce ExternalGateway a la interfaz de ExternalSlackAPI.

    La API pide 'channel' y 'text' y se comunica con 'ok' y 'ts'; la interfaz
    pide destinatario, asunto y cuerpo. Aqui se decide que canal se usa, se arma el
    texto con formato de Slack, y se convierte la respuesta a una forma comun.
    """

    def __init__(self, api, canal_por_defecto="#proyectos"):
        self._api = api
        self._canal_por_defecto = canal_por_defecto

    @property
    def canal_por_defecto(self):
        return self._canal_por_defecto

    def send(self, destinatario, asunto, cuerpo) -> dict:
        es_canal = self._es_canal(destinatario)
        canal = destinatario if es_canal else self._canal_por_defecto
        respuesta = self._api.post_to_channel(canal, self._armar_texto(destinatario, es_canal, asunto, cuerpo))
        if not respuesta.get("ok"):
            raise RuntimeError(f"Slack rechazo el mensaje: {respuesta.get('error')}")
        return {
            "transport": "slack",
            "destinatario_resuelto": canal,
            "referencia": respuesta["ts"],
            "respuesta_externa": respuesta,
        }

    def _armar_texto(self, destinatario, es_canal, asunto, cuerpo):
        partes = [f"*{asunto}*"]
        if destinatario and not es_canal:
            partes.append(f"<{destinatario}>")
        partes.append(str(cuerpo))
        return "\n".join(partes)

    def _es_canal(self, destinatario):
        return bool(destinatario) and str(destinatario).startswith("#")
