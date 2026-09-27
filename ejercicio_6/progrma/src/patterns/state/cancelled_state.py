from patterns.state.reservation_state import InvalidStateTransitionError, ReservationState


class CancelledState(ReservationState):
    def modify(self, reservation):
        raise InvalidStateTransitionError("Una reserva cancelada no puede modificarse.")

    def confirm(self, reservation):
        raise InvalidStateTransitionError("Una reserva cancelada no puede confirmarse.")

    def cancel(self, reservation):
        raise InvalidStateTransitionError("La reserva ya está cancelada.")

    def check_in(self, reservation):
        raise InvalidStateTransitionError("Una reserva cancelada no puede hacer check-in.")

    def board(self, reservation):
        raise InvalidStateTransitionError("Una reserva cancelada no puede abordar.")