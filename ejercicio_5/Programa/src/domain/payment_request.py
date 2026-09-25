from dataclasses import dataclass


@dataclass
class PaymentRequest:
    amount: float
    country: str
    method_type: str
    client_type: str = "standard"