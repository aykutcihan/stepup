

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    name: str

# DepartmentUpdate → PATCH body (sadece isim değiştirmek için)
class DepartmentUpdate(BaseModel):
    name: str

# DepartmentResponse → tüm endpoint'lerin döndürdüğü shape
class DepartmentResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
