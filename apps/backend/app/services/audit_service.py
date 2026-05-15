import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository

audit_log_repository = AuditLogRepository()


class AuditService:

    async def log(
        self,
        db: AsyncSession,
        actor_id: uuid.UUID,
        action: str,
        entity_type: str,
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
        action: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditLog]:
        return await audit_log_repository.get_all(db, action=action, limit=limit, offset=offset)
