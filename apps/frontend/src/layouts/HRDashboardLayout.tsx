import { Outlet, NavLink, Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'

export default function HRDashboardLayout() {
  const user = useAuthStore((state) => state.user)
  const clearUser = useAuthStore((state) => state.clearUser)
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    clearUser()
    navigate(ROUTES.LOGIN)
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <nav className="bg-blue-800 text-white px-6 py-3 flex items-center justify-between shadow-md">
        <span className="text-xl font-bold tracking-tight">StepUp</span>
        <div className="flex items-center gap-3">
          <Link to={ROUTES.PROFILE} className="text-sm text-blue-200 hover:text-white transition-colors">
            {user?.first_name} {user?.last_name}
          </Link>
          <span className="text-xs bg-blue-600 px-2.5 py-0.5 rounded-full font-medium uppercase tracking-wide">
            HR Admin
          </span>
          <button
            onClick={handleLogout}
            className="text-sm bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition-colors font-medium"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="flex flex-1">
        <aside className="w-52 bg-white border-r border-gray-200 shadow-sm">
          <nav className="flex flex-col p-4 gap-1">
            <NavLink
              to={ROUTES.HR_DASHBOARD}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Dashboard
            </NavLink>
            <NavLink
              to={ROUTES.HR_USERS}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Users
            </NavLink>
            <NavLink
              to={ROUTES.HR_DEPARTMENTS}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Departments
            </NavLink>
            <NavLink
              to={ROUTES.HR_TEMPLATES}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Templates
            </NavLink>
          </nav>
        </aside>

        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
