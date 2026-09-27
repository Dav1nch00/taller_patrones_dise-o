from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from domain.additional_service import AdditionalService
from domain.flight import Flight
from domain.passenger import Passenger

if TYPE_CHECKING:
    from patterns.observer.notification_observer import NotificationObserver
    from patterns.state.reservation_state import ReservationState
    from patterns.strategy.pricing_strategy import PricingStrategy


class Reservation:
    def __init__(self, passenger, flight, base_price, services=None, preferences=None):
        self._passenger = passenger
        self._flight = flight
        self._base_price = float(base_price)
        self._services = list(services or [])
        self._preferences = dict(preferences or {})
        self._state = None
        self._pricing_strategy = None
        self._observers = []

    @property
    def passenger(self):
        return self._passenger

    @property
    def flight(self):
        return self._flight

    @property
    def base_price(self):
        return self._base_price

    @property
    def services(self):
        return list(self._services)

    @property
    def preferences(self):
        return dict(self._preferences)

    @property
    def state(self):
        return self._state

    @property
    def pricing_strategy(self):
        return self._pricing_strategy

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self, event):
        for observer in list(self._observers):
            observer.update(event, self)

    def change_state(self, new_state):
        previous_name = self._state.__class__.__name__ if self._state else "sin estado"
        self._state = new_state
        self._notify(f"Estado: {previous_name} -> {new_state.__class__.__name__}")

    def set_pricing_strategy(self, strategy):
        self._pricing_strategy = strategy

    def calculate_price(self, season="regular", anticipation_days=0):
        if self._pricing_strategy is None:
            raise RuntimeError("Sin estrategia de precio configurada.")
        subtotal = self._base_price + sum(s.costo for s in self._services)
        return self._pricing_strategy.calculate_price(subtotal, season, anticipation_days)

    def modify(self):
        return self._state.modify(self)

    def confirm(self):
        return self._state.confirm(self)

    def cancel(self):
        return self._state.cancel(self)

    def check_in(self):
        return self._state.check_in(self)

    def board(self):
        return self._state.board(self)

    def __str__(self):
        state_name = self._state.__class__.__name__ if self._state else "sin estado"
        return f"Reservation(passenger={self._passenger.nombre}, flight={self._flight.numero_vuelo}, state={state_name})"