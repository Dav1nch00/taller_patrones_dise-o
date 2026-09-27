from patterns.state.reservation_state import InvalidStateTransitionError, ReservationState


class CheckInState(ReservationState):
    def modify(self, reservation):
        raise InvalidStateTransitionError("Solo se pueden modificar reservas en estado pendiente.")

    def confirm(self, reservation):
        raise InvalidStateTransitionError("La reserva ya está confirmada.")

    def cancel(self, reservation):
        raise InvalidStateTransitionError("Una reserva con check-in realizado no puede cancelarse.")

    def check_in(self, reservation):
        raise InvalidStateTransitionError("El check-in ya fue realizado.")

    def board(self, reservation):
        from patterns.state.boarded_state import BoardedState

        reservation.change_state(BoardedState())