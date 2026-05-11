import uuid
import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.onboarding_plan_service import OnboardingPlanService
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import ValidationError, NotFoundError

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def service():
    return OnboardingPlanService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


class TestCreatePlan:

    async def test_deadline_calculated_from_start_date(self, service, mock_db):
        start_date = date(2026, 5, 1)
        mock_template = MagicMock()
        mock_template.is_active = True

        mock_task = MagicMock()
        mock_task.deadline_days = 7

        created_tasks = []

        def capture_add(obj):
            from app.models.onboarding_plan_task import OnboardingPlanTask
            if isinstance(obj, OnboardingPlanTask):
                created_tasks.append(obj)

        mock_db.add.side_effect = capture_add

        with patch("app.services.onboarding_plan_service.plan_repository") as mock_plan_repo, \
             patch("app.services.onboarding_plan_service.template_repository") as mock_tmpl_repo, \
             patch("app.services.onboarding_plan_service.template_task_repository") as mock_task_repo:

            mock_plan_repo.get_active_by_user = AsyncMock(return_value=None)
            mock_plan_repo.create = AsyncMock()
            mock_plan_repo.get_by_id = AsyncMock(return_value=MagicMock())
            mock_tmpl_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_by_template = AsyncMock(return_value=[mock_task])

            from app.schemas.onboarding_plan import OnboardingPlanCreate
            data = OnboardingPlanCreate(
                user_id=uuid.uuid4(),
                template_id=uuid.uuid4(),
                manager_id=uuid.uuid4(),
                start_date=start_date,
            )
            await service.create_plan(mock_db, data)

        assert len(created_tasks) == 1
        assert created_tasks[0].deadline == date(2026, 5, 8)

    async def test_raises_validation_error_when_employee_already_has_active_plan(
        self, service, mock_db
    ):
        with patch("app.services.onboarding_plan_service.plan_repository") as mock_plan_repo:
            mock_plan_repo.get_active_by_user = AsyncMock(return_value=MagicMock())

            from app.schemas.onboarding_plan import OnboardingPlanCreate
            data = OnboardingPlanCreate(
                user_id=uuid.uuid4(),
                template_id=uuid.uuid4(),
                manager_id=uuid.uuid4(),
                start_date=date(2026, 5, 1),
            )

            with pytest.raises(ValidationError) as exc_info:
                await service.create_plan(mock_db, data)

            assert exc_info.value.code == "EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN"

    async def test_raises_validation_error_when_template_is_not_active(
        self, service, mock_db
    ):
        mock_template = MagicMock()
        mock_template.is_active = False

        with patch("app.services.onboarding_plan_service.plan_repository") as mock_plan_repo, \
             patch("app.services.onboarding_plan_service.template_repository") as mock_tmpl_repo:

            mock_plan_repo.get_active_by_user = AsyncMock(return_value=None)
            mock_tmpl_repo.get_by_id = AsyncMock(return_value=mock_template)

            from app.schemas.onboarding_plan import OnboardingPlanCreate
            data = OnboardingPlanCreate(
                user_id=uuid.uuid4(),
                template_id=uuid.uuid4(),
                manager_id=uuid.uuid4(),
                start_date=date(2026, 5, 1),
            )

            with pytest.raises(ValidationError) as exc_info:
                await service.create_plan(mock_db, data)

            assert exc_info.value.code == "TEMPLATE_NOT_ACTIVE"


class TestCancelTask:

    async def test_sets_task_status_to_cancelled(self, service, mock_db):
        plan_id = uuid.uuid4()
        task_id = uuid.uuid4()

        mock_plan = MagicMock()
        mock_task = MagicMock()
        mock_task.plan_id = plan_id
        mock_task.status = OnboardingPlanTaskStatus.NOT_STARTED

        with patch("app.services.onboarding_plan_service.plan_repository") as mock_plan_repo, \
             patch("app.services.onboarding_plan_service.plan_task_repository") as mock_task_repo:

            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)
            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)

            await service.cancel_task(mock_db, plan_id, task_id)

        assert mock_task.status == OnboardingPlanTaskStatus.CANCELLED

    async def test_raises_validation_error_when_task_already_cancelled(
        self, service, mock_db
    ):
        plan_id = uuid.uuid4()
        task_id = uuid.uuid4()

        mock_plan = MagicMock()
        mock_task = MagicMock()
        mock_task.plan_id = plan_id
        mock_task.status = OnboardingPlanTaskStatus.CANCELLED

        with patch("app.services.onboarding_plan_service.plan_repository") as mock_plan_repo, \
             patch("app.services.onboarding_plan_service.plan_task_repository") as mock_task_repo:

            mock_plan_repo.get_by_id = AsyncMock(return_value=mock_plan)
            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)

            with pytest.raises(ValidationError) as exc_info:
                await service.cancel_task(mock_db, plan_id, task_id)

            assert exc_info.value.code == "TASK_ALREADY_TERMINAL"
