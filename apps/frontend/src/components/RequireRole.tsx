import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES, ERROR_ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type Role = components['schemas']['UserResponse']['role']

type Props = {
  roles: Role[]
}

export default function RequireRole({ roles }: Props) {
  const user = useAuthStore((state) => state.user)
  const isLoading = useAuthStore((state) => state.isLoading)

  if (isLoading) return null
  if (!user) return <Navigate to={ROUTES.LOGIN} replace />
  if (!roles.includes(user.role)) return <Navigate to={ERROR_ROUTES.FORBIDDEN} replace />

  return <Outlet />
}
