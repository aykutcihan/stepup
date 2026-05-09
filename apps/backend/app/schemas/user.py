import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.user_role import UserRole


class RegisterRequest(BaseModel):
    token: str
    first_name: str
    last_name: str
    password: str


class UserUpdate(BaseModel):
    department_id: uuid.UUID | None = None
    role: UserRole | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    first_name: str
    last_name: str
    is_active: bool
    department_id: uuid.UUID | None
    department_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
