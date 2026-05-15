import pytest
from httpx import ASGITransport, AsyncClient
from passlib.context import CryptContext

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.enums.user_role import UserRole
from app.main import app
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestGetMe:

    async def test_get_me_returns_200_with_correct_user(self, authenticated_client, hr_admin_user):
        response = await authenticated_client.get("/api/v1/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == hr_admin_user.email
        assert data["first_name"] == hr_admin_user.first_name
        assert data["last_name"] == hr_admin_user.last_name
        assert data["role"] == hr_admin_user.role.value
        assert data["department_name"] is None

    async def test_get_me_returns_401_when_not_authenticated(self, client):
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 401


class TestUpdateMyProfile:

    async def test_patch_me_updates_name(self, authenticated_client):
        response = await authenticated_client.patch(
            "/api/v1/users/me",
            json={"first_name": "Updated", "last_name": "Name"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"

    async def test_patch_me_cannot_change_role(self, authenticated_client):
        response = await authenticated_client.patch(
            "/api/v1/users/me",
            json={"role": "employee"},
        )

        assert response.status_code == 422

    async def test_patch_me_returns_401_when_not_authenticated(self, client):
        response = await client.patch(
            "/api/v1/users/me",
            json={"first_name": "Hacker"},
        )

        assert response.status_code == 401


class TestUpdateUser:

    async def test_patch_user_assigns_department(self, authenticated_client, db_session):
        from app.models.department import Department

        dept = Department(name="UpdateTestDept", is_active=True)
        db_session.add(dept)
        await db_session.flush()
        dept_id = str(dept.id)
        target = User(
            email="update_target@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Update",
            last_name="Target",
            password_hash="placeholder",
            is_active=True,
        )
        db_session.add(target)
        await db_session.flush()

        response = await authenticated_client.patch(
            f"/api/v1/users/{target.id}",
            json={"department_id": dept_id},
        )

        assert response.status_code == 200
        assert response.json()["department_id"] == dept_id

    async def test_patch_user_returns_404_when_not_found(self, authenticated_client):
        response = await authenticated_client.patch(
            "/api/v1/users/00000000-0000-0000-0000-000000000000",
            json={"role": "manager"},
        )

        assert response.status_code == 404


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
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)

    async def test_get_users_returns_401_when_not_authenticated(
        self, client
    ):
        response = await client.get("/api/v1/users/")

        assert response.status_code == 401

    async def test_get_users_filters_by_role(self, authenticated_client, db_session):
        user = User(
            email="manager_filter@test.com",
            role=UserRole.MANAGER,
            first_name="Manager",
            last_name="Filter",
            password_hash="placeholder",
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()

        response = await authenticated_client.get("/api/v1/users/?role=manager")

        assert response.status_code == 200
        data = response.json()
        assert all(u["role"] == "manager" for u in data["items"])

    async def test_get_users_filters_by_is_active(self, authenticated_client, db_session):
        user = User(
            email="inactive_filter@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Inactive",
            last_name="Filter",
            password_hash="placeholder",
            is_active=False,
        )
        db_session.add(user)
        await db_session.flush()

        response = await authenticated_client.get("/api/v1/users/?is_active=false")

        assert response.status_code == 200
        data = response.json()
        assert all(u["is_active"] is False for u in data["items"])

    async def test_get_users_returns_pagination_metadata(self, authenticated_client):
        response = await authenticated_client.get("/api/v1/users/?page=1&page_size=10")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert "total_pages" in data
        assert data["has_prev"] is False

    async def test_get_users_page_size_above_limit_returns_422(self, authenticated_client):
        response = await authenticated_client.get("/api/v1/users/?page_size=101")

        assert response.status_code == 422

    async def test_get_users_page_zero_returns_422(self, authenticated_client):
        response = await authenticated_client.get("/api/v1/users/?page=0")

        assert response.status_code == 422

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
        from app.errors import AuthenticationError, messages

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
