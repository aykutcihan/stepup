import { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import RegisterPage from '@/pages/RegisterPage'
import InviteUserPage from '@/pages/hr/InviteUserPage'
import LoginPage from '@/pages/LoginPage'
import HRDashboard from '@/pages/hr/HRDashboard'
import ManagerDashboard from '@/pages/manager/ManagerDashboard'
import EmployeeDashboard from '@/pages/employee/EmployeeDashboard'
import ForbiddenPage from '@/pages/ForbiddenPage'
import RequireRole from '@/components/RequireRole'
import { ROUTES, ERROR_ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'
import { getMe } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

export default function App() {
  const setUser = useAuthStore((state) => state.setUser)
  const setLoading = useAuthStore((state) => state.setLoading)

  useEffect(() => {
    getMe()
      .then(setUser)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <Routes>
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />
      <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
      <Route path={ERROR_ROUTES.FORBIDDEN} element={<ForbiddenPage />} />

      <Route element={<RequireRole roles={[USER_ROLES.HR_ADMIN]} />}>
        <Route path={ROUTES.HR_DASHBOARD} element={<HRDashboard />} />
        <Route path={ROUTES.HR_INVITE_USER} element={<InviteUserPage />} />
      </Route>

      <Route element={<RequireRole roles={[USER_ROLES.MANAGER]} />}>
        <Route path={ROUTES.MANAGER_DASHBOARD} element={<ManagerDashboard />} />
      </Route>

      <Route element={<RequireRole roles={[USER_ROLES.EMPLOYEE]} />}>
        <Route path={ROUTES.EMPLOYEE_DASHBOARD} element={<EmployeeDashboard />} />
      </Route>
    </Routes>
  )
}
