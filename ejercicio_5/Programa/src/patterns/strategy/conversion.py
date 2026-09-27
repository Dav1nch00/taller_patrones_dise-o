from abc import ABC, abstractmethod

from src.config.payment_config import PaymentConfig


class CurrencyConversionStrategy(ABC):

    @abstractmethod
    def convert(self, amount: float, source: str, target: str) -> float:
        pass


class FixedRateConversion(CurrencyConversionStrategy):

    def __init__(self):
        self._config = PaymentConfig.get_instance()

    def convert(self, amount: float, source: str, target: str) -> float:
        return amount * self._config.exchange_rate(source, target)