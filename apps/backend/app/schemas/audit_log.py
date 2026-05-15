import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.audit_enums import AuditActionType, AuditEntityType


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    actor_id: uuid.UUID
    actor_name: str
    action: AuditActionType
    entity_type: AuditEntityType
    entity_id: uuid.UUID
    detail: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
