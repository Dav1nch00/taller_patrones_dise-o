from abc import ABC, abstractmethod


class CommissionStrategy(ABC):

    @abstractmethod
    def calculate(self, base_amount: float) -> float:
        pass


class StandardCommission(CommissionStrategy):

    def calculate(self, base_amount: float) -> float:
        return base_amount * 0.02


class PremiumCommission(CommissionStrategy):

    def calculate(self, base_amount: float) -> float:
        return base_amount * 0.005


class InternationalCommission(CommissionStrategy):

    def calculate(self, base_amount: float) -> float:
        return base_amount * 0.035