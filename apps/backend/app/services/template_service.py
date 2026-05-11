import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate
from app.repositories.template_repository import TemplateRepository
from app.schemas.template import TemplateCreate

template_repository = TemplateRepository()

class TemplateService:
    async def create_template(
        self, db: AsyncSession, data: TemplateCreate
    ) -> OnboardingTemplate:
        template = OnboardingTemplate(
            name=data.name,
            department_id=data.department_id,
            is_active=False,
        )
        await template_repository.create(db, template)
        await db.commit()  
        await db.refresh(template) 
        return template
    
    async def get_all_templates(
        self,
        db: AsyncSession,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
    ) -> list[OnboardingTemplate]:
        return await template_repository.get_all(db, department_id, is_active)