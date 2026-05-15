import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import NotFoundError, ValidationError
from app.services.task_workflow_service import TaskWorkflowService

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def service():
    return TaskWorkflowService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


class TestGetMyPlan:

    async def test_raises_404_when_no_active_plan(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()

        with patch("app.services.task_workflow_service.plan_repository") as mock_repo:
            mock_repo.get_active_by_user = AsyncMock(return_value=None)

            with pytest.raises(NotFoundError) as exc_info:
                await service.get_my_plan(mock_db, current_user)

            assert exc_info.value.code == "PLAN_NOT_FOUND"

    async def test_returns_plan_when_active_plan_exists(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        mock_plan = MagicMock()

        with patch("app.services.task_workflow_service.plan_repository") as mock_repo:
            mock_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            result = await service.get_my_plan(mock_db, current_user)

        assert result is mock_plan


class TestStartTask:

    async def test_transitions_not_started_to_in_progress(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.NOT_STARTED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            await service.start_task(mock_db, uuid.uuid4(), current_user)

        assert mock_task.status == OnboardingPlanTaskStatus.IN_PROGRESS

    async def test_raises_400_when_already_in_progress(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.start_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "INVALID_TASK_TRANSITION"

    async def test_raises_400_when_cancelled(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.CANCELLED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.start_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "INVALID_TASK_TRANSITION"


class TestCompleteTask:

    async def test_transitions_in_progress_to_completed(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            await service.complete_task(mock_db, uuid.uuid4(), current_user)

        assert mock_task.status == OnboardingPlanTaskStatus.COMPLETED

    async def test_raises_400_when_not_started(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.NOT_STARTED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.complete_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "INVALID_TASK_TRANSITION"

    async def test_raises_400_when_already_completed(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.COMPLETED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.complete_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "INVALID_TASK_TRANSITION"
