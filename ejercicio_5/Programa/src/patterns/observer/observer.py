from abc import ABC, abstractmethod


class PaymentObserver(ABC):

    @abstractmethod
    def update(self, event: str, data: dict):
        pass