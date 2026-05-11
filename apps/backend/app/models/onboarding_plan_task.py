from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Date, String, Text, Integer, Boolean
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base, TimestampMixin
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus

if TYPE_CHECKING:
    from app.models.onboarding_plan import OnboardingPlan


class OnboardingPlanTask(Base, TimestampMixin):
    __tablename__ = "onboarding_plan_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("onboarding_plans.id"), nullable=False
    )
    template_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("template_tasks.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    deadline: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[OnboardingPlanTaskStatus] = mapped_column(
        SAEnum(
            OnboardingPlanTaskStatus,
            name="onboarding_plan_task_status",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=OnboardingPlanTaskStatus.NOT_STARTED,
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    plan: Mapped["OnboardingPlan"] = relationship("OnboardingPlan", back_populates="tasks")
