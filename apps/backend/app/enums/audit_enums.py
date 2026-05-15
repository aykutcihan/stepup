import enum


class AuditActionType(str, enum.Enum):
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


class AuditEntityType(str, enum.Enum):
    user = "user"
    invitation = "invitation"
    plan = "plan"
    task = "task"
