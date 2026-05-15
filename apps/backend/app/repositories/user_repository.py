import uuid

from sqlalchemy import and_, func, select
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
                User.is_active,
            )
        )
        return result.scalar_one()

    async def count_active(self, db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count()).where(
                User.is_active.is_(True),
                User.deleted_at.is_(None),
            )
        )
        return result.scalar_one()

    async def get_all(
        self,
        db: AsyncSession,
        role: UserRole | None = None,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[User], int]:
        filters = []
        if role is not None:
            filters.append(User.role == role)
        if department_id is not None:
            filters.append(User.department_id == department_id)
        if is_active is not None:
            filters.append(User.is_active == is_active)

        count_query = select(func.count()).select_from(User)
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = await db.execute(count_query)
        total = count_result.scalar_one()

        query = select(User).options(joinedload(User.department))
        if filters:
            query = query.where(and_(*filters))
        query = query.order_by(User.created_at.desc()).limit(page_size).offset((page - 1) * page_size)
        result = await db.execute(query)
        return list(result.scalars().all()), total

