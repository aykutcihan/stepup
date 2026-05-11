from datetime import datetime, timezone
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate
from app.repositories.template_repository import TemplateRepository
from app.schemas.template import TemplateCreate, TemplateUpdate, TaskCreate, TaskUpdate
from app.errors import NotFoundError, ValidationError
from app.errors import messages
from app.models.template_task import TemplateTask
from app.repositories.template_task_repository import TemplateTaskRepository

template_repository = TemplateRepository()
template_task_repository = TemplateTaskRepository()

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
    
    async def clone_template(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> OnboardingTemplate:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        new_template = OnboardingTemplate(
            name=f"{template.name} (copy)",
            department_id=template.department_id,
            is_active=False,
        )
        await template_repository.create(db, new_template)
        await db.flush()

        tasks = await template_task_repository.get_by_template(db, template_id)
        for task in tasks:
            new_task = TemplateTask(
                template_id=new_template.id,
                title=task.title,
                description=task.description,
                order=task.order,
                deadline_days=task.deadline_days,
                is_required=task.is_required,
            )
            db.add(new_task)

        await db.commit()
        await db.refresh(new_template)
        return new_template

    async def add_task(
        self, db: AsyncSession, template_id: uuid.UUID, data: TaskCreate
    ) -> TemplateTask:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        max_order = await template_task_repository.get_max_order(db, template_id)
        task = TemplateTask(
            template_id=template_id,
            title=data.title,
            description=data.description,
            order=max_order + 1,
            deadline_days=data.deadline_days,
            is_required=data.is_required,
        )
        await template_task_repository.create(db, task)
        await db.commit()
        await db.refresh(task)
        return task

    async def update_task(
        self,
        db: AsyncSession,
        template_id: uuid.UUID,
        task_id: uuid.UUID,
        data: TaskUpdate,
    ) -> TemplateTask:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        task = await template_task_repository.get_by_id(db, task_id)
        if not task or task.template_id != template_id:
            raise NotFoundError(*messages.TASK_NOT_FOUND)

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.deadline_days is not None:
            task.deadline_days = data.deadline_days
        if data.is_required is not None:
            task.is_required = data.is_required

        await db.commit()
        await db.refresh(task)
        return task

    async def delete_task(
        self, db: AsyncSession, template_id: uuid.UUID, task_id: uuid.UUID
    ) -> None:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        task = await template_task_repository.get_by_id(db, task_id)
        if not task or task.template_id != template_id:
            raise NotFoundError(*messages.TASK_NOT_FOUND)

        task.deleted_at = datetime.now(timezone.utc)
        await db.commit()

    async def get_tasks(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> list[TemplateTask]:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)
        return await template_task_repository.get_by_template(db, template_id)

    async def reorder_task(
        self,
        db: AsyncSession,
        template_id: uuid.UUID,
        task_id: uuid.UUID,
        new_order: int,
    ) -> TemplateTask:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        tasks = await template_task_repository.get_by_template(db, template_id)
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise NotFoundError(*messages.TASK_NOT_FOUND)

        if new_order < 1 or new_order > len(tasks):
            raise ValidationError(*messages.INVALID_REORDER)

        current_order = task.order
        if new_order == current_order:
            return task

        if new_order < current_order:
            for t in tasks:
                if new_order <= t.order < current_order:
                    t.order += 1
        else:
            for t in tasks:
                if current_order < t.order <= new_order:
                    t.order -= 1

        task.order = new_order
        await db.commit()
        await db.refresh(task)
        return task

    async def delete_template(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> None:
        template = await template_repository.get_by_id(db, template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)

        template.deleted_at = datetime.now(timezone.utc)
        template.is_active = False
        await db.commit()
