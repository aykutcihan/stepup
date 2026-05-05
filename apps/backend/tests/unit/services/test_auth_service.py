import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.auth_service import AuthService
from app.errors import AuthenticationError


@pytest.fixture
def service():
    return AuthService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    return db


class TestLogin:

    async def test_login_returns_tokens_when_credentials_are_valid(
        self, service, mock_db
    ):
        mock_user = MagicMock()
        mock_user.id = MagicMock()

        with patch(
            "app.services.auth_service.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.services.auth_service.refresh_token_repository",
            autospec=True,
        ) as mock_rt_repo, patch(
            "app.services.auth_service.pwd_context",
        ) as mock_pwd:

            mock_user_repo.get_by_email = AsyncMock(return_value=mock_user)
            mock_pwd.verify = MagicMock(return_value=True)
            mock_rt_repo.create = AsyncMock()

            access_token, refresh_token = await service.login(
                mock_db, "user@example.com", "password123"
            )

            assert access_token is not None
            assert refresh_token is not None

    async def test_login_raises_error_when_user_does_not_exist(
        self, service, mock_db
    ):
        with patch(
            "app.services.auth_service.user_repository",
            autospec=True,
        ) as mock_user_repo:

            mock_user_repo.get_by_email = AsyncMock(return_value=None)

            with pytest.raises(AuthenticationError):
                await service.login(mock_db, "unknown@example.com", "password123")

    async def test_login_raises_error_when_password_is_wrong(
        self, service, mock_db
    ):
        mock_user = MagicMock()

        with patch(
            "app.services.auth_service.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.services.auth_service.pwd_context",
        ) as mock_pwd:

            mock_user_repo.get_by_email = AsyncMock(return_value=mock_user)
            mock_pwd.verify = MagicMock(return_value=False)

            with pytest.raises(AuthenticationError):
                await service.login(mock_db, "user@example.com", "wrongpassword")


class TestRefresh:

    async def test_refresh_returns_new_tokens_when_token_is_valid(
        self, service, mock_db
    ):
        mock_refresh_token = MagicMock()
        mock_refresh_token.user_id = MagicMock()
        mock_refresh_token.expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        with patch(
            "app.services.auth_service.refresh_token_repository",
            autospec=True,
        ) as mock_rt_repo:

            mock_rt_repo.get_by_token = AsyncMock(return_value=mock_refresh_token)
            mock_rt_repo.delete_by_token = AsyncMock()
            mock_rt_repo.create = AsyncMock()

            new_access_token, new_refresh_token = await service.refresh(
                mock_db, "valid-refresh-token"
            )

            assert new_access_token is not None
            assert new_refresh_token is not None

    async def test_refresh_raises_error_when_token_does_not_exist(
        self, service, mock_db
    ):
        with patch(
            "app.services.auth_service.refresh_token_repository",
            autospec=True,
        ) as mock_rt_repo:

            mock_rt_repo.get_by_token = AsyncMock(return_value=None)

            with pytest.raises(AuthenticationError):
                await service.refresh(mock_db, "nonexistent-token")

    async def test_refresh_raises_error_when_token_is_expired(
        self, service, mock_db
    ):
        mock_refresh_token = MagicMock()
        mock_refresh_token.expires_at = datetime.now(timezone.utc) - timedelta(days=1)

        with patch(
            "app.services.auth_service.refresh_token_repository",
            autospec=True,
        ) as mock_rt_repo:

            mock_rt_repo.get_by_token = AsyncMock(return_value=mock_refresh_token)

            with pytest.raises(AuthenticationError):
                await service.refresh(mock_db, "expired-token")
