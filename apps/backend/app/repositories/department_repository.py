import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department


class DepartmentRepository: 

    async def get_all(self, db: AsyncSession) -> list[Department]:
        result = await db.execute(select(Department))
        return list(result.scalars().all())

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
