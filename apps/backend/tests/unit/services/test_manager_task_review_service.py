import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.task_workflow_service import TaskWorkflowService
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import ValidationError, NotFoundError
from app.schemas.onboarding_plan import ReturnTask

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def service():
    return TaskWorkflowService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    return db


class TestApproveTask:

    async def test_transitions_completed_to_approved(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.COMPLETED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            await service.approve_task(mock_db, uuid.uuid4(), current_user)

        assert mock_task.status == OnboardingPlanTaskStatus.APPROVED

    async def test_raises_400_when_not_completed(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.approve_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "TASK_NOT_APPROVABLE"

    async def test_raises_400_when_already_approved(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.APPROVED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.approve_task(mock_db, uuid.uuid4(), current_user)

            assert exc_info.value.code == "TASK_NOT_APPROVABLE"


class TestReturnTask:

    async def test_transitions_completed_to_in_progress(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.COMPLETED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            await service.return_task(mock_db, uuid.uuid4(), current_user, ReturnTask(content="Please redo"))

        assert mock_task.status == OnboardingPlanTaskStatus.IN_PROGRESS

    async def test_raises_400_when_content_is_empty(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.COMPLETED
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.return_task(mock_db, uuid.uuid4(), current_user, ReturnTask(content="   "))

            assert exc_info.value.code == "RETURN_COMMENT_REQUIRED"

    async def test_raises_400_when_not_completed(self, service, mock_db):
        current_user = MagicMock()
        current_user.id = uuid.uuid4()
        plan_id = uuid.uuid4()

        mock_task = MagicMock()
        mock_task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        mock_task.plan_id = plan_id

        mock_plan = MagicMock()
        mock_plan.id = plan_id
        mock_plan.manager_id = current_user.id

        with patch("app.services.task_workflow_service.plan_task_repository") as mock_task_repo, \
             patch("app.services.task_workflow_service.plan_repository") as mock_plan_repo:

            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)
            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)

            with pytest.raises(ValidationError) as exc_info:
                await service.return_task(mock_db, uuid.uuid4(), current_user, ReturnTask(content="feedback"))

            assert exc_info.value.code == "TASK_NOT_APPROVABLE"
