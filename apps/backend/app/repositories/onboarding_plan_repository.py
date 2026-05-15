import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask


class OnboardingPlanRepository:
    async def create(self, db: AsyncSession, plan: OnboardingPlan) -> OnboardingPlan:
        db.add(plan)
        return plan

    def _task_options(self):
        return selectinload(OnboardingPlan.tasks).options(
            selectinload(OnboardingPlanTask.attachments),
            selectinload(OnboardingPlanTask.comments),
        )

    async def get_by_id(self, db: AsyncSession, plan_id: uuid.UUID) -> OnboardingPlan | None:
        result = await db.execute(
            select(OnboardingPlan)
            .options(self._task_options())
            .where(
                OnboardingPlan.id == plan_id,
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_manager(self, db: AsyncSession, manager_id: uuid.UUID) -> list[OnboardingPlan]:
        result = await db.execute(
            select(OnboardingPlan)
            .options(self._task_options(), selectinload(OnboardingPlan.employee))
            .where(
                OnboardingPlan.manager_id == manager_id,
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def get_active_by_user(self, db: AsyncSession, user_id: uuid.UUID) -> OnboardingPlan | None:
        result = await db.execute(
            select(OnboardingPlan)
            .options(self._task_options())
            .where(
                OnboardingPlan.user_id == user_id,
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def count_active(self, db: AsyncSession) -> int:
        result = await db.execute(
            select(func.count()).where(
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one()
