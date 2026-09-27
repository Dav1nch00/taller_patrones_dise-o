from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def charge(self, amount: float, currency: str, token: str):
        pass