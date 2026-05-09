import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        return user
    

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: uuid.UUID) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def count_active_by_department(self, db: AsyncSession, department_id: uuid.UUID) -> int:
        result = await db.execute(
            select(func.count()).where(
                User.department_id == department_id,
                User.is_active == True,
            )
        )
        return result.scalar_one()

    async def get_all(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return list(result.scalars().all())

