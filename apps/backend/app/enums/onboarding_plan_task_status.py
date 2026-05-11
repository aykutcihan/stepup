import enum


class OnboardingPlanTaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    CANCELLED = "cancelled"
