from patterns.state.reservation_state import InvalidStateTransitionError, ReservationState


class ConfirmedState(ReservationState):
    def modify(self, reservation):
        raise InvalidStateTransitionError("Solo se pueden modificar reservas en estado pendiente.")

    def confirm(self, reservation):
        raise InvalidStateTransitionError("La reserva ya está confirmada.")

    def cancel(self, reservation):
        from patterns.state.cancelled_state import CancelledState

        reservation.change_state(CancelledState())

    def check_in(self, reservation):
        from patterns.state.check_in_state import CheckInState

        reservation.change_state(CheckInState())

    def board(self, reservation):
        raise InvalidStateTransitionError("Se requiere check-in antes de abordar.")