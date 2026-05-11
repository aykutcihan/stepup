import { Routes, Route } from 'react-router-dom'
import RegisterPage from '@/features/invitation/pages/RegisterPage'
import InviteUserPage from '@/features/invitation/pages/InviteUserPage'
import LoginPage from '@/features/auth/pages/LoginPage'
import HRDashboard from '@/features/users/pages/HRDashboard'
import ManagerDashboard from '@/features/users/pages/ManagerDashboard'
import EmployeeDashboard from '@/features/users/pages/EmployeeDashboard'
import ForbiddenPage from '@/components/ForbiddenPage'
import RequireRole from '@/components/RequireRole'
import DashboardLayout from '@/layouts/DashboardLayout'
import { ROUTES, ERROR_ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'
import { useAuthInit } from './useAuthInit'
import HRDashboardLayout from '@/layouts/HRDashboardLayout'
import DepartmentsPage from '@/features/department/pages/DepartmentsPage'
import UsersPage from '@/features/users/pages/UsersPage'
import ProfilePage from '@/features/users/pages/ProfilePage'
import TemplatesPage from '@/features/template/pages/TemplatesPage'
import TemplateDetailPage from '@/features/template/pages/TemplateDetailPage'


export default function App() {
  useAuthInit()

  return (
    <Routes>
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />
      <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
      <Route path={ERROR_ROUTES.FORBIDDEN} element={<ForbiddenPage />} />

      <Route element={<RequireRole roles={[USER_ROLES.HR_ADMIN]} />}>
        <Route element={<HRDashboardLayout />}>
          <Route path={ROUTES.HR_DASHBOARD} element={<HRDashboard />} />
          <Route path={ROUTES.HR_INVITE_USER} element={<InviteUserPage />} />
          <Route path={ROUTES.HR_DEPARTMENTS} element={<DepartmentsPage />} />
          <Route path={ROUTES.HR_USERS} element={<UsersPage />} />
          <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
          <Route path={ROUTES.HR_TEMPLATES} element={<TemplatesPage />} />
          <Route path="/hr/templates/:id" element={<TemplateDetailPage />} />
        </Route>
      </Route>

      <Route element={<RequireRole roles={[USER_ROLES.MANAGER]} />}>
        <Route element={<DashboardLayout />}>
          <Route path={ROUTES.MANAGER_DASHBOARD} element={<ManagerDashboard />} />
          <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
        </Route>
      </Route>

      <Route element={<RequireRole roles={[USER_ROLES.EMPLOYEE]} />}>
        <Route element={<DashboardLayout />}>
          <Route path={ROUTES.EMPLOYEE_DASHBOARD} element={<EmployeeDashboard />} />
          <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
        </Route>
      </Route>
    </Routes>
  )
}
