import uuid

from src.patterns.adapter.gateway import PaymentGateway


class MercadoPagoAPI:

    def payment_create(self, payload: dict) -> dict:
        return {"id": f"mp_{uuid.uuid4().hex[:12]}", "status": payload.get("status", "approved")}


class MercadoPagoAdapter(PaymentGateway):

    def __init__(self):
        self._api = MercadoPagoAPI()

    def charge(self, amount: float, currency: str, token: str) -> str:
        payload = {"transaction_amount": amount, "currency": currency, "token": token}
        result = self._api.payment_create(payload)
        return result["id"]