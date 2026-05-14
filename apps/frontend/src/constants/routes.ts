export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  HR_DASHBOARD: '/hr/dashboard',
  HR_INVITE_USER: '/hr/invite-user',
  MANAGER_DASHBOARD: '/manager/dashboard',
  EMPLOYEE_DASHBOARD: '/employee/dashboard',
  HR_DEPARTMENTS: '/hr/departments',
  HR_USERS: '/hr/users',
  PROFILE: '/profile',
  HR_TEMPLATES: '/hr/templates',
  HR_TEMPLATE_DETAIL: (id: string) => `/hr/templates/${id}`,
  HR_PLANS: '/hr/plans',
  HR_PLAN_NEW: '/hr/plans/new',
  HR_PLAN_DETAIL: (id: string) => `/hr/plans/${id}`,
  EMPLOYEE_PLAN: '/employee/plan',
  EMPLOYEE_PROFILE: '/employee/profile',
  MANAGER_PROFILE: '/manager/profile',
  MANAGER_APPROVALS: '/manager/approvals',
  MANAGER_TASK_REVIEW: (id: string) => `/manager/tasks/${id}`,
  HR_AUDIT: '/hr/audit',
}

export const ERROR_ROUTES = {
  FORBIDDEN: '/403',
}
