import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.onboarding_plan import OnboardingPlan


class OnboardingPlanRepository:
    async def create(self, db: AsyncSession, plan: OnboardingPlan) -> OnboardingPlan:
        db.add(plan)
        return plan

    async def get_by_id(self, db: AsyncSession, plan_id: uuid.UUID) -> OnboardingPlan | None:
        result = await db.execute(
            select(OnboardingPlan)
            .options(selectinload(OnboardingPlan.tasks))
            .where(
                OnboardingPlan.id == plan_id,
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_active_by_user(self, db: AsyncSession, user_id: uuid.UUID) -> OnboardingPlan | None:
        result = await db.execute(
            select(OnboardingPlan).where(
                OnboardingPlan.user_id == user_id,
                OnboardingPlan.is_active.is_(True),
                OnboardingPlan.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
