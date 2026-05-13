# Invitation
INVITATION_NOT_FOUND = ("INVITATION_NOT_FOUND", "Invitation not found")
INVITATION_EXPIRED = ("INVITATION_EXPIRED", "Invitation token has expired")
INVITATION_ALREADY_USED = ("INVITATION_ALREADY_USED", "Invitation has already been used")

# User
USER_ALREADY_EXISTS = ("USER_ALREADY_EXISTS", "A user with this email already exists")
USER_NOT_FOUND = ("USER_NOT_FOUND", "User not found")
CANNOT_DEACTIVATE_SELF = ("CANNOT_DEACTIVATE_SELF", "You cannot deactivate your own account")

# Authentication
INVALID_CREDENTIALS = ("INVALID_CREDENTIALS", "Invalid email or password")
INVALID_TOKEN = ("INVALID_TOKEN", "Invalid token")
TOKEN_EXPIRED = ("TOKEN_EXPIRED", "Token has expired")
USER_DEACTIVATED = ("USER_DEACTIVATED", "Your account has been deactivated")

# Authorization
PERMISSION_DENIED = ("PERMISSION_DENIED", "You do not have permission to perform this action")

# Department
DEPARTMENT_ALREADY_EXISTS = ("DEPARTMENT_ALREADY_EXISTS", "A department with this name already exists")
DEPARTMENT_NOT_FOUND = ("DEPARTMENT_NOT_FOUND", "Department not found")
DEPARTMENT_HAS_ACTIVE_USERS = ("DEPARTMENT_HAS_ACTIVE_USERS", "Cannot deactivate a department with active users")

# Template
TEMPLATE_NOT_FOUND = ("TEMPLATE_NOT_FOUND", "Template not found")
TEMPLATE_NO_TASKS = ("TEMPLATE_NO_TASKS", "Template must have at least one task before it can be activated")
TEMPLATE_HAS_PLANS = ("TEMPLATE_HAS_PLANS", "Cannot delete a template that has associated plans")

# Task
TASK_NOT_FOUND = ("TASK_NOT_FOUND", "Task not found")
INVALID_REORDER = ("INVALID_REORDER", "Invalid order position")

# Onboarding Plan
PLAN_NOT_FOUND = ("PLAN_NOT_FOUND", "Plan not found")
PLAN_TASK_NOT_FOUND = ("PLAN_TASK_NOT_FOUND", "Plan task not found")
EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN = ("EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN", "This employee already has an active onboarding plan")
TEMPLATE_NOT_ACTIVE = ("TEMPLATE_NOT_ACTIVE", "Template must be active to create a plan")
TASK_ALREADY_TERMINAL = ("TASK_ALREADY_TERMINAL", "This task is already in a terminal state and cannot be cancelled")