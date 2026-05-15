import logging
from datetime import date, timedelta

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload, sessionmaker

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.user import User
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)
email_service = EmailService()

_OVERDUEABLE = [OnboardingPlanTaskStatus.NOT_STARTED, OnboardingPlanTaskStatus.IN_PROGRESS]
_REMINDABLE = [
    OnboardingPlanTaskStatus.NOT_STARTED,
    OnboardingPlanTaskStatus.IN_PROGRESS,
    OnboardingPlanTaskStatus.OVERDUE,
]


async def mark_overdue_tasks(session_factory: sessionmaker) -> None:
    today = date.today()
    processed = 0
    emails_sent = 0
    errors = 0

    async with session_factory() as db:
        try:
            result = await db.execute(
                select(OnboardingPlanTask)
                .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
                .where(
                    and_(
                        OnboardingPlanTask.deadline < today,
                        OnboardingPlanTask.status.in_(_OVERDUEABLE),
                        OnboardingPlanTask.deleted_at.is_(None),
                        OnboardingPlan.is_active.is_(True),
                        OnboardingPlan.deleted_at.is_(None),
                    )
                )
                .options(selectinload(OnboardingPlanTask.plan))
            )
            tasks = list(result.scalars().unique().all())

            for task in tasks:
                try:
                    task.status = OnboardingPlanTaskStatus.OVERDUE
                    processed += 1
                    plan = task.plan

                    emp_row = await db.execute(select(User).where(User.id == plan.user_id))
                    employee = emp_row.scalar_one_or_none()

                    mgr_row = await db.execute(select(User).where(User.id == plan.manager_id))
                    manager = mgr_row.scalar_one_or_none()

                    deadline_str = task.deadline.isoformat()

                    if employee:
                        try:
                            await email_service.send_task_overdue_email(
                                to_email=employee.email,
                                first_name=employee.first_name,
                                task_title=task.title,
                                deadline=deadline_str,
                            )
                            emails_sent += 1
                        except Exception as e:
                            logger.error(f"Overdue email to employee failed: {e}")
                            errors += 1

                    if manager and employee:
                        try:
                            await email_service.send_task_overdue_manager_email(
                                to_email=manager.email,
                                manager_first_name=manager.first_name,
                                employee_name=f"{employee.first_name} {employee.last_name}",
                                task_title=task.title,
                                deadline=deadline_str,
                            )
                            emails_sent += 1
                        except Exception as e:
                            logger.error(f"Overdue email to manager failed: {e}")
                            errors += 1

                except Exception as e:
                    logger.error(f"Failed processing task {task.id}: {e}")
                    errors += 1

            await db.commit()

        except Exception as e:
            logger.error(f"mark_overdue_tasks job failed: {e}")
            await db.rollback()
            return

    logger.info(
        f"mark_overdue_tasks — tasks_marked={processed}, emails_sent={emails_sent}, errors={errors}"
    )


async def send_deadline_reminders(session_factory: sessionmaker) -> None:
    reminder_date = date.today() + timedelta(days=2)
    emails_sent = 0
    errors = 0

    async with session_factory() as db:
        try:
            result = await db.execute(
                select(OnboardingPlanTask)
                .join(OnboardingPlan, OnboardingPlanTask.plan_id == OnboardingPlan.id)
                .where(
                    and_(
                        OnboardingPlanTask.deadline == reminder_date,
                        OnboardingPlanTask.status.in_(_REMINDABLE),
                        OnboardingPlanTask.deleted_at.is_(None),
                        OnboardingPlan.is_active.is_(True),
                        OnboardingPlan.deleted_at.is_(None),
                    )
                )
                .options(selectinload(OnboardingPlanTask.plan))
            )
            tasks = list(result.scalars().unique().all())

            for task in tasks:
                try:
                    plan = task.plan
                    emp_row = await db.execute(select(User).where(User.id == plan.user_id))
                    employee = emp_row.scalar_one_or_none()

                    if employee:
                        await email_service.send_deadline_reminder_email(
                            to_email=employee.email,
                            first_name=employee.first_name,
                            task_title=task.title,
                            deadline=task.deadline.isoformat(),
                        )
                        emails_sent += 1

                except Exception as e:
                    logger.error(f"Reminder email failed for task {task.id}: {e}")
                    errors += 1

        except Exception as e:
            logger.error(f"send_deadline_reminders job failed: {e}")
            return

    logger.info(f"send_deadline_reminders — emails_sent={emails_sent}, errors={errors}")
