import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.department_service import DepartmentService
from app.errors import ValidationError

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
def service():
    return DepartmentService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    return db


class TestDeactivateDepartment:

    async def test_deactivate_raises_validation_error_when_department_has_active_users(
        self, service, mock_db
    ):
        mock_department = MagicMock()

        with patch(
            "app.services.department_service.department_repository", autospec=True
        ) as mock_dept_repo, patch(
            "app.services.department_service.user_repository", autospec=True
        ) as mock_user_repo:
            mock_dept_repo.get_by_id = AsyncMock(return_value=mock_department)
            mock_user_repo.count_active_by_department = AsyncMock(return_value=3)

            with pytest.raises(ValidationError):
                await service.deactivate_department(mock_db, MagicMock())

    async def test_deactivate_sets_is_active_false_when_no_active_users(
        self, service, mock_db
    ):
        mock_department = MagicMock()
        mock_department.is_active = True

        with patch(
            "app.services.department_service.department_repository", autospec=True
        ) as mock_dept_repo, patch(
            "app.services.department_service.user_repository", autospec=True
        ) as mock_user_repo:
            mock_dept_repo.get_by_id = AsyncMock(return_value=mock_department)
            mock_user_repo.count_active_by_department = AsyncMock(return_value=0)

            await service.deactivate_department(mock_db, MagicMock())

            assert mock_department.is_active is False


class TestAssignUserToDepartment:

    async def test_assign_department_updates_department_id(self, service, mock_db):
        import uuid
        from app.schemas.user import UserUpdate

        mock_user = MagicMock()
        department_id = uuid.uuid4()

        with patch(
            "app.services.user_service.user_repository", autospec=True
        ) as mock_user_repo:
            mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)

            from app.services.user_service import UserService
            user_service = UserService()
            await user_service.update_user(
                mock_db, mock_user.id, UserUpdate(department_id=department_id)
            )

            assert mock_user.department_id == department_id
