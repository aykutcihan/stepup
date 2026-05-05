import secrets
from datetime import datetime, timedelta, timezone

import pytest
from unittest.mock import AsyncMock, patch

from app.enums.user_role import UserRole
from app.models.invitation import Invitation

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestPostInvitation:

    async def test_post_invitation_returns_201_when_request_is_valid(
        self, authenticated_client
    ):
        with patch(
            "app.services.invitation_service.email_service",
            autospec=True,
        ) as mock_email:
            mock_email.send_invitation_email = AsyncMock()

            response = await authenticated_client.post(
                "/api/v1/invitations/",
                json={"email": "newemployee@example.com", "role": "employee"},
            )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newemployee@example.com"
        assert data["role"] == "employee"
        assert "id" in data
        assert "expires_at" in data


    async def test_post_invitation_returns_400_when_user_already_exists(
        self, authenticated_client
    ):
        with patch(
            "app.services.invitation_service.email_service",
            autospec=True,
        ) as mock_email:
            mock_email.send_invitation_email = AsyncMock()

            response = await authenticated_client.post(
                "/api/v1/invitations/",
                json={"email": "admin@test.com", "role": "employee"},
            )

        assert response.status_code == 400


    async def test_post_invitation_returns_401_when_not_authenticated(
        self, client
    ):
        response = await client.post(
            "/api/v1/invitations/",
            json={"email": "someone@example.com", "role": "employee"},
        )

        assert response.status_code == 401


class TestValidateInvitation:

    async def test_validate_invitation_returns_200_when_token_is_valid(
        self, authenticated_client, db_session, hr_admin_user
    ):
        invitation = Invitation(
            email="invited@example.com",
            role=UserRole.EMPLOYEE,
            token=secrets.token_urlsafe(32),
            invited_by=hr_admin_user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db_session.add(invitation)
        await db_session.flush()

        response = await authenticated_client.get(
            f"/api/v1/invitations/validate?token={invitation.token}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "invited@example.com"
        assert data["role"] == "employee"


    async def test_validate_invitation_returns_404_when_token_does_not_exist(
        self, client
    ):
        response = await client.get(
            "/api/v1/invitations/validate?token=nonexistent-token"
        )

        assert response.status_code == 404


class TestGetInvitations:

    async def test_get_invitations_returns_200_with_empty_list(
        self, authenticated_client
    ):
        response = await authenticated_client.get("/api/v1/invitations/")

        assert response.status_code == 200
        assert response.json() == []

    async def test_get_invitations_returns_401_when_not_authenticated(
        self, client
    ):
        response = await client.get("/api/v1/invitations/")

        assert response.status_code == 401


class TestResendInvitation:

    async def test_resend_invitation_returns_200_when_id_is_valid(
        self, authenticated_client, db_session, hr_admin_user
    ):
        with patch(
            "app.services.invitation_service.email_service",
            autospec=True,
        ) as mock_email:
            mock_email.send_invitation_email = AsyncMock()

            invitation = Invitation(
                email="resend@example.com",
                role=UserRole.EMPLOYEE,
                token=secrets.token_urlsafe(32),
                invited_by=hr_admin_user.id,
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            )
            db_session.add(invitation)
            await db_session.flush()

            response = await authenticated_client.post(
                f"/api/v1/invitations/{invitation.id}/resend"
            )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "resend@example.com"

    async def test_resend_invitation_returns_401_when_not_authenticated(
        self, client
    ):
        import uuid
        response = await client.post(
            f"/api/v1/invitations/{uuid.uuid4()}/resend"
        )

        assert response.status_code == 401
