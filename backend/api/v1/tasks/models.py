from pydantic import BaseModel

from backend.core.models import Task


class UserTasksResponse(BaseModel):
    """User create response model"""

    tasks: list[Task]
