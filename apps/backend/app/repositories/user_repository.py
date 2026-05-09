import uuid

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.enums.user_role import UserRole
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
            select(User).where(User.id == user_id).options(joinedload(User.department))
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

    async def get_all(
        self,
        db: AsyncSession,
        role: UserRole | None = None,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        filters = []
        if role is not None:
            filters.append(User.role == role)
        if department_id is not None:
            filters.append(User.department_id == department_id)
        if is_active is not None:
            filters.append(User.is_active == is_active)

        result = await db.execute(select(User).where(and_(*filters)).options(joinedload(User.department)))
        return list(result.scalars().all())

