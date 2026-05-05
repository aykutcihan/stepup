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
    return MagicMock()

async def test_validate_invitation_returns_invitation_when_token_is_valid(
    service, mock_db
):
    mock_invitation = MagicMock()
    mock_invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    mock_invitation.used_at = None

    with patch(
        "app.services.invitation_service.invitation_repository"
    ) as mock_repo:
        mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

        result = await service.validate_invitation(mock_db, "valid-token")

        assert result == mock_invitation


async def test_validate_invitation_raises_not_found_when_token_does_not_exist(
    service, mock_db
):
    with patch(
        "app.services.invitation_service.invitation_repository"
    ) as mock_repo:
        mock_repo.get_by_token = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError):
            await service.validate_invitation(mock_db, "invalid-token")


async def test_validate_invitation_raises_error_when_invitation_is_expired(
    service, mock_db
):
    mock_invitation = MagicMock()
    mock_invitation.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    mock_invitation.used_at = None

    with patch(
        "app.services.invitation_service.invitation_repository"
    ) as mock_repo:
        mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

        with pytest.raises(ValidationError):
            await service.validate_invitation(mock_db, "expired-token")


async def test_validate_invitation_raises_error_when_invitation_is_already_used(
    service, mock_db
):
    mock_invitation = MagicMock()
    mock_invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    mock_invitation.used_at = datetime.now(timezone.utc) - timedelta(days=1)

    with patch(
        "app.services.invitation_service.invitation_repository"
    ) as mock_repo:
        mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

        with pytest.raises(ValidationError):
            await service.validate_invitation(mock_db, "used-token")
