import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
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
from app.services.storage_service import StorageService

_ALLOWED_AVATAR_TYPES = {"image/jpeg", "image/png", "image/webp"}
_AVATAR_EXT_MAP = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
_MAX_AVATAR_BYTES = 5 * 1024 * 1024


def _valid_avatar_signature(content: bytes, content_type: str) -> bool:
    if content_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")
    if content_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/webp":
        return content[:4] == b"RIFF" and content[8:12] == b"WEBP"
    return False


def _gcs_object_name(avatar_url: str) -> str | None:
    prefix = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/"
    if avatar_url.startswith(prefix):
        return avatar_url[len(prefix):]
    return None

user_repository = UserRepository()
refresh_token_repository = RefreshTokenRepository()
audit_service = AuditService()
storage_service = StorageService()


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

        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.user_updated, entity_type=AuditEntityType.user, entity_id=user_id)
        await db.commit()
        return await user_repository.get_by_id(db, user_id)

    async def upload_avatar(
        self,
        db: AsyncSession,
        user: User,
        content: bytes,
        content_type: str,
    ) -> User:
        if content_type not in _ALLOWED_AVATAR_TYPES:
            raise ValidationError(*messages.INVALID_AVATAR_TYPE)
        if len(content) > _MAX_AVATAR_BYTES:
            raise ValidationError(*messages.AVATAR_TOO_LARGE)
        if not _valid_avatar_signature(content, content_type):
            raise ValidationError(*messages.INVALID_AVATAR_TYPE)

        if user.avatar_url:
            old_object = _gcs_object_name(user.avatar_url)
            if old_object:
                storage_service.delete(old_object)

        ext = _AVATAR_EXT_MAP[content_type]
        object_name = f"avatars/{user.id}.{ext}"
        storage_service.upload(content, object_name, content_type)
        user.avatar_url = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/{object_name}"
        user_id = user.id
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
        if actor_id:
            await audit_service.log(db, actor_id=actor_id, action=AuditActionType.user_reactivated, entity_type=AuditEntityType.user, entity_id=user_id)
        await db.commit()
        return await user_repository.get_by_id(db, user_id)
