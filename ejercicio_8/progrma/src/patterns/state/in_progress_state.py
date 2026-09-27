from patterns.state.task_state import TaskState


class InProgressState(TaskState):
    name = "InProgress"

    def start(self, task):
        self._rechazar(task, "start")

    def submit_for_review(self, task):
        from patterns.state.in_review_state import InReviewState

        task.change_state(InReviewState(), "submit_for_review")

    def approve(self, task):
        self._rechazar(task, "approve")

    def reject(self, task):
        self._rechazar(task, "reject")

    def block(self, task, motivo=""):
        from patterns.state.blocked_state import BlockedState

        task.change_state(BlockedState(), "block", motivo)

    def unblock(self, task):
        self._rechazar(task, "unblock")

    def is_mutable(self):
        return True
