import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.repositories.department_repository import DepartmentRepository
from app.repositories.onboarding_plan_repository import OnboardingPlanRepository
from app.repositories.onboarding_plan_task_repository import (
    OnboardingPlanTaskRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import (
    EmployeeDashboardResponse,
    HRDashboardResponse,
    ManagerDashboardResponse,
)

user_repository = UserRepository()
plan_repository = OnboardingPlanRepository()
plan_task_repository = OnboardingPlanTaskRepository()
department_repository = DepartmentRepository()


class DashboardService:

    async def get_hr_stats(self, db: AsyncSession) -> HRDashboardResponse:
        active_users = await user_repository.count_active(db)
        active_plans = await plan_repository.count_active(db)
        active_departments = await department_repository.count_active(db)
        pending_approvals = await plan_task_repository.count_completed_across_active_plans(db)

        return HRDashboardResponse(
            active_users=active_users,
            active_plans=active_plans,
            active_departments=active_departments,
            pending_approvals=pending_approvals,
        )

    async def get_manager_stats(self, db: AsyncSession, manager_id: uuid.UUID) -> ManagerDashboardResponse:
        plans = await plan_repository.get_all_by_manager(db, manager_id)
        pending_approvals = await plan_task_repository.count_completed_by_manager(db, manager_id)

        return ManagerDashboardResponse(
            active_plans=len(plans),
            pending_approvals=pending_approvals,
            total_employees=len({p.user_id for p in plans}),
        )

    async def get_employee_stats(self, db: AsyncSession, user_id: uuid.UUID) -> EmployeeDashboardResponse:
        plan = await plan_repository.get_active_by_user(db, user_id)

        if not plan:
            return EmployeeDashboardResponse(
                total_tasks=0,
                approved_tasks=0,
                completed_tasks=0,
                in_progress_tasks=0,
                next_deadline=None,
            )

        active_tasks = [t for t in plan.tasks if t.deleted_at is None]

        approved = sum(1 for t in active_tasks if t.status == OnboardingPlanTaskStatus.APPROVED)
        completed = sum(1 for t in active_tasks if t.status == OnboardingPlanTaskStatus.COMPLETED)
        in_progress = sum(1 for t in active_tasks if t.status == OnboardingPlanTaskStatus.IN_PROGRESS)

        pending_deadlines: list[date] = [
            t.deadline for t in active_tasks
            if t.status not in (OnboardingPlanTaskStatus.APPROVED, OnboardingPlanTaskStatus.CANCELLED)
        ]
        next_deadline = min(pending_deadlines) if pending_deadlines else None

        return EmployeeDashboardResponse(
            total_tasks=len(active_tasks),
            approved_tasks=approved,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            next_deadline=next_deadline,
        )
