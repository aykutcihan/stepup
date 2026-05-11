import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemplateCreate(BaseModel):
    name: str
    department_id: uuid.UUID


class TemplateUpdate(BaseModel):
    name: str | None = None
    department_id: uuid.UUID | None = None


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    department_id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    id: uuid.UUID
    template_id: uuid.UUID
    title: str
    description: str | None
    order: int
    deadline_days: int
    is_required: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


    