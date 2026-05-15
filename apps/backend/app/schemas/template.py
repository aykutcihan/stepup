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


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    deadline_days: int
    is_required: bool = True


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline_days: int | None = None
    is_required: bool | None = None


class TaskReorder(BaseModel):
    new_order: int


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


    