from fastapi import Request

from app.core.constants import ACCESS_TOKEN_COOKIE
from app.core.database import get_db
from app.core.security import decode_access_token
from app.errors import AuthenticationError
from app.errors import messages
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

user_repository = UserRepository()


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
