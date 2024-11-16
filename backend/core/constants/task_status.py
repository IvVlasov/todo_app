from backend.core.constants.base import AppStringEnum


class TaskStatus(AppStringEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__.values()
