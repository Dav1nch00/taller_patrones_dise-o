from abc import ABC, abstractmethod


class InvalidStateTransitionError(Exception):
    pass


class TaskNotMutableError(InvalidStateTransitionError):
    pass


class TaskState(ABC):
    """Estado del ciclo de vida de una tarea (State pattern).

    Cada subclase implementa todas las acciones posibles; las que no aplican
    a su estado se rechazan con _rechazar. Las que si aplican delegan en
    Task.change_state, que a su vez valida contra el Workflow configurado.
    """

    name = "AbstractState"

    @abstractmethod
    def start(self, task):
        pass

    @abstractmethod
    def submit_for_review(self, task):
        pass

    @abstractmethod
    def approve(self, task):
        pass

    @abstractmethod
    def reject(self, task):
        pass

    @abstractmethod
    def block(self, task, motivo=""):
        pass

    @abstractmethod
    def unblock(self, task):
        pass

    @abstractmethod
    def is_mutable(self):
        pass

    def _rechazar(self, task, accion):
        raise InvalidStateTransitionError(
            f"Accion '{accion}' no permitida sobre la tarea {task.id} en estado {self.name}."
        )
