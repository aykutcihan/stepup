import pytest
from unittest.mock import AsyncMock, patch

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
