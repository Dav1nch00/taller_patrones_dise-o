from patterns.observer.notification_observer import NotificationObserver


class SMSNotifier(NotificationObserver):
    def update(self, event, reservation):
        print(f"[SMS] Para: {reservation.passenger.telefono} | {event}")