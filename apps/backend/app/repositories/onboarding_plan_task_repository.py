import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.onboarding_plan_task import OnboardingPlanTask


class OnboardingPlanTaskRepository:
    async def create(self, db: AsyncSession, task: OnboardingPlanTask) -> OnboardingPlanTask:
        db.add(task)
        return task

    async def get_by_id(self, db: AsyncSession, task_id: uuid.UUID) -> OnboardingPlanTask | None:
        result = await db.execute(
            select(OnboardingPlanTask).where(
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
