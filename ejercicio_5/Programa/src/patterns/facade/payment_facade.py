from src.domain.payment_result import PaymentResult
from src.patterns.factory.payment_factory import PaymentFactory
from src.patterns.observer.notifiers import EmailNotifier
from src.patterns.observer.notifiers import SmsNotifier
from src.patterns.observer.notifiers import WebhookNotifier
from src.patterns.template.payment_processor_factory import PaymentProcessorFactory


class PaymentFacade:

    def __init__(self):
        self._payment_factory = PaymentFactory()
        self._processor_factory = PaymentProcessorFactory()

    def pay(self, method_type: str, amount: float, country: str, client_type: str = "standard") -> PaymentResult:
        method = self._payment_factory.create(method_type, country)
        processor = self._processor_factory.create(country)
        processor.notifier.attach(EmailNotifier())
        processor.notifier.attach(SmsNotifier())
        processor.notifier.attach(WebhookNotifier())
        return processor.process_payment(method, amount, country, client_type)