import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate
from app.repositories.template_repository import TemplateRepository
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.errors import NotFoundError, ValidationError
from app.errors import messages

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
    
    
    async def update_template(
        self, db: AsyncSession, template_id: uuid.UUID, data: TemplateUpdate
    ) -> OnboardingTemplate:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        if data.name is not None:
            template.name = data.name
        if data.department_id is not None:
            template.department_id = data.department_id

        await db.commit()
        await db.refresh(template)
        return template
    
    async def activate_template(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> OnboardingTemplate:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        task_count = await template_repository.count_active_tasks(db, template_id)
        if task_count == 0:
            raise ValidationError(*messages.TEMPLATE_NO_TASKS)

        current_active = await template_repository.get_active_by_department(
            db, template.department_id
        )
        if current_active and current_active.id != template_id:
            current_active.is_active = False

        template.is_active = True
        await db.commit()
        await db.refresh(template)
        return template
    
    async def deactivate_template(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> OnboardingTemplate:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        template.is_active = False
        await db.commit()
        await db.refresh(template)
        return template