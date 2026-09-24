from patterns.observer.notification_observer import NotificationObserver


class EmailNotifier(NotificationObserver):
    def update(self, event, reservation):
        print(f"[EMAIL] Para: {reservation.passenger.email} | {event}")