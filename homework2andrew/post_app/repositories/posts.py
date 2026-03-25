from typing import List, Optional
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_db
from models import Post


class PostRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, post_text: str, owner_id: int, img_url: Optional[str] = None) -> Post:
        db_post = Post(post_text=post_text, owner_id=owner_id, img_url=img_url)
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        result = await self.db.execute(select(Post).filter(Post.id == post_id))
        return result.scalars().first()

    async def get_all(self) -> List[Post]:
        result = await self.db.execute(select(Post))
        return result.scalars().all()

    async def delete(self, post: Post) -> None:
        await self.db.delete(post)
        await self.db.commit()
