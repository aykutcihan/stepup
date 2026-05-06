import uuid

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.user_service import UserService
from app.errors import NotFoundError, ValidationError


@pytest.fixture
def service():
    return UserService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    return db


class TestDeactivateUser:

    async def test_deactivate_user_deactivates_when_id_is_valid(
        self, service, mock_db
    ):
        user_id = uuid.uuid4()
        current_user_id = uuid.uuid4()
        mock_user = MagicMock()

        with patch(
            "app.services.user_service.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.services.user_service.refresh_token_repository",
            autospec=True,
        ) as mock_rt_repo:

            mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
            mock_rt_repo.delete_by_user_id = AsyncMock()

            await service.deactivate_user(mock_db, user_id, current_user_id)

            assert mock_user.is_active is False

    async def test_deactivate_user_raises_error_when_deactivating_self(
        self, service, mock_db
    ):
        user_id = uuid.uuid4()

        with pytest.raises(ValidationError):
            await service.deactivate_user(mock_db, user_id, user_id)

    async def test_deactivate_user_raises_error_when_user_not_found(
        self, service, mock_db
    ):
        user_id = uuid.uuid4()
        current_user_id = uuid.uuid4()

        with patch(
            "app.services.user_service.user_repository",
            autospec=True,
        ) as mock_user_repo:

            mock_user_repo.get_by_id = AsyncMock(return_value=None)

            with pytest.raises(NotFoundError):
                await service.deactivate_user(mock_db, user_id, current_user_id)
