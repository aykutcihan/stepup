export const ERROR_MESSAGES: Record<string, string> = {
  INVITATION_EXPIRED: 'This invitation link has expired.',
  INVITATION_ALREADY_USED: 'This invitation link has already been used.',
  INVITATION_ALREADY_PENDING: 'An active invitation for this email already exists.',
  INVITATION_NOT_FOUND: 'Invitation not found.',
  USER_ALREADY_EXISTS: 'An account with this email already exists.',
  USER_NOT_FOUND: 'User not found.',
  USER_DEACTIVATED: 'Your account has been deactivated. Please contact your HR Admin.',
  PERMISSION_DENIED: 'You do not have permission to perform this action.',
  EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN: 'This employee already has an active onboarding plan.',
  TEMPLATE_NOT_ACTIVE: 'Template must be active to create a plan.',
  DEPARTMENT_HAS_ACTIVE_USERS: 'Cannot deactivate a department with active users.',
  DEPARTMENT_NOT_FOUND: 'Department not found.',
}
