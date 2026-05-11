import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate
from app.models.template_task import TemplateTask

class TemplateRepository:
    async def create(
        self, db: AsyncSession, template: OnboardingTemplate
    ) -> OnboardingTemplate:
        db.add(template)
        return template
    
    async def get_all(
        self,
        db: AsyncSession,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
    ) -> list[OnboardingTemplate]:
        query = select(OnboardingTemplate).where(
            OnboardingTemplate.deleted_at.is_(None)
        )
        
        if department_id is not None:
            query = query.where(OnboardingTemplate.department_id == department_id)
            
        if is_active is not None:
            query = query.where(OnboardingTemplate.is_active == is_active)
            
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> OnboardingTemplate | None:
        result = await db.execute(
            select(OnboardingTemplate).where(
                OnboardingTemplate.id == template_id,
                OnboardingTemplate.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
    
    async def get_active_by_department(
        self, db: AsyncSession, department_id: uuid.UUID
    ) -> OnboardingTemplate | None:
        result = await db.execute(
            select(OnboardingTemplate).where(
                OnboardingTemplate.department_id == department_id,
                OnboardingTemplate.is_active.is_(True),
                OnboardingTemplate.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
    
    async def count_active_tasks(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> int:
        result = await db.execute(
            select(func.count()).where(
                TemplateTask.template_id == template_id,
                TemplateTask.deleted_at.is_(None),
            )
        )
        return result.scalar_one()