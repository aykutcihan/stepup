import pytest
from passlib.context import CryptContext

from app.enums.user_role import UserRole
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestDeactivateUser:

    async def test_deactivate_user_returns_204_when_id_is_valid(
        self, authenticated_client, db_session
    ):
        target_user = User(
            email="target@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Target",
            last_name="User",
            password_hash=pwd_context.hash("password123"),
            is_active=True,
        )
        db_session.add(target_user)
        await db_session.flush()

        response = await authenticated_client.patch(
            f"/api/v1/users/{target_user.id}/deactivate"
        )

        assert response.status_code == 204

    async def test_deactivate_user_returns_400_when_deactivating_self(
        self, authenticated_client, hr_admin_user
    ):
        response = await authenticated_client.patch(
            f"/api/v1/users/{hr_admin_user.id}/deactivate"
        )

        assert response.status_code == 400

    async def test_deactivate_user_returns_404_when_user_not_found(
        self, authenticated_client
    ):
        import uuid
        response = await authenticated_client.patch(
            f"/api/v1/users/{uuid.uuid4()}/deactivate"
        )

        assert response.status_code == 404

    async def test_deactivate_user_returns_401_when_not_authenticated(
        self, client
    ):
        import uuid
        response = await client.patch(
            f"/api/v1/users/{uuid.uuid4()}/deactivate"
        )

        assert response.status_code == 401
