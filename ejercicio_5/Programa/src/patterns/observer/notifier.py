from src.patterns.observer.observer import PaymentObserver


class PaymentNotifier:

    def __init__(self):
        self._observers = []

    def attach(self, observer: PaymentObserver):
        self._observers.append(observer)

    def detach(self, observer: PaymentObserver):
        self._observers.remove(observer)

    def notify(self, event: str, data: dict):
        for observer in self._observers:
            observer.update(event, data)