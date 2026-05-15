import uuid
from datetime import date, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.services.scheduler_service import mark_overdue_tasks, send_deadline_reminders

pytestmark = pytest.mark.asyncio(loop_scope="session")


def _make_task(status, deadline, plan_user_id=None, plan_manager_id=None):
    task = MagicMock()
    task.id = uuid.uuid4()
    task.title = "Test Task"
    task.status = status
    task.deadline = deadline
    task.deleted_at = None
    plan = MagicMock()
    plan.user_id = plan_user_id or uuid.uuid4()
    plan.manager_id = plan_manager_id or uuid.uuid4()
    task.plan = plan
    return task


def _make_session_factory(tasks):
    session = AsyncMock()

    execute_result = MagicMock()
    execute_result.scalars.return_value.unique.return_value.all.return_value = tasks

    user = MagicMock()
    user.email = "test@example.com"
    user.first_name = "Test"
    user.last_name = "User"
    user_result = MagicMock()
    user_result.scalar_one_or_none.return_value = user

    session.execute = AsyncMock(side_effect=[execute_result, user_result, user_result] * (len(tasks) + 1))
    session.commit = AsyncMock()
    session.rollback = AsyncMock()

    factory = MagicMock()
    factory.return_value.__aenter__ = AsyncMock(return_value=session)
    factory.return_value.__aexit__ = AsyncMock(return_value=False)
    return factory, session


class TestMarkOverdueTasks:

    async def test_marks_not_started_task_as_overdue(self):
        yesterday = date.today() - timedelta(days=1)
        task = _make_task(OnboardingPlanTaskStatus.NOT_STARTED, yesterday)
        factory, session = _make_session_factory([task])

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_task_overdue_email = AsyncMock()
            mock_email.send_task_overdue_manager_email = AsyncMock()
            await mark_overdue_tasks(factory)

        assert task.status == OnboardingPlanTaskStatus.OVERDUE

    async def test_marks_in_progress_task_as_overdue(self):
        yesterday = date.today() - timedelta(days=1)
        task = _make_task(OnboardingPlanTaskStatus.IN_PROGRESS, yesterday)
        factory, session = _make_session_factory([task])

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_task_overdue_email = AsyncMock()
            mock_email.send_task_overdue_manager_email = AsyncMock()
            await mark_overdue_tasks(factory)

        assert task.status == OnboardingPlanTaskStatus.OVERDUE

    async def test_does_not_mark_completed_task_overdue(self):
        yesterday = date.today() - timedelta(days=1)
        task = _make_task(OnboardingPlanTaskStatus.COMPLETED, yesterday)

        session = AsyncMock()
        execute_result = MagicMock()
        execute_result.scalars.return_value.unique.return_value.all.return_value = []
        session.execute = AsyncMock(return_value=execute_result)
        session.commit = AsyncMock()

        factory = MagicMock()
        factory.return_value.__aenter__ = AsyncMock(return_value=session)
        factory.return_value.__aexit__ = AsyncMock(return_value=False)

        await mark_overdue_tasks(factory)
        assert task.status == OnboardingPlanTaskStatus.COMPLETED

    async def test_does_not_mark_approved_task_overdue(self):
        yesterday = date.today() - timedelta(days=1)
        task = _make_task(OnboardingPlanTaskStatus.APPROVED, yesterday)

        session = AsyncMock()
        execute_result = MagicMock()
        execute_result.scalars.return_value.unique.return_value.all.return_value = []
        session.execute = AsyncMock(return_value=execute_result)
        session.commit = AsyncMock()

        factory = MagicMock()
        factory.return_value.__aenter__ = AsyncMock(return_value=session)
        factory.return_value.__aexit__ = AsyncMock(return_value=False)

        await mark_overdue_tasks(factory)
        assert task.status == OnboardingPlanTaskStatus.APPROVED

    async def test_commits_after_marking(self):
        yesterday = date.today() - timedelta(days=1)
        task = _make_task(OnboardingPlanTaskStatus.NOT_STARTED, yesterday)
        factory, session = _make_session_factory([task])

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_task_overdue_email = AsyncMock()
            mock_email.send_task_overdue_manager_email = AsyncMock()
            await mark_overdue_tasks(factory)

        session.commit.assert_called_once()

    async def test_no_tasks_still_commits(self):
        session = AsyncMock()
        execute_result = MagicMock()
        execute_result.scalars.return_value.unique.return_value.all.return_value = []
        session.execute = AsyncMock(return_value=execute_result)
        session.commit = AsyncMock()

        factory = MagicMock()
        factory.return_value.__aenter__ = AsyncMock(return_value=session)
        factory.return_value.__aexit__ = AsyncMock(return_value=False)

        await mark_overdue_tasks(factory)
        session.commit.assert_called_once()


class TestSendDeadlineReminders:

    async def test_sends_reminder_for_task_due_in_two_days(self):
        in_two_days = date.today() + timedelta(days=2)
        task = _make_task(OnboardingPlanTaskStatus.NOT_STARTED, in_two_days)
        task.deadline = in_two_days
        factory, session = _make_session_factory([task])

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_deadline_reminder_email = AsyncMock()
            await send_deadline_reminders(factory)

        mock_email.send_deadline_reminder_email.assert_called_once()

    async def test_sends_reminder_for_overdue_task_due_in_two_days(self):
        in_two_days = date.today() + timedelta(days=2)
        task = _make_task(OnboardingPlanTaskStatus.OVERDUE, in_two_days)
        task.deadline = in_two_days
        factory, session = _make_session_factory([task])

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_deadline_reminder_email = AsyncMock()
            await send_deadline_reminders(factory)

        mock_email.send_deadline_reminder_email.assert_called_once()

    async def test_no_tasks_no_emails_sent(self):
        session = AsyncMock()
        execute_result = MagicMock()
        execute_result.scalars.return_value.unique.return_value.all.return_value = []
        session.execute = AsyncMock(return_value=execute_result)

        factory = MagicMock()
        factory.return_value.__aenter__ = AsyncMock(return_value=session)
        factory.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("app.services.scheduler_service.email_service") as mock_email:
            mock_email.send_deadline_reminder_email = AsyncMock()
            await send_deadline_reminders(factory)

        mock_email.send_deadline_reminder_email.assert_not_called()
