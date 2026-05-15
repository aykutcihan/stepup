import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError, ValidationError, messages
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate

department_repository = DepartmentRepository()
user_repository = UserRepository()


class DepartmentService:

    async def reactivate_department(self, db: AsyncSession, department_id: uuid.UUID) -> Department:
        department = await department_repository.get_by_id(db, department_id)
        if not department:
            raise NotFoundError(*messages.DEPARTMENT_NOT_FOUND)

        department.is_active = True
        await db.commit()
        await db.refresh(department)
        return department

    async def deactivate_department(self, db: AsyncSession, department_id: uuid.UUID) -> Department:
        department = await department_repository.get_by_id(db, department_id)
        if not department:
            raise NotFoundError(*messages.DEPARTMENT_NOT_FOUND)

        active_user_count = await user_repository.count_active_by_department(db, department_id)
        if active_user_count > 0:
            raise ValidationError(*messages.DEPARTMENT_HAS_ACTIVE_USERS)

        department.is_active = False
        await db.commit()
        await db.refresh(department)
        return department

    async def get_all_departments(self, db: AsyncSession) -> list[Department]:
        return await department_repository.get_all(db)

    async def update_department(
        self, db: AsyncSession, department_id: uuid.UUID, data: DepartmentUpdate
    ) -> Department:
        department = await department_repository.get_by_id(db, department_id)
        if not department:
            raise NotFoundError(*messages.DEPARTMENT_NOT_FOUND)

        existing = await department_repository.get_by_name(db, data.name)
        if existing and existing.id != department_id:
            raise ValidationError(*messages.DEPARTMENT_ALREADY_EXISTS)

        department.name = data.name
        await db.commit()
        await db.refresh(department)
        return department

    async def create_department(self, db: AsyncSession, data: DepartmentCreate) -> Department:
        existing = await department_repository.get_by_name(db, data.name)
        if existing:
            raise ValidationError(*messages.DEPARTMENT_ALREADY_EXISTS)

        department = Department(name=data.name)
        await department_repository.create(db, department)
        await db.commit()
        await db.refresh(department)
        return department
