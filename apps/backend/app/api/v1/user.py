import uuid

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.user import (
    UserListResponse,
    UserProfileUpdate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/", response_model=UserListResponse, status_code=200)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
    role: UserRole | None = Query(None),
    department_id: uuid.UUID | None = Query(None),
    is_active: bool | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> UserListResponse:
    return await user_service.get_users(
        db=db, role=role, department_id=department_id, is_active=is_active, page=page, page_size=page_size
    )


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    content = await file.read()
    user = await user_service.upload_avatar(db, current_user, content, file.content_type or "")
    return UserResponse.model_validate(user)


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    user = await user_service.update_my_profile(db=db, user=current_user, data=data)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> UserResponse:
    user = await user_service.update_user(db=db, user_id=user_id, data=data, actor_id=current_user.id)
    return UserResponse.model_validate(user)


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


@router.patch("/{user_id}/reactivate", response_model=UserResponse)
async def reactivate_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> UserResponse:
    user = await user_service.reactivate_user(db=db, user_id=user_id, actor_id=current_user.id)
    return UserResponse.model_validate(user)
