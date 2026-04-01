from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_db
from models import Comment
from schemas import CommentCreate

class CommentRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, task_id: int, user_id: int, comment_in: CommentCreate) -> Comment:
        db_comment = Comment(text=comment_in.text, task_id=task_id, owner_id=user_id)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment

    async def get_by_task_id(self, task_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).filter(Comment.task_id == task_id))
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int, task_id: int) -> Comment | None:
        result = await self.db.execute(
            select(Comment).filter(Comment.id == comment_id, Comment.task_id == task_id)
        )
        return result.scalars().first()
