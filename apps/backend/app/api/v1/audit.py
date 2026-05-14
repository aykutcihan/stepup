from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()


@router.get("/", response_model=list[AuditLogResponse])
async def get_audit_logs(
    action: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[AuditLogResponse]:
    logs = await audit_service.get_logs(db=db, action=action, limit=limit, offset=offset)
    return [AuditLogResponse.model_validate(log) for log in logs]
