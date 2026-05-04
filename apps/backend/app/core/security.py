import uuid
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.errors import AuthenticationError
from app.errors import messages


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError as exc:
        raise AuthenticationError(*messages.TOKEN_EXPIRED) from exc
    except JWTError as exc:
        raise AuthenticationError(*messages.INVALID_TOKEN) from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise AuthenticationError(*messages.INVALID_TOKEN)

    return uuid.UUID(user_id)
