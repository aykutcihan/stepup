import enum


class OnboardingPlanTaskStatus(enum.StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    RETURNED = "returned"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
