from datetime import date
from sqlalchemy import func, case, and_, cast
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.models.department import Department
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.onboarding_template import OnboardingTemplate
from app.models.user import User

_TERMINAL = [
    OnboardingPlanTaskStatus.COMPLETED,
    OnboardingPlanTaskStatus.APPROVED,
    OnboardingPlanTaskStatus.CANCELLED,
]


class ReportsRepository:

    async def get_completion_time_by_department(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        # Subquery: last approval timestamp per plan (= plan completion moment)
        last_approval = (
            select(
                OnboardingPlanTask.plan_id,
                func.max(OnboardingPlanTask.updated_at).label("completed_at"),
            )
            .where(OnboardingPlanTask.status == OnboardingPlanTaskStatus.APPROVED)
            .group_by(OnboardingPlanTask.plan_id)
            .subquery()
        )

        days_expr = (
            func.extract(
                "epoch",
                last_approval.c.completed_at - cast(OnboardingPlan.start_date, TIMESTAMP),
            )
            / 86400
        )

        query = (
            select(
                Department.name.label("department_name"),
                func.count(OnboardingPlan.id.distinct()).label("total_plans"),
                func.avg(days_expr).label("avg_completion_days"),
            )
            .join(last_approval, OnboardingPlan.id == last_approval.c.plan_id)
            .join(User, OnboardingPlan.user_id == User.id)
            .join(Department, User.department_id == Department.id)
        )

        if start_date:
            query = query.where(OnboardingPlan.start_date >= start_date)
        if end_date:
            query = query.where(OnboardingPlan.start_date <= end_date)

        query = query.group_by(Department.name).order_by(Department.name)
        result = await db.execute(query)
        return [dict(row._mapping) for row in result.all()]

    async def get_task_completion_rates(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        done_statuses = [OnboardingPlanTaskStatus.COMPLETED, OnboardingPlanTaskStatus.APPROVED]
        done_case = case(
            (OnboardingPlanTask.status.in_(done_statuses), 1),
            else_=0,
        )

        query = (
            select(
                OnboardingTemplate.name.label("template_name"),
                func.count(OnboardingPlanTask.id).label("total_tasks"),
                func.sum(done_case).label("completed_tasks"),
            )
            .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
            .join(OnboardingTemplate, OnboardingPlan.template_id == OnboardingTemplate.id)
        )

        if start_date:
            query = query.where(OnboardingPlan.start_date >= start_date)
        if end_date:
            query = query.where(OnboardingPlan.start_date <= end_date)

        query = query.group_by(OnboardingTemplate.name).order_by(OnboardingTemplate.name)
        result = await db.execute(query)
        return [dict(row._mapping) for row in result.all()]

    async def get_bottlenecks(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        today = date.today()

        returned_case = case(
            (OnboardingPlanTask.status == OnboardingPlanTaskStatus.RETURNED, 1),
            else_=0,
        )
        overdue_case = case(
            (
                and_(
                    OnboardingPlanTask.deadline < today,
                    OnboardingPlanTask.status.notin_(_TERMINAL),
                ),
                1,
            ),
            else_=0,
        )

        total_expr = func.sum(returned_case) + func.sum(overdue_case)

        query = (
            select(
                OnboardingPlanTask.title.label("task_title"),
                func.sum(returned_case).label("returned_count"),
                func.sum(overdue_case).label("overdue_count"),
            )
            .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
        )

        if start_date:
            query = query.where(OnboardingPlan.start_date >= start_date)
        if end_date:
            query = query.where(OnboardingPlan.start_date <= end_date)

        query = (
            query.group_by(OnboardingPlanTask.title)
            .having(total_expr > 0)
            .order_by(total_expr.desc())
            .limit(20)
        )

        result = await db.execute(query)
        return [dict(row._mapping) for row in result.all()]
