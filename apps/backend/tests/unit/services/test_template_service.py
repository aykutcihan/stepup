import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.template_service import TemplateService
from app.errors import ValidationError, NotFoundError

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def service():
    return TemplateService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


class TestActivateTemplate:

    async def test_activate_raises_validation_error_when_no_tasks(
        self, service, mock_db
    ):
        mock_template = MagicMock()
        mock_template.department_id = uuid.uuid4()

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_repo.count_active_tasks = AsyncMock(return_value=0)

            with pytest.raises(ValidationError):
                await service.activate_template(mock_db, uuid.uuid4())

    async def test_activate_deactivates_previous_active_template(
        self, service, mock_db
    ):
        template_id = uuid.uuid4()
        department_id = uuid.uuid4()

        mock_template = MagicMock()
        mock_template.id = template_id
        mock_template.department_id = department_id

        mock_previous = MagicMock()
        mock_previous.id = uuid.uuid4()
        mock_previous.is_active = True

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_repo.count_active_tasks = AsyncMock(return_value=2)
            mock_repo.get_active_by_department = AsyncMock(return_value=mock_previous)

            await service.activate_template(mock_db, template_id)

            assert mock_previous.is_active is False
            assert mock_template.is_active is True


class TestAddTask:

    async def test_add_task_raises_not_found_when_template_not_found(
        self, service, mock_db
    ):
        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=None)

            with pytest.raises(NotFoundError):
                await service.add_task(mock_db, uuid.uuid4(), MagicMock())

    async def test_add_task_assigns_next_order(self, service, mock_db):
        mock_template = MagicMock()
        mock_data = MagicMock()
        mock_data.title = "New Task"
        mock_data.description = None
        mock_data.deadline_days = 3
        mock_data.is_required = True

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_max_order = AsyncMock(return_value=2)
            mock_task_repo.create = AsyncMock()

            await service.add_task(mock_db, uuid.uuid4(), mock_data)

            created_task = mock_task_repo.create.call_args[0][1]
            assert created_task.order == 3


class TestUpdateTask:

    async def test_update_task_raises_not_found_when_task_not_found(
        self, service, mock_db
    ):
        mock_template = MagicMock()
        template_id = uuid.uuid4()

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_by_id = AsyncMock(return_value=None)

            with pytest.raises(NotFoundError):
                await service.update_task(mock_db, template_id, uuid.uuid4(), MagicMock())


class TestDeleteTask:

    async def test_delete_task_sets_deleted_at(self, service, mock_db):
        template_id = uuid.uuid4()
        mock_template = MagicMock()
        mock_task = MagicMock()
        mock_task.template_id = template_id
        mock_task.deleted_at = None

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_by_id = AsyncMock(return_value=mock_task)

            await service.delete_task(mock_db, template_id, uuid.uuid4())

            assert mock_task.deleted_at is not None


class TestReorderTask:

    async def test_reorder_task_shifts_tasks_correctly(self, service, mock_db):
        template_id = uuid.uuid4()
        task_id = uuid.uuid4()
        mock_template = MagicMock()

        task_1 = MagicMock()
        task_1.id = uuid.uuid4()
        task_1.order = 1

        task_2 = MagicMock()
        task_2.id = task_id
        task_2.order = 2

        task_3 = MagicMock()
        task_3.id = uuid.uuid4()
        task_3.order = 3

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_by_template = AsyncMock(
                return_value=[task_1, task_2, task_3]
            )

            await service.reorder_task(mock_db, template_id, task_id, new_order=1)

            assert task_2.order == 1
            assert task_1.order == 2

    async def test_reorder_task_raises_validation_error_when_order_out_of_range(
        self, service, mock_db
    ):
        template_id = uuid.uuid4()
        task_id = uuid.uuid4()
        mock_template = MagicMock()
        mock_task = MagicMock()
        mock_task.id = task_id
        mock_task.order = 1

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_task_repo.get_by_template = AsyncMock(return_value=[mock_task])

            with pytest.raises(ValidationError):
                await service.reorder_task(mock_db, template_id, task_id, new_order=99)


class TestCloneTemplate:

    async def test_clone_copies_all_tasks(self, service, mock_db):
        template_id = uuid.uuid4()

        mock_template = MagicMock()
        mock_template.id = template_id
        mock_template.name = "Engineering Onboarding"
        mock_template.department_id = uuid.uuid4()

        mock_task_1 = MagicMock()
        mock_task_1.title = "Sign contract"
        mock_task_1.description = "Sign the employment contract"
        mock_task_1.order = 1
        mock_task_1.deadline_days = 1
        mock_task_1.is_required = True

        mock_task_2 = MagicMock()
        mock_task_2.title = "Setup laptop"
        mock_task_2.description = None
        mock_task_2.order = 2
        mock_task_2.deadline_days = 3
        mock_task_2.is_required = True

        with patch(
            "app.services.template_service.template_repository", autospec=True
        ) as mock_repo, patch(
            "app.services.template_service.template_task_repository", autospec=True
        ) as mock_task_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_template)
            mock_repo.create = AsyncMock()
            mock_task_repo.get_by_template = AsyncMock(
                return_value=[mock_task_1, mock_task_2]
            )

            await service.clone_template(mock_db, template_id)

            assert mock_db.add.call_count == 2
