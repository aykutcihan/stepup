from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import RegisterRequest, UserResponse
from app.services.invitation_service import InvitationService

router = APIRouter()
invitation_service = InvitationService()


@router.post("/register", response_model=UserResponse, status_code=201)
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
