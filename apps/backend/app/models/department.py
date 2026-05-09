

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Department(Base, TimestampMixin):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )    

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="department")