import { useState, useRef, useEffect } from 'react'
import { Outlet, NavLink, Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'

export default function HRDashboardLayout() {
  const user = useAuthStore((state) => state.user)
  const clearUser = useAuthStore((state) => state.clearUser)
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

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
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setOpen((v) => !v)}
              className="flex flex-col justify-center items-center gap-1 w-8 h-8 rounded-lg hover:bg-white/10 transition-colors"
              aria-label="User menu"
            >
              <span className="block w-4 h-0.5 bg-white rounded" />
              <span className="block w-4 h-0.5 bg-white rounded" />
              <span className="block w-4 h-0.5 bg-white rounded" />
            </button>

            {open && (
              <div className="absolute right-0 mt-2 w-44 bg-white rounded-xl shadow-lg border border-gray-200 py-1 z-50">
                <div className="px-4 py-2 border-b border-gray-100">
                  <p className="text-xs font-medium text-gray-900">{user?.first_name} {user?.last_name}</p>
                  <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                </div>
                <Link
                  to={ROUTES.PROFILE}
                  onClick={() => setOpen(false)}
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  My Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
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
            <NavLink
              to={ROUTES.HR_PLAN_NEW}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Plans
            </NavLink>
            <NavLink
              to={ROUTES.HR_AUDIT}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              Audit Trail
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
