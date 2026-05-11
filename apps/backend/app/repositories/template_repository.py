import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate

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