import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.get("/", response_model=list[UserResponse], status_code=200)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[UserResponse]:
    users = await user_service.get_users(db=db)
    result = []
    for u in users:
        result.append(UserResponse.model_validate(u))
    return result


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> None:
    await user_service.deactivate_user(
        db=db,
        user_id=user_id,
        current_user_id=current_user.id,
    )
