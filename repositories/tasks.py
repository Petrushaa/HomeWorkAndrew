from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.tasks import Task
from schemas.tasks import TaskCreate

class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, user_id: int):
        return self.db.query(Task).filter(Task.owner_id == user_id).all()

    def get_by_id(self, task_id: int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

    def create(self, task_in: TaskCreate, user_id: int):
        db_task = Task(**task_in.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, task_id: int, task_in: TaskCreate, user_id: int):
        db_task = self.get_by_id(task_id, user_id)
        if not db_task:
            return None
        
        for key, value in task_in.model_dump().items():
            setattr(db_task, key, value)
            
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int, user_id: int):
        db_task = self.get_by_id(task_id, user_id)
        if not db_task:
            return False
            
        self.db.delete(db_task)
        self.db.commit()
        return True
