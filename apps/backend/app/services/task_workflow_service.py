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
from app.schemas.onboarding_plan import ApprovalTaskResponse, ReturnTask

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

    async def get_pending_approvals(
        self, db: AsyncSession, current_user: User
    ) -> list[ApprovalTaskResponse]:
        plans = await plan_repository.get_all_by_manager(db, current_user.id)
        result = []
        for plan in plans:
            for task in plan.tasks:
                if task.status == OnboardingPlanTaskStatus.COMPLETED and task.deleted_at is None:
                    result.append(ApprovalTaskResponse(
                        id=task.id,
                        plan_id=task.plan_id,
                        title=task.title,
                        description=task.description,
                        deadline=task.deadline,
                        status=task.status,
                        is_required=task.is_required,
                        order=task.order,
                        created_at=task.created_at,
                        employee_name=f"{plan.employee.first_name} {plan.employee.last_name}",
                        plan_start_date=plan.start_date,
                    ))
        return result

    async def approve_task(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User
    ) -> OnboardingPlanTask:
        task = await self._get_task_for_manager(db, task_id, current_user)
        if task.status != OnboardingPlanTaskStatus.COMPLETED:
            raise ValidationError(*messages.TASK_NOT_APPROVABLE)
        task.status = OnboardingPlanTaskStatus.APPROVED
        await db.commit()
        await db.refresh(task)
        return task

    async def return_task(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User, data: ReturnTask
    ) -> OnboardingPlanTask:
        task = await self._get_task_for_manager(db, task_id, current_user)
        if task.status != OnboardingPlanTaskStatus.COMPLETED:
            raise ValidationError(*messages.TASK_NOT_APPROVABLE)
        if not data.content or not data.content.strip():
            raise ValidationError(*messages.RETURN_COMMENT_REQUIRED)
        task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        await db.commit()
        await db.refresh(task)
        return task

    async def _get_task_for_manager(
        self, db: AsyncSession, task_id: uuid.UUID, current_user: User
    ) -> OnboardingPlanTask:
        task = await plan_task_repository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
        plan = await plan_repository.get_by_id(db, task.plan_id)
        if not plan or plan.manager_id != current_user.id:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
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
