import logging
import uuid
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import NotFoundError, ValidationError, messages
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.repositories.onboarding_plan_repository import OnboardingPlanRepository
from app.repositories.onboarding_plan_task_repository import (
    OnboardingPlanTaskRepository,
)
from app.repositories.template_repository import TemplateRepository
from app.repositories.template_task_repository import TemplateTaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.onboarding_plan import (
    OnboardingPlanCreate,
    OnboardingPlanTaskAdd,
    OnboardingPlanTaskUpdate,
    OnboardingPlanUpdate,
)
from app.services.audit_service import AuditService
from app.services.email import EmailService

logger = logging.getLogger(__name__)

audit_service = AuditService()
email_service = EmailService()

plan_repository = OnboardingPlanRepository()
user_repository = UserRepository()
plan_task_repository = OnboardingPlanTaskRepository()
template_repository = TemplateRepository()
template_task_repository = TemplateTaskRepository()

TERMINAL_STATUSES = {OnboardingPlanTaskStatus.CANCELLED}


class OnboardingPlanService:
    async def create_plan(self, db: AsyncSession, data: OnboardingPlanCreate, actor_id: uuid.UUID | None = None) -> OnboardingPlan:
        existing = await plan_repository.get_active_by_user(db, data.user_id)
        if existing:
            raise ValidationError(*messages.EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN)

        template = await template_repository.get_by_id(db, data.template_id)
        if not template:
            raise NotFoundError(*messages.TEMPLATE_NOT_FOUND)
        if not template.is_active:
            raise ValidationError(*messages.TEMPLATE_NOT_ACTIVE)

        plan = OnboardingPlan(
            user_id=data.user_id,
            template_id=data.template_id,
            manager_id=data.manager_id,
            start_date=data.start_date,
            is_active=True,
        )
        await plan_repository.create(db, plan)
        await db.flush()

        tasks = await template_task_repository.get_by_template(db, data.template_id)
        for task in tasks:
            db.add(OnboardingPlanTask(
                plan_id=plan.id,
                template_task_id=task.id,
                title=task.title,
                description=task.description,
                deadline=data.start_date + timedelta(days=task.deadline_days),
                status=OnboardingPlanTaskStatus.NOT_STARTED,
                is_required=task.is_required,
                order=task.order,
            ))

        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.plan_created, entity_type=AuditEntityType.plan, entity_id=plan.id)
        await db.commit()
        try:
            employee = await user_repository.get_by_id(db, data.user_id)
            if employee:
                await email_service.send_plan_started_email(
                    to_email=employee.email,
                    first_name=employee.first_name,
                )
        except Exception as e:
            logger.error(f"Failed to send plan_started email: {e}")
        return await plan_repository.get_by_id(db, plan.id)

    async def get_plan(self, db: AsyncSession, plan_id: uuid.UUID) -> OnboardingPlan:
        plan = await plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)
        return plan

    async def update_plan(self, db: AsyncSession, plan_id: uuid.UUID, data: OnboardingPlanUpdate) -> OnboardingPlan:
        plan = await plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)

        if data.manager_id is not None:
            plan.manager_id = data.manager_id

        await db.commit()
        return await plan_repository.get_by_id(db, plan_id)

    async def update_task_deadline(
        self, db: AsyncSession, plan_id: uuid.UUID, task_id: uuid.UUID, data: OnboardingPlanTaskUpdate
    ) -> OnboardingPlanTask:
        plan = await plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)

        task = await plan_task_repository.get_by_id(db, task_id)
        if not task or task.plan_id != plan_id:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)

        task.deadline = data.deadline
        await db.commit()
        task = await plan_task_repository.get_by_id(db, task_id)
        return task

    async def add_task(self, db: AsyncSession, plan_id: uuid.UUID, data: OnboardingPlanTaskAdd) -> OnboardingPlanTask:
        plan = await plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)

        max_order = await plan_task_repository.get_max_order(db, plan_id)
        task = OnboardingPlanTask(
            plan_id=plan_id,
            template_task_id=None,
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            status=OnboardingPlanTaskStatus.NOT_STARTED,
            is_required=data.is_required,
            order=max_order + 1,
        )
        await plan_task_repository.create(db, task)
        await db.flush()
        await db.commit()
        task = await plan_task_repository.get_by_id(db, task.id)
        return task

    async def cancel_task(self, db: AsyncSession, plan_id: uuid.UUID, task_id: uuid.UUID, actor_id: uuid.UUID | None = None) -> OnboardingPlanTask:
        plan = await plan_repository.get_by_id(db, plan_id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)

        task = await plan_task_repository.get_by_id(db, task_id)
        if not task or task.plan_id != plan_id:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)

        if task.status in TERMINAL_STATUSES:
            raise ValidationError(*messages.TASK_ALREADY_TERMINAL)

        task.status = OnboardingPlanTaskStatus.CANCELLED
        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.plan_task_cancelled, entity_type=AuditEntityType.task, entity_id=task_id)
        await db.commit()
        task = await plan_task_repository.get_by_id(db, task_id)
        return task
