
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department


class DepartmentRepository: 

    async def get_by_name(self, db: AsyncSession, name: str) -> Department | None:
        result = await db.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, department: Department) -> Department:
        db.add(department)
        return department
