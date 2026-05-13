import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, TimestampMixin
from app.enums.user_role import UserRole
from app.models.department import Department


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
    SAEnum(UserRole, name="user_role"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.id"),
        nullable=True,
    )
    department: Mapped["Department"] = relationship("Department", back_populates="users")

    @property
    def department_name(self) -> str | None:
        return self.department.name if self.department else None

