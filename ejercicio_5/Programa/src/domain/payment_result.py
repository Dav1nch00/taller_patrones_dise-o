from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PaymentResult:
    success: bool
    message: str
    transaction_id: str = ""
    amount: float = 0.0
    currency: str = "USD"
    commission: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)