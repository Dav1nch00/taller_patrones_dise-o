from patterns.state.reservation_state import InvalidStateTransitionError, ReservationState


class BoardedState(ReservationState):
    def modify(self, reservation):
        raise InvalidStateTransitionError("Una reserva abordada no puede modificarse.")

    def confirm(self, reservation):
        raise InvalidStateTransitionError("Una reserva abordada ya está confirmada.")

    def cancel(self, reservation):
        raise InvalidStateTransitionError("Una reserva abordada no puede cancelarse.")

    def check_in(self, reservation):
        raise InvalidStateTransitionError("Una reserva abordada ya hizo check-in.")

    def board(self, reservation):
        raise InvalidStateTransitionError("El pasajero ya abordó.")