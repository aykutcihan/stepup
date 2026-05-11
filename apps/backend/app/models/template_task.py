from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.onboarding_template import OnboardingTemplate


class TemplateTask(Base, TimestampMixin):
    __tablename__ = "template_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    template_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("onboarding_templates.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    deadline_days: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    template: Mapped["OnboardingTemplate"] = relationship(
        "OnboardingTemplate", back_populates="tasks"
    )