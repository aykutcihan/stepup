import enum


class AuditActionType(enum.StrEnum):
    user_invited = "user.invited"
    user_registered = "user.registered"
    user_deactivated = "user.deactivated"
    user_reactivated = "user.reactivated"
    user_updated = "user.updated"

    plan_created = "plan.created"
    plan_task_cancelled = "plan.task_cancelled"

    task_started = "task.started"
    task_completed = "task.completed"
    task_approved = "task.approved"
    task_returned = "task.returned"


class AuditEntityType(enum.StrEnum):
    user = "user"
    invitation = "invitation"
    plan = "plan"
    task = "task"
