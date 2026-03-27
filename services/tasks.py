from fastapi import Depends

from core.exceptions import TaskNotFound
from models.tasks import Task
from repositories.tasks import TaskRepository
from schemas.tasks import TaskCreate


class TaskService:
    def __init__(self, repository: TaskRepository = Depends(TaskRepository)):
        self.repository = repository

    def create_task(self, task_in: TaskCreate, user_id: int) -> Task:
        return self.repository.create(task_in=task_in, user_id=user_id)

    def get_all_tasks(self, user_id: int) -> list[Task]:
        return self.repository.get_all(user_id=user_id)

    def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        task = self.repository.get_by_id(task_id=task_id, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task

    def update_task(self, task_id: int, task_in: TaskCreate, user_id: int) -> Task:
        task = self.repository.update(task_id=task_id, task_in=task_in, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task

    def delete_task(self, task_id: int, user_id: int) -> None:
        is_deleted = self.repository.delete(task_id=task_id, user_id=user_id)
        if not is_deleted:
            raise TaskNotFound(task_id=task_id)
