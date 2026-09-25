from src.config.payment_config import PaymentConfig
from src.patterns.chain.handler import ValidationHandler


class AmountValidator(ValidationHandler):

    def __init__(self):
        super().__init__()
        self._config = PaymentConfig.get_instance()

    def _validate(self, request) -> bool:
        return request.amount <= self._config.threshold(request.country)


class HighRiskCountryValidator(ValidationHandler):

    _high_risk_countries = {"CU", "IR", "KP", "SY", "VE"}

    def _validate(self, request) -> bool:
        return request.country.upper() not in self._high_risk_countries


class BehaviorPatternValidator(ValidationHandler):

    _max_operational_amount = 50000.0

    def _validate(self, request) -> bool:
        return request.amount <= self._max_operational_amount