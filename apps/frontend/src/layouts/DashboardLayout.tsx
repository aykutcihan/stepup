import { Outlet } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { ROLE_LABELS } from '@/constants/userRoles'

export default function DashboardLayout() {
  const user = useAuthStore((state) => state.user)
  const clearUser = useAuthStore((state) => state.clearUser)
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    clearUser()
    navigate(ROUTES.LOGIN)
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-blue-800 text-white px-6 py-3 flex items-center justify-between shadow-md">
        <span className="text-xl font-bold tracking-tight">StepUp</span>
        <div className="flex items-center gap-3">
          <span className="text-sm text-blue-200">
            {user?.first_name} {user?.last_name}
          </span>
          <span className="text-xs bg-blue-600 px-2.5 py-0.5 rounded-full font-medium uppercase tracking-wide">
            {ROLE_LABELS[user?.role ?? ''] ?? user?.role}
          </span>
          <button
            onClick={handleLogout}
            className="text-sm bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition-colors font-medium"
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  )
}
