from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.dependencies import get_current_user, require_role
from app.enums.user_role import UserRole
from app.errors import AuthenticationError, PermissionError


@pytest.fixture
def mock_db():
    db = AsyncMock()
    return db


class TestRequireRole:

    async def test_require_role_returns_user_when_role_matches(self, mock_db):
        mock_user = MagicMock()
        mock_user.role = UserRole.HR_ADMIN
        mock_user.is_active = True

        with patch(
            "app.core.dependencies.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.core.dependencies.decode_access_token",
            return_value=mock_user.id,
        ):
            mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
            checker = require_role(UserRole.HR_ADMIN)
            result = await checker(current_user=mock_user)

            assert result == mock_user

    async def test_require_role_raises_permission_error_when_role_does_not_match(self, mock_db):
        mock_user = MagicMock()
        mock_user.role = UserRole.EMPLOYEE

        checker = require_role(UserRole.HR_ADMIN)

        with pytest.raises(PermissionError):
            await checker(current_user=mock_user)


class TestGetCurrentUser:

    async def test_get_current_user_raises_error_when_user_is_inactive(self, mock_db):
        mock_user = MagicMock()
        mock_user.is_active = False
        mock_request = MagicMock()
        mock_request.cookies.get = MagicMock(return_value="valid-token")

        with patch(
            "app.core.dependencies.decode_access_token",
            return_value=mock_user.id,
        ), patch(
            "app.core.dependencies.user_repository",
            autospec=True,
        ) as mock_user_repo:

            mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)

            with pytest.raises(AuthenticationError):
                await get_current_user(request=mock_request, db=mock_db)
