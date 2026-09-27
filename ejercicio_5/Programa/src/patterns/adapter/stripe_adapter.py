import uuid

from src.patterns.adapter.gateway import PaymentGateway


class StripeAPI:

    def create_charge(self, amount_cents: int, currency: str, source: str) -> str:
        return f"stripe_{uuid.uuid4().hex[:12]}"


class StripeAdapter(PaymentGateway):

    def __init__(self):
        self._api = StripeAPI()

    def charge(self, amount: float, currency: str, token: str) -> str:
        cents = int(round(amount * 100))
        return self._api.create_charge(cents, currency, token)