import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import NotFoundError, ValidationError
from app.errors import messages
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.user import User
from app.repositories.onboarding_plan_repository import OnboardingPlanRepository
from app.repositories.onboarding_plan_task_repository import OnboardingPlanTaskRepository

plan_repository = OnboardingPlanRepository()
plan_task_repository = OnboardingPlanTaskRepository()

VALID_TRANSITIONS = {
    OnboardingPlanTaskStatus.NOT_STARTED: OnboardingPlanTaskStatus.IN_PROGRESS,
    OnboardingPlanTaskStatus.IN_PROGRESS: OnboardingPlanTaskStatus.COMPLETED,
}


class TaskWorkflowService:
    async def get_my_plan(self, db: AsyncSession, current_user: User) -> OnboardingPlan:
        plan = await plan_repository.get_active_by_user(db, current_user.id)
        if not plan:
            raise NotFoundError(*messages.PLAN_NOT_FOUND)
        return plan

    async def start_task(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User
    ) -> OnboardingPlanTask:
        task = await self._get_task_for_user(db, task_id, current_user)
        self._assert_transition(task, OnboardingPlanTaskStatus.IN_PROGRESS)
        task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        await db.commit()
        await db.refresh(task)
        return task

    async def complete_task(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User
    ) -> OnboardingPlanTask:
        task = await self._get_task_for_user(db, task_id, current_user)
        self._assert_transition(task, OnboardingPlanTaskStatus.COMPLETED)
        task.status = OnboardingPlanTaskStatus.COMPLETED
        await db.commit()
        await db.refresh(task)
        return task

    async def _get_task_for_user(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User
    ) -> OnboardingPlanTask:
        task = await plan_task_repository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
        plan = await plan_repository.get_active_by_user(db, current_user.id)
        if not plan or task.plan_id != plan.id:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
        return task

    def _assert_transition(
        self, task: OnboardingPlanTask, target: OnboardingPlanTaskStatus
    ) -> None:
        if VALID_TRANSITIONS.get(task.status) != target:
            raise ValidationError(*messages.INVALID_TASK_TRANSITION)
