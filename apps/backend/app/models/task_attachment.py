from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.onboarding_plan_task import OnboardingPlanTask
    from app.models.user import User


class TaskAttachment(Base, TimestampMixin):
    __tablename__ = "task_attachments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("onboarding_plan_tasks.id"), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    object_name: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(128), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    task: Mapped[OnboardingPlanTask] = relationship("OnboardingPlanTask", back_populates="attachments")
    uploader: Mapped[User] = relationship("User", foreign_keys=[uploaded_by])
