import type { components } from '@/types/api'

export type UserRole = components['schemas']['UserRole']

export const USER_ROLE_VALUES = ['employee', 'manager', 'hr_admin'] as const satisfies readonly UserRole[]

export const USER_ROLES = {
  HR_ADMIN: 'hr_admin' as UserRole,
  MANAGER: 'manager' as UserRole,
  EMPLOYEE: 'employee' as UserRole,
}
