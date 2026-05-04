from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import RegisterRequest, UserResponse
from app.services.auth_service import AuthService
from app.services.invitation_service import InvitationService
from app.errors import AuthenticationError, messages
from app.core.constants import ACCESS_TOKEN_COOKIE, REFRESH_TOKEN_COOKIE


router = APIRouter()
invitation_service = InvitationService()
auth_service = AuthService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await invitation_service.register_user_from_invitation(
        db=db,
        token=data.token,
        first_name=data.first_name,
        last_name=data.last_name,
        password=data.password,
    )
    return UserResponse.model_validate(user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> dict:
    access_token, refresh_token = await auth_service.login(
        db=db,
        email=data.email,
        password=data.password,
    )
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        httponly=True,
        samesite="strict",
        max_age=60 * 15,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        httponly=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7,
    )
    return {"message": "Login successful"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    await auth_service.logout(db=db, user_id=current_user.id)
    response.delete_cookie(ACCESS_TOKEN_COOKIE)
    response.delete_cookie(REFRESH_TOKEN_COOKIE)
    return {"message": "Logout successful"}



@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> dict:
    token = request.cookies.get(REFRESH_TOKEN_COOKIE)
    if not token:
        raise AuthenticationError(*messages.INVALID_TOKEN)

    access_token, refresh_token = await auth_service.refresh(
        db=db,
        token=token,
    )
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        httponly=True,
        samesite="strict",
        max_age=60 * 15,
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        httponly=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7,
    )
    return {"message": "Token refreshed"}

