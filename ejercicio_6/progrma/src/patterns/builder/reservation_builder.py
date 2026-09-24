from domain.reservation import Reservation
from patterns.state.pending_state import PendingState


class ReservationBuilder:
    def __init__(self):
        self._passenger = None
        self._flight = None
        self._base_price = 0.0
        self._services = []
        self._preferences = {}
        self._pricing_strategy = None

    def set_passenger(self, passenger):
        self._passenger = passenger
        return self

    def set_flight(self, flight):
        self._flight = flight
        return self

    def set_base_price(self, base_price):
        self._base_price = base_price
        return self

    def add_service(self, service):
        self._services.append(service)
        return self

    def set_preference(self, key, value):
        self._preferences[key] = value
        return self

    def set_pricing_strategy(self, pricing_strategy):
        self._pricing_strategy = pricing_strategy
        return self

    def build(self):
        if self._passenger is None:
            raise ValueError("Se requiere un pasajero para construir la reserva.")
        if self._flight is None:
            raise ValueError("Se requiere un vuelo para construir la reserva.")
        if self._pricing_strategy is None:
            raise ValueError("Se requiere una estrategia de precio para construir la reserva.")
        reservation = Reservation(
            self._passenger,
            self._flight,
            self._base_price,
            self._services,
            self._preferences,
        )
        reservation.set_pricing_strategy(self._pricing_strategy)
        reservation.change_state(PendingState())
        return reservation