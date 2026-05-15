import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    actor_id: uuid.UUID
    action: str
    entity_type: str
    entity_id: uuid.UUID
    detail: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
