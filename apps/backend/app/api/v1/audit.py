import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.audit_log import AuditLogListResponse
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()


@router.get("/", response_model=AuditLogListResponse)
async def get_audit_logs(
    action: AuditActionType | None = Query(None, description="Filter by action type"),
    entity_type: AuditEntityType | None = Query(None, description="Filter by entity type"),
    actor_id: uuid.UUID | None = Query(None, description="Filter by actor (user) ID"),
    date_from: datetime | None = Query(None, description="Filter from date (ISO 8601)"),
    date_to: datetime | None = Query(None, description="Filter to date (ISO 8601)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> AuditLogListResponse:
    return await audit_service.get_logs(
        db=db,
        action=action,
        entity_type=entity_type,
        actor_id=actor_id,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
    )
