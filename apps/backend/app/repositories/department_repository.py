import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department


class DepartmentRepository: 

    async def get_all(self, db: AsyncSession, page: int = 1, page_size: int = 20) -> tuple[list[Department], int]:
        count_result = await db.execute(select(func.count()).select_from(Department))
        total = count_result.scalar_one()

        query = select(Department).order_by(Department.name).limit(page_size).offset((page - 1) * page_size)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    async def get_by_id(self, db: AsyncSession, department_id: uuid.UUID) -> Department | None:
        result = await db.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, db: AsyncSession, name: str) -> Department | None:
        result = await db.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, department: Department) -> Department:
        db.add(department)
        return department

    async def count_active(self, db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count()).where(
                Department.is_active.is_(True),
                Department.deleted_at.is_(None),
            )
        )
        return result.scalar_one()
