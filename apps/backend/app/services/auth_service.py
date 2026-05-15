from datetime import UTC, datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token
from app.errors import AuthenticationError, messages
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository

REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_repository = UserRepository()
refresh_token_repository = RefreshTokenRepository()


class AuthService:

    async def login(self, db: AsyncSession, email: str, password: str) -> tuple[str, str]:
        user = await user_repository.get_by_email(db, email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise AuthenticationError(*messages.INVALID_CREDENTIALS)
        if not user.is_active:
            raise AuthenticationError(*messages.USER_DEACTIVATED)

        access_token = create_access_token(user.id)
        refresh_token_value = create_refresh_token()

        refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token_value,
            expires_at=datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await refresh_token_repository.create(db, refresh_token)
        await db.commit()

        return access_token, refresh_token_value

    async def refresh(self, db: AsyncSession, token: str) -> tuple[str, str]:
        refresh_token = await refresh_token_repository.get_by_token(db, token)

        if not refresh_token or refresh_token.expires_at < datetime.now(UTC):
            raise AuthenticationError(*messages.INVALID_TOKEN)

        await refresh_token_repository.delete_by_token(db, token)

        new_access_token = create_access_token(refresh_token.user_id)
        new_refresh_token_value = create_refresh_token()

        new_refresh_token = RefreshToken(
            user_id=refresh_token.user_id,
            token=new_refresh_token_value,
            expires_at=datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await refresh_token_repository.create(db, new_refresh_token)
        await db.commit()

        return new_access_token, new_refresh_token_value

    async def logout(self, db: AsyncSession, user_id) -> None:
        await refresh_token_repository.delete_by_user_id(db, user_id)
        await db.commit()
