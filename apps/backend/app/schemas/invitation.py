import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.user_role import UserRole


class InvitationCreate(BaseModel):
    email: EmailStr
    role: UserRole
    department_id: uuid.UUID | None = None


class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    expires_at: datetime
    department_id: uuid.UUID | None

    model_config = ConfigDict(from_attributes=True)

class InvitationValidateResponse(BaseModel):
    email: str
    role: UserRole


class InvitationListResponse(BaseModel):
    items: list[InvitationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

