

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str

class DepartmentUpdate(BaseModel):
    name: str

class DepartmentResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
