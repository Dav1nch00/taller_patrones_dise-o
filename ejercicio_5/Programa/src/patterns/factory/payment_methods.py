from abc import ABC, abstractmethod


class PaymentMethod(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def supports(self, country: str) -> bool:
        pass


class CreditCardPayment(PaymentMethod):

    @property
    def name(self) -> str:
        return "credit_card"

    def supports(self, country: str) -> bool:
        return True


class BankTransferSEPA(PaymentMethod):

    @property
    def name(self) -> str:
        return "sepa"

    def supports(self, country: str) -> bool:
        return country.upper() in {"EU", "DE", "FR", "ES", "IT"}


class BankTransferACH(PaymentMethod):

    @property
    def name(self) -> str:
        return "ach"

    def supports(self, country: str) -> bool:
        return country.upper() in {"US", "MX"}


class CryptoPayment(PaymentMethod):

    @property
    def name(self) -> str:
        return "crypto"

    def supports(self, country: str) -> bool:
        return True


class DigitalWallet(PaymentMethod):

    @property
    def name(self) -> str:
        return "digital_wallet"

    def supports(self, country: str) -> bool:
        return True