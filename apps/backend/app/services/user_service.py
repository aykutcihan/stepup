import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.user_role import UserRole
from app.errors import NotFoundError, ValidationError
from app.errors import messages
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate

user_repository = UserRepository()
refresh_token_repository = RefreshTokenRepository()


class UserService:

    async def get_users(
        self,
        db: AsyncSession,
        role: UserRole | None = None,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
    ) -> list:
        return await user_repository.get_all(db, role=role, department_id=department_id, is_active=is_active)

    async def update_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        data: UserUpdate,
    ) -> User:
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError(*messages.USER_NOT_FOUND)

        if data.department_id is not None:
            user.department_id = data.department_id
        if data.role is not None:
            user.role = data.role

        await db.commit()
        await db.refresh(user)
        return user

    async def deactivate_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        current_user_id: uuid.UUID,
    ) -> None:
        if user_id == current_user_id:
            raise ValidationError(*messages.CANNOT_DEACTIVATE_SELF)

        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError(*messages.USER_NOT_FOUND)

        user.is_active = False
        await refresh_token_repository.delete_by_user_id(db, user_id)
        await db.commit()
