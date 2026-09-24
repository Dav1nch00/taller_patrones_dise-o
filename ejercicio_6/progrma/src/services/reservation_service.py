from patterns.builder.reservation_builder import ReservationBuilder
from patterns.observer.app_notifier import AppNotifier
from patterns.observer.email_notifier import EmailNotifier
from patterns.observer.sms_notifier import SMSNotifier


class ReservationService:
    def crear_reserva(self, passenger, flight, base_price, services=None, preferences=None, pricing_strategy=None):
        builder = ReservationBuilder()
        builder.set_passenger(passenger)
        builder.set_flight(flight)
        builder.set_base_price(base_price)
        for service in services or []:
            builder.add_service(service)
        for key, value in (preferences or {}).items():
            builder.set_preference(key, value)
        builder.set_pricing_strategy(pricing_strategy)
        reservation = builder.build()
        self.adjuntar_notificadores(reservation)
        return reservation

    def adjuntar_notificadores(self, reservation):
        reservation.attach(EmailNotifier())
        reservation.attach(SMSNotifier())
        reservation.attach(AppNotifier())

    def calcular_precio(self, reservation, season="regular", anticipation_days=0):
        return reservation.calculate_price(season, anticipation_days)

    def modificar(self, reservation):
        return reservation.modify()

    def confirmar(self, reservation):
        reservation.confirm()

    def cancelar(self, reservation):
        reservation.cancel()

    def check_in(self, reservation):
        reservation.check_in()

    def abordar(self, reservation):
        reservation.board()

    def upgrade(self, reservation, pricing_strategy):
        reservation.set_pricing_strategy(pricing_strategy)