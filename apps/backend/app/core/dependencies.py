from fastapi import Request

from app.errors import AuthenticationError
from app.errors import messages
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.database import get_db
from app.core.security import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

user_repository = UserRepository()

ACCESS_TOKEN_COOKIE = "access_token"


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    token = request.cookies.get(ACCESS_TOKEN_COOKIE)
    if not token:
        raise AuthenticationError(*messages.INVALID_TOKEN)

    user_id = decode_access_token(token)
    user = await user_repository.get_by_id(db, user_id)
    if not user:
        raise AuthenticationError(*messages.INVALID_TOKEN)
    return user
