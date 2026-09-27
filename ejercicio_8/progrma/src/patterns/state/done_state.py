from patterns.state.task_state import TaskState


class DoneState(TaskState):
    name = "Done"

    def start(self, task):
        self._rechazar(task, "start")

    def submit_for_review(self, task):
        self._rechazar(task, "submit_for_review")

    def approve(self, task):
        self._rechazar(task, "approve")

    def reject(self, task):
        self._rechazar(task, "reject")

    def block(self, task, motivo=""):
        self._rechazar(task, "block")

    def unblock(self, task):
        self._rechazar(task, "unblock")

    def is_mutable(self):
        return False
