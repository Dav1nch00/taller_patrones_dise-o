from src.patterns.factory.payment_methods import (
    BankTransferACH,
    BankTransferSEPA,
    CreditCardPayment,
    CryptoPayment,
    DigitalWallet,
    PaymentMethod,
)


class PaymentFactory:

    _registry = {
        "credit_card": CreditCardPayment,
        "sepa": BankTransferSEPA,
        "ach": BankTransferACH,
        "crypto": CryptoPayment,
        "digital_wallet": DigitalWallet,
    }

    def create(self, method_type: str, country: str) -> PaymentMethod:
        if method_type not in self._registry:
            raise ValueError(f"Metodo de pago no soportado: {method_type}")
        method = self._registry[method_type]()
        if not method.supports(country):
            raise ValueError(f"Metodo {method_type} no disponible en {country}")
        return method