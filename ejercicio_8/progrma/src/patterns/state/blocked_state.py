from patterns.state.task_state import TaskState


class BlockedState(TaskState):
    name = "Blocked"

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
        from patterns.state.in_progress_state import InProgressState

        task.change_state(InProgressState(), "unblock")

    def is_mutable(self):
        return True
