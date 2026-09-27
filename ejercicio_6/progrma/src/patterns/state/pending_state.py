from patterns.state.reservation_state import InvalidStateTransitionError, ReservationState


class PendingState(ReservationState):
    def modify(self, reservation):
        return "Reserva modificada."

    def confirm(self, reservation):
        from patterns.state.confirmed_state import ConfirmedState

        reservation.change_state(ConfirmedState())

    def cancel(self, reservation):
        from patterns.state.cancelled_state import CancelledState

        reservation.change_state(CancelledState())

    def check_in(self, reservation):
        raise InvalidStateTransitionError("No se puede hacer check-in de una reserva pendiente.")

    def board(self, reservation):
        raise InvalidStateTransitionError("No se puede abordar una reserva pendiente.")