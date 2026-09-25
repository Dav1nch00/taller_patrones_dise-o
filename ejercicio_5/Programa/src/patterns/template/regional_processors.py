from src.patterns.adapter.mercadopago_adapter import MercadoPagoAdapter
from src.patterns.adapter.paypal_adapter import PayPalAdapter
from src.patterns.adapter.stripe_adapter import StripeAdapter
from src.patterns.strategy.commission import CommissionStrategy, InternationalCommission
from src.patterns.template.payment_processor import PaymentProcessor


class ColombiaProcessor(PaymentProcessor):

    def __init__(self):
        super().__init__()
        self._gw = MercadoPagoAdapter()

    def get_currency(self) -> str:
        return "COP"

    def validation_chain(self):
        from src.patterns.chain.validators import AmountValidator, BehaviorPatternValidator, HighRiskCountryValidator

        chain = AmountValidator()
        chain.set_next(HighRiskCountryValidator()).set_next(BehaviorPatternValidator())
        return chain

    def gateway(self):
        return self._gw


class MexicoProcessor(PaymentProcessor):

    def __init__(self):
        super().__init__()
        self._gw = MercadoPagoAdapter()

    def get_currency(self) -> str:
        return "MXN"

    def validation_chain(self):
        from src.patterns.chain.validators import AmountValidator, BehaviorPatternValidator, HighRiskCountryValidator

        chain = AmountValidator()
        chain.set_next(HighRiskCountryValidator()).set_next(BehaviorPatternValidator())
        return chain

    def gateway(self):
        return self._gw


class USProcessor(PaymentProcessor):

    def __init__(self):
        super().__init__()
        self._gw = StripeAdapter()

    def get_currency(self) -> str:
        return "USD"

    def validation_chain(self):
        from src.patterns.chain.validators import AmountValidator, BehaviorPatternValidator, HighRiskCountryValidator

        chain = AmountValidator()
        chain.set_next(HighRiskCountryValidator()).set_next(BehaviorPatternValidator())
        return chain

    def gateway(self):
        return self._gw


class EuropeProcessor(PaymentProcessor):

    def __init__(self):
        super().__init__()
        self._gw = PayPalAdapter()

    def get_currency(self) -> str:
        return "EUR"

    def commission_strategy(self, client_type: str) -> CommissionStrategy:
        return InternationalCommission()

    def validation_chain(self):
        from src.patterns.chain.validators import AmountValidator, BehaviorPatternValidator, HighRiskCountryValidator

        chain = AmountValidator()
        chain.set_next(HighRiskCountryValidator()).set_next(BehaviorPatternValidator())
        return chain

    def gateway(self):
        return self._gw