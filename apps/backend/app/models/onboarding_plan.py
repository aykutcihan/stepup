from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.onboarding_plan_task import OnboardingPlanTask
    from app.models.user import User


class OnboardingPlan(Base, TimestampMixin):
    __tablename__ = "onboarding_plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    template_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("onboarding_templates.id"), nullable=False
    )
    manager_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tasks: Mapped[list[OnboardingPlanTask]] = relationship(
        "OnboardingPlanTask", back_populates="plan", order_by="OnboardingPlanTask.order"
    )
    employee: Mapped[User] = relationship("User", foreign_keys=[user_id])
    manager: Mapped[User] = relationship("User", foreign_keys=[manager_id])
