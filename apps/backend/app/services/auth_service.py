from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.core.security import create_access_token
from app.errors import AuthenticationError
from app.errors import messages
from app.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_repository = UserRepository()


class AuthService:

    async def login(self, db: AsyncSession, email: str, password: str) -> str:
        user = await user_repository.get_by_email(db, email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise AuthenticationError(*messages.INVALID_CREDENTIALS)

        return create_access_token(user.id)
