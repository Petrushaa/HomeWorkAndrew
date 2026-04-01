from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr

from core.database import get_db
from core.security import hash_password
from models.users import User
from schemas.users import UserRegistrationSchema

class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, new_user: UserRegistrationSchema) -> User:
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = hash_password(new_user.password)
        user_dict.pop("password")
        
        db_user = User(**user_dict)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def get_by_email(self, email: str | EmailStr) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == str(email)))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
