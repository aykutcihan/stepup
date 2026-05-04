from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.errors import AuthenticationError
from app.errors import messages
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.database import get_db
from app.core.security import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession


user_repository = UserRepository()
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_id = decode_access_token(credentials.credentials)
    user = await user_repository.get_by_id(db, user_id)
    if not user:
        raise AuthenticationError(*messages.INVALID_TOKEN)
    return user
