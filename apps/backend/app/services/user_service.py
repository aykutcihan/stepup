import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.enums.user_role import UserRole
from app.errors import NotFoundError, ValidationError, messages
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserListResponse,
    UserProfileUpdate,
    UserResponse,
    UserUpdate,
)
from app.services.audit_service import AuditService

user_repository = UserRepository()
refresh_token_repository = RefreshTokenRepository()
audit_service = AuditService()


class UserService:

    async def get_users(
        self,
        db: AsyncSession,
        role: UserRole | None = None,
        department_id: uuid.UUID | None = None,
        is_active: bool | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> UserListResponse:
        items, total = await user_repository.get_all(
            db, role=role, department_id=department_id, is_active=is_active, page=page, page_size=page_size
        )
        total_pages = (total + page_size - 1) // page_size
        return UserListResponse(
            items=[UserResponse.model_validate(u) for u in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page * page_size < total,
            has_prev=page > 1,
        )

    async def update_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        data: UserUpdate,
        actor_id: uuid.UUID | None = None,
    ) -> User:
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError(*messages.USER_NOT_FOUND)

        if data.department_id is not None:
            user.department_id = data.department_id
        if data.role is not None:
            user.role = data.role

        await db.commit()
        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.user_updated, entity_type=AuditEntityType.user, entity_id=user_id)
            await db.commit()
        return await user_repository.get_by_id(db, user_id)

    async def update_my_profile(
        self,
        db: AsyncSession,
        user: User,
        data: UserProfileUpdate,
    ) -> User:
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        user_id = user.id
        await db.commit()
        return await user_repository.get_by_id(db, user_id)

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
        await audit_service.log(db, actor_id=current_user_id, action=AuditActionType.user_deactivated, entity_type=AuditEntityType.user, entity_id=user_id)
        await db.commit()

    async def reactivate_user(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        actor_id: uuid.UUID | None = None,
    ) -> User:
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError(*messages.USER_NOT_FOUND)

        user.is_active = True
        await db.commit()
        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.user_reactivated, entity_type=AuditEntityType.user, entity_id=user_id)
            await db.commit()
        return await user_repository.get_by_id(db, user_id)
