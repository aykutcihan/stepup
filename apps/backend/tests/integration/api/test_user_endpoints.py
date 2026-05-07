import pytest
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.enums.user_role import UserRole
from app.main import app
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


class TestGetUsers:

    async def test_get_users_returns_200_for_hr_admin(
        self, authenticated_client
    ):
        response = await authenticated_client.get("/api/v1/users/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_users_returns_401_when_not_authenticated(
        self, client
    ):
        response = await client.get("/api/v1/users/")

        assert response.status_code == 401

    async def test_get_users_returns_403_for_employee(
        self, db_session, client
    ):
        employee = User(
            email="employee_list@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Employee",
            last_name="Test",
            password_hash=pwd_context.hash("password123"),
            is_active=True,
        )
        db_session.add(employee)
        await db_session.flush()

        async def override_get_db():
            yield db_session

        async def override_get_current_user():
            return employee

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/v1/users/")

        app.dependency_overrides.clear()

        assert response.status_code == 403


class TestDeactivatedUserAccess:

    async def test_deactivated_user_gets_401_on_next_request(
        self, db_session, client
    ):
        from app.errors import AuthenticationError
        from app.errors import messages

        async def override_get_db():
            yield db_session

        async def override_get_current_user():
            raise AuthenticationError(*messages.USER_DEACTIVATED)

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/v1/users/")

        app.dependency_overrides.clear()

        assert response.status_code == 401
