from abc import ABC, abstractmethod


class EventObserver(ABC):
    """Contrato unico de todo canal de la plataforma.

    update recibe un DomainEvent, no un texto: el canal decide con event.tipo que
    hacer y usa event.origen y event.proyecto para armar su contenido. Asi el
    dominio no menciona canales y los canales no dependen entre si.
    """

    canal = "desconocido"

    @abstractmethod
    def update(self, event) -> dict:
        pass
