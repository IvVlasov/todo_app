from datetime import datetime

from pydantic import BaseModel, Field

from backend.core.constants import TaskStatus


def get_current_time() -> datetime:
    return datetime.now()


class Task(BaseModel):
    task_id: int | None = None
    user_id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime | None = Field(default_factory=get_current_time)


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
