import secrets
from datetime import datetime, timedelta, timezone

import pytest
from passlib.context import CryptContext

from app.enums.user_role import UserRole
from app.models.refresh_token import RefreshToken
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestLogin:

    async def test_login_returns_200_and_sets_cookies_when_credentials_are_valid(
        self, client, db_session
    ):
        user = User(
            email="loginuser@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Login",
            last_name="User",
            password_hash=pwd_context.hash("password123"),
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()

        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "loginuser@test.com", "password": "password123"},
        )

        assert response.status_code == 200
        assert "access_token" in response.cookies or "Set-Cookie" in response.headers

    async def test_login_returns_401_when_password_is_wrong(
        self, client, db_session
    ):
        user = User(
            email="wrongpass@test.com",
            role=UserRole.EMPLOYEE,
            first_name="Wrong",
            last_name="Pass",
            password_hash=pwd_context.hash("correctpassword"),
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()

        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "wrongpass@test.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401

    async def test_login_returns_401_when_user_does_not_exist(
        self, client
    ):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@test.com", "password": "password123"},
        )

        assert response.status_code == 401


class TestLogout:

    async def test_logout_returns_204_when_authenticated(
        self, authenticated_client
    ):
        response = await authenticated_client.post("/api/v1/auth/logout")

        assert response.status_code == 204

    async def test_logout_returns_401_when_not_authenticated(
        self, client
    ):
        response = await client.post("/api/v1/auth/logout")

        assert response.status_code == 401
