from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import RegisterRequest, UserResponse
from app.services.invitation_service import InvitationService
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse

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

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    token = await auth_service.login(
        db=db,
        email=data.email,
        password=data.password
    )
    return TokenResponse(access_token=token)