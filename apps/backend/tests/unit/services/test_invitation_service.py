import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta, timezone

from app.services.invitation_service import InvitationService
from app.errors import NotFoundError, ValidationError


@pytest.fixture
def service():
    return InvitationService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    return db


class TestValidateInvitation:

    async def test_validate_invitation_returns_invitation_when_token_is_valid(
        self, service, mock_db
    ):
        mock_invitation = MagicMock()
        mock_invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        mock_invitation.used_at = None

        with patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_repo:
            mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

            result = await service.validate_invitation(mock_db, "valid-token")

            assert result == mock_invitation

    async def test_validate_invitation_raises_not_found_when_token_does_not_exist(
        self, service, mock_db
    ):
        with patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_repo:
            mock_repo.get_by_token = AsyncMock(return_value=None)

            with pytest.raises(NotFoundError):
                await service.validate_invitation(mock_db, "invalid-token")

    async def test_validate_invitation_raises_error_when_invitation_is_expired(
        self, service, mock_db
    ):
        mock_invitation = MagicMock()
        mock_invitation.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        mock_invitation.used_at = None

        with patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_repo:
            mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

            with pytest.raises(ValidationError):
                await service.validate_invitation(mock_db, "expired-token")

    async def test_validate_invitation_raises_error_when_invitation_is_already_used(
        self, service, mock_db
    ):
        mock_invitation = MagicMock()
        mock_invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        mock_invitation.used_at = datetime.now(timezone.utc) - timedelta(days=1)

        with patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_repo:
            mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

            with pytest.raises(ValidationError):
                await service.validate_invitation(mock_db, "used-token")


class TestCreateInvitation:

    async def test_create_invitation_returns_invitation_when_email_is_new(
        self, service, mock_db
    ):
        with patch(
            "app.services.invitation_service.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_inv_repo, patch(
            "app.services.invitation_service.email_service",
            autospec=True,
        ) as mock_email:

            mock_user_repo.get_by_email = AsyncMock(return_value=None)
            mock_inv_repo.create = AsyncMock()
            mock_email.send_invitation_email = AsyncMock()

            result = await service.create_invitation(
                mock_db, "new@example.com", MagicMock(), MagicMock()
            )

            assert result is not None


    async def test_create_invitation_raises_error_when_user_already_exists(
        self, service, mock_db
    ):
        with patch(
            "app.services.invitation_service.user_repository",
            autospec=True,
        ) as mock_user_repo:
            mock_user_repo.get_by_email = AsyncMock(return_value=MagicMock())

            with pytest.raises(ValidationError):
                await service.create_invitation(
                    mock_db, "existing@example.com", MagicMock(), MagicMock()
                )


    async def test_create_invitation_still_returns_invitation_when_email_service_fails(
        self, service, mock_db
    ):
        with patch(
            "app.services.invitation_service.user_repository",
            autospec=True,
        ) as mock_user_repo, patch(
            "app.services.invitation_service.invitation_repository",
            autospec=True,
        ) as mock_inv_repo, patch(
            "app.services.invitation_service.email_service",
            autospec=True,
        ) as mock_email:

            mock_user_repo.get_by_email = AsyncMock(return_value=None)
            mock_inv_repo.create = AsyncMock()
            mock_email.send_invitation_email = AsyncMock(side_effect=Exception("SMTP error"))

            result = await service.create_invitation(
                mock_db, "new@example.com", MagicMock(), MagicMock()
            )

            assert result is not None


class TestRegisterUserFromInvitation:

    async def test_register_user_from_invitation_returns_user_when_token_is_valid(
        self, service, mock_db
    ):
        mock_invitation = MagicMock()
        mock_invitation.email = "user@example.com"
        mock_invitation.role = MagicMock()

        with patch.object(
            service, "validate_invitation", new=AsyncMock(return_value=mock_invitation)
        ), patch(
            "app.services.invitation_service.user_repository",
            autospec=True,
        ) as mock_user_repo:

            mock_user_repo.get_by_email = AsyncMock(return_value=None)

            result = await service.register_user_from_invitation(
                mock_db, "valid-token", "John", "Doe", "password123"
            )

            assert result is not None
