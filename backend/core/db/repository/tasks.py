from backend.core.db.repository.base import BaseRepository
from backend.core.models import Task, TaskUpdate


class TaskRepository(BaseRepository):
    """Task repository"""

    async def create_task(self, task: Task) -> None:
        """Create task"""
        query = """
            INSERT INTO tasks (title, description, user_id, status, created_at) VALUES ($1, $2, $3, $4, $5)
        """
        await self.connector.execute_query(
            query,
            task.title,
            task.description,
            task.user_id,
            task.status,
            task.created_at,
        )

    async def get_tasks_by_user_id(self, user_id: int) -> list[Task]:
        """Get tasks by user id"""
        query = """
            SELECT * FROM tasks WHERE user_id = $1
        """
        result = await self.connector.get_query_result_as_list(query, user_id)
        if not result:
            return []
        return [Task(**task) for task in result]

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> None:
        """Update task"""
        query = """
            UPDATE tasks SET {set_query} WHERE task_id = $1
        """
        set_query = ", ".join(
            [
                f"{key} = ${idx + 2}"
                for idx, key in enumerate(
                    task_update.model_dump(exclude_none=True).keys()
                )
            ]
        )
        query = query.format(set_query=set_query)
        await self.connector.execute_query(
            query, task_id, *task_update.model_dump(exclude_none=True).values()
        )

    async def delete_task(self, task_id: int) -> None:
        """Delete task"""
        query = """
            DELETE FROM tasks WHERE task_id = $1
        """
        await self.connector.execute_query(query, task_id)
