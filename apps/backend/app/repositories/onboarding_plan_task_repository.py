import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask


class OnboardingPlanTaskRepository:
    async def create(self, db: AsyncSession, task: OnboardingPlanTask) -> OnboardingPlanTask:
        db.add(task)
        return task

    async def get_by_id(self, db: AsyncSession, task_id: uuid.UUID) -> OnboardingPlanTask | None:
        result = await db.execute(
            select(OnboardingPlanTask)
            .options(
                selectinload(OnboardingPlanTask.attachments),
                selectinload(OnboardingPlanTask.comments),
            )
            .where(
                OnboardingPlanTask.id == task_id,
                OnboardingPlanTask.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_max_order(self, db: AsyncSession, plan_id: uuid.UUID) -> int:
        result = await db.execute(
            select(func.max(OnboardingPlanTask.order)).where(
                OnboardingPlanTask.plan_id == plan_id,
                OnboardingPlanTask.deleted_at.is_(None),
            )
        )
        return result.scalar_one() or 0

    async def count_completed_across_active_plans(self, db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count())
            .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
            .where(
                OnboardingPlanTask.status == OnboardingPlanTaskStatus.COMPLETED,
                OnboardingPlanTask.deleted_at.is_(None),
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one()

    async def count_completed_by_manager(self, db: AsyncSession, manager_id: uuid.UUID) -> int:
        result = await db.execute(
            select(func.count())
            .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
            .where(
                OnboardingPlanTask.status == OnboardingPlanTaskStatus.COMPLETED,
                OnboardingPlanTask.deleted_at.is_(None),
                OnboardingPlan.manager_id == manager_id,
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one()
