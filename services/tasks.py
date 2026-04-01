from fastapi import Depends

from core.exceptions import TaskNotFound
from models.tasks import Task
from repositories.tasks import TaskRepository
from schemas.tasks import TaskCreate


class TaskService:
    def __init__(self, repository: TaskRepository = Depends(TaskRepository)):
        self.repository = repository

    async def create_task(self, task_in: TaskCreate, user_id: int) -> Task:
        return await self.repository.create(task_in=task_in, user_id=user_id)

    async def get_all_tasks(self, user_id: int) -> list[Task]:
        return await self.repository.get_all(user_id=user_id)

    async def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = await self.repository.get_by_id(task_id=task_id, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task

    async def update_task(self, task_id: int, task_in: TaskCreate, user_id: int) -> Task:
        task = await self.repository.update(task_id=task_id, task_in=task_in, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task
        
    async def update_avatar(self, task_id: int, user_id: int, avatar_url: str) -> Task:
        task = await self.repository.update_avatar(task_id=task_id, user_id=user_id, avatar_url=avatar_url)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        is_deleted = await self.repository.delete(task_id=task_id, user_id=user_id)
        if not is_deleted:
            raise TaskNotFound(task_id=task_id)
