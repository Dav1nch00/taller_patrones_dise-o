from abc import ABC, abstractmethod


class InvalidStateTransitionError(Exception):
    pass


class ReservationState(ABC):
    @abstractmethod
    def modify(self, reservation):
        pass

    @abstractmethod
    def confirm(self, reservation):
        pass

    @abstractmethod
    def cancel(self, reservation):
        pass

    @abstractmethod
    def check_in(self, reservation):
        pass

    @abstractmethod
    def board(self, reservation):
        pass