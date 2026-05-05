import pytest
from httpx import AsyncClient, ASGITransport

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.enums.user_role import UserRole
from app.main import app
from app.models.user import User


@pytest.fixture
async def hr_admin_user(db_session):
    user = User(
        email="admin@test.com",
        role=UserRole.HR_ADMIN,
        first_name="Admin",
        last_name="Test",
        password_hash="placeholder_hash",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def authenticated_client(db_session, hr_admin_user):
    async def override_get_db():
        yield db_session

    async def override_get_current_user():
        return hr_admin_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
