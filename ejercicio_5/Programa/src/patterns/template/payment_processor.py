from abc import ABC, abstractmethod

from src.config.payment_config import PaymentConfig
from src.domain.payment_request import PaymentRequest
from src.domain.payment_result import PaymentResult
from src.patterns.adapter.gateway import PaymentGateway
from src.patterns.factory.payment_methods import PaymentMethod
from src.patterns.observer.notifier import PaymentNotifier
from src.patterns.chain.handler import ValidationHandler
from src.patterns.strategy.commission import CommissionStrategy, PremiumCommission, StandardCommission
from src.patterns.strategy.conversion import CurrencyConversionStrategy, FixedRateConversion


class PaymentProcessor(ABC):

    def __init__(self):
        self._notifier = PaymentNotifier()

    @property
    def notifier(self) -> PaymentNotifier:
        return self._notifier

    def process_payment(self, method: PaymentMethod, amount: float, country: str, client_type: str) -> PaymentResult:
        config = PaymentConfig.get_instance()
        local_currency = self.get_currency()

        converted = self.conversion().convert(amount, local_currency, config.default_currency)
        request = PaymentRequest(amount=converted, country=country, method_type=method.name, client_type=client_type)

        if not self.validation_chain().handle(request):
            self.notifier.notify(
                "payment.failed",
                {"reason": "antifraud", "country": country, "amount": amount},
            )
            return PaymentResult(
                success=False,
                message="Pago rechazado por validacion antifraude",
                amount=amount,
                currency=local_currency,
            )

        commission = self.commission_strategy(client_type).calculate(converted)
        total = converted + commission

        transaction_id = self.gateway().charge(total, config.default_currency, f"token_{method.name}")

        result = PaymentResult(
            success=True,
            message="Pago aprobado",
            transaction_id=transaction_id,
            amount=converted,
            currency=config.default_currency,
            commission=commission,
        )
        self.notifier.notify(
            "payment.success",
            {"transaction_id": transaction_id, "amount": converted, "commission": commission},
        )
        return result

    def conversion(self) -> CurrencyConversionStrategy:
        return FixedRateConversion()

    def commission_strategy(self, client_type: str) -> CommissionStrategy:
        if client_type == "premium":
            return PremiumCommission()
        return StandardCommission()

    @abstractmethod
    def get_currency(self) -> str:
        pass

    @abstractmethod
    def validation_chain(self) -> ValidationHandler:
        pass

    @abstractmethod
    def gateway(self) -> PaymentGateway:
        pass