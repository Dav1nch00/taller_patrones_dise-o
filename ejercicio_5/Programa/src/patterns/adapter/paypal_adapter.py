import uuid

from src.patterns.adapter.gateway import PaymentGateway


class PayPalAPI:

    def payment(self, amount: str, curr: str, payer: str) -> dict:
        return {"id": f"paypal_{uuid.uuid4().hex[:12]}", "status": "approved", "amount": amount}


class PayPalAdapter(PaymentGateway):

    def __init__(self):
        self._api = PayPalAPI()

    def charge(self, amount: float, currency: str, token: str) -> str:
        result = self._api.payment(str(round(amount, 2)), currency, token)
        return result["id"]