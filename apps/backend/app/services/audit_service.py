import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogListResponse, AuditLogResponse

audit_log_repository = AuditLogRepository()


class AuditService:

    async def log(
        self,
        db: AsyncSession,
        actor_id: uuid.UUID,
        action: AuditActionType,
        entity_type: AuditEntityType,
        entity_id: uuid.UUID,
        detail: str | None = None,
    ) -> None:
        entry = AuditLog(
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            detail=detail,
        )
        await audit_log_repository.create(db, entry)

    async def get_logs(
        self,
        db: AsyncSession,
        action: AuditActionType | None = None,
        entity_type: AuditEntityType | None = None,
        actor_id: uuid.UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> AuditLogListResponse:
        items, total = await audit_log_repository.get_all(
            db,
            action=action,
            entity_type=entity_type,
            actor_id=actor_id,
            date_from=date_from,
            date_to=date_to,
            page=page,
            page_size=page_size,
        )
        total_pages = (total + page_size - 1) // page_size

        return AuditLogListResponse(
            items=[
                AuditLogResponse(
                    id=item.id,
                    actor_id=item.actor_id,
                    actor_name=f"{item.actor.first_name} {item.actor.last_name}" if item.actor else str(item.actor_id),
                    action=item.action,
                    entity_type=item.entity_type,
                    entity_id=item.entity_id,
                    detail=item.detail,
                    created_at=item.created_at,
                )
                for item in items
            ],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page * page_size < total,
            has_prev=page > 1,
        )
