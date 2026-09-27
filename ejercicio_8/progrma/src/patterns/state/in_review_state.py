from patterns.state.task_state import TaskState


class InReviewState(TaskState):
    name = "InReview"

    def start(self, task):
        self._rechazar(task, "start")

    def submit_for_review(self, task):
        self._rechazar(task, "submit_for_review")

    def approve(self, task):
        from patterns.state.done_state import DoneState

        task.change_state(DoneState(), "approve")

    def reject(self, task):
        from patterns.state.in_progress_state import InProgressState

        task.change_state(InProgressState(), "reject")

    def block(self, task, motivo=""):
        from patterns.state.blocked_state import BlockedState

        task.change_state(BlockedState(), "block", motivo)

    def unblock(self, task):
        self._rechazar(task, "unblock")

    def is_mutable(self):
        return True
