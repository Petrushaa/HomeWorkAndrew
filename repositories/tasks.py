from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from models import Task
from schemas import TaskCreate

class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self, user_id: int):
        result = await self.db.execute(select(Task).filter(Task.owner_id == user_id))
        return result.scalars().all()

    async def get_by_id(self, task_id: int, user_id: int):
        result = await self.db.execute(select(Task).filter(Task.id == task_id, Task.owner_id == user_id))
        return result.scalars().first()

    async def create(self, task_in: TaskCreate, user_id: int):
        db_task = Task(**task_in.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update(self, task_id: int, task_in: TaskCreate, user_id: int):
        db_task = await self.get_by_id(task_id, user_id)
        if not db_task:
            return None
        
        for key, value in task_in.model_dump().items():
            setattr(db_task, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update_avatar(self, task_id: int, user_id: int, avatar_url: str):
        db_task = await self.get_by_id(task_id, user_id)
        if not db_task:
            return None
            
        db_task.avatar_url = avatar_url
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete(self, task_id: int, user_id: int):
        db_task = await self.get_by_id(task_id, user_id)
        if not db_task:
            return False
            
        await self.db.delete(db_task)
        await self.db.commit()
        return True
