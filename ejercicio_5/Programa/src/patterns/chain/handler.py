from abc import ABC, abstractmethod


class ValidationHandler(ABC):

    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, request) -> bool:
        if self._validate(request):
            return self._next.handle(request) if self._next is not None else True
        return False

    @abstractmethod
    def _validate(self, request) -> bool:
        pass