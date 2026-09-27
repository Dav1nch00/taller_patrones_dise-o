from abc import ABC, abstractmethod


class ExternalGateway(ABC):
    """Interfaz uniforme para cualquier canal de notificacion.

    Obliga a que el dominio y los observadores hablen un solo idioma. 'destinatario'
    no significa lo mismo en cada canal: es una direccion de correo en SMTP y un
    canal o usuario de Slack en la API de Slack. Esa ambiguedad es intencional,
    la resuelve el adaptador de cada canal.
    """

    @abstractmethod
    def send(self, destinatario, asunto, cuerpo) -> dict:
        pass
