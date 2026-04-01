import uuid
from fastapi import Depends, UploadFile, HTTPException

from core.exceptions import TaskNotFound
from models import Task
from repositories import TaskRepository
from schemas import TaskCreate
from adapters.storage.base import StorageAdapter
from core.adapters import get_storage


class TaskService:
    def __init__(
        self,
        repository: TaskRepository = Depends(TaskRepository),
        storage: StorageAdapter = Depends(get_storage)
    ):
        self.repository = repository
        self.storage = storage

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
        
    async def update_avatar(self, task_id: int, user_id: int, file: UploadFile) -> Task:
        task = await self.get_task_by_id(task_id=task_id, user_id=user_id)
        
        content = await file.read()
        ext = file.filename.split('.')[-1] if file.filename else "bin"
        key = f"tasks/{task_id}_{uuid.uuid4()}.{ext}"
        
        try:
            url = await self.storage.upload_file(content, key, file.content_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
            
        task = await self.repository.update_avatar(task_id=task_id, user_id=user_id, avatar_url=url)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        is_deleted = await self.repository.delete(task_id=task_id, user_id=user_id)
        if not is_deleted:
            raise TaskNotFound(task_id=task_id)
