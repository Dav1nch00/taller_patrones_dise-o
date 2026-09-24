from patterns.observer.notification_observer import NotificationObserver


class AppNotifier(NotificationObserver):
    def update(self, event, reservation):
        print(f"[APP] Notificación para: {reservation.passenger.nombre} | {event}")