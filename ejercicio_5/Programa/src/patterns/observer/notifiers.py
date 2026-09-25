from src.patterns.observer.observer import PaymentObserver


class EmailNotifier(PaymentObserver):

    def update(self, event: str, data: dict):
        print(f"[email] {event}: {data}")


class SmsNotifier(PaymentObserver):

    def update(self, event: str, data: dict):
        print(f"[sms] {event}: {data}")


class WebhookNotifier(PaymentObserver):

    def update(self, event: str, data: dict):
        print(f"[webhook] {event}: {data}")