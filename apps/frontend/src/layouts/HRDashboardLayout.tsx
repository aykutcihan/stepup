import { useState, useRef, useEffect } from 'react'
import { Outlet, NavLink, Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { useThemeStore, type Theme } from '@/stores/themeStore'
import { ROUTES } from '@/constants/routes'

const THEME_OPTIONS: { value: Theme; label: string }[] = [
  { value: 'light', label: 'Light' },
  { value: 'dark', label: 'Dark' },
  { value: 'system', label: 'System' },
]

export default function HRDashboardLayout() {
  const user = useAuthStore((state) => state.user)
  const clearUser = useAuthStore((state) => state.clearUser)
  const { theme, setTheme } = useThemeStore()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const [showTheme, setShowTheme] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false)
        setShowTheme(false)
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

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
    }`

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-gray-900 flex flex-col">
      <nav className="bg-blue-800 dark:bg-gray-950 text-white px-6 py-3 flex items-center justify-between shadow-md">
        <Link to={ROUTES.HR_DASHBOARD} className="text-xl font-bold tracking-tight hover:opacity-80 transition-opacity">StepUp</Link>
        <div className="flex items-center gap-3">
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => { setOpen((v) => !v); setShowTheme(false) }}
              className="flex flex-col justify-center items-center gap-1 w-8 h-8 rounded-lg hover:bg-white/10 transition-colors"
              aria-label="User menu"
            >
              <span className="block w-4 h-0.5 bg-white rounded" />
              <span className="block w-4 h-0.5 bg-white rounded" />
              <span className="block w-4 h-0.5 bg-white rounded" />
            </button>

            {open && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
                <div className="px-4 py-2 border-b border-gray-100 dark:border-gray-700">
                  <p className="text-xs font-medium text-gray-900 dark:text-gray-100">{user?.first_name} {user?.last_name}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email}</p>
                </div>

                <Link
                  to={ROUTES.PROFILE}
                  onClick={() => setOpen(false)}
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  My Profile
                </Link>

                <button
                  onClick={() => setShowTheme((v) => !v)}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center justify-between"
                >
                  <span>Theme</span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">{showTheme ? '▲' : '▼'}</span>
                </button>

                {showTheme && (
                  <div className="px-3 pb-2 flex gap-1">
                    {THEME_OPTIONS.map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => { setTheme(opt.value); setShowTheme(false) }}
                        className={`flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors ${
                          theme === opt.value
                            ? 'bg-blue-600 text-white'
                            : 'text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                )}

                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border-t border-gray-100 dark:border-gray-700"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      <div className="flex flex-1">
        <aside className="w-52 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 shadow-sm">
          <nav className="flex flex-col p-4 gap-1">
            <NavLink to={ROUTES.HR_DASHBOARD} className={navLinkClass}>Dashboard</NavLink>
            <NavLink to={ROUTES.HR_USERS} className={navLinkClass}>Users</NavLink>
            <NavLink to={ROUTES.HR_DEPARTMENTS} className={navLinkClass}>Departments</NavLink>
            <NavLink to={ROUTES.HR_TEMPLATES} className={navLinkClass}>Templates</NavLink>
            <NavLink to={ROUTES.HR_PLAN_NEW} className={navLinkClass}>Plans</NavLink>
            <NavLink to={ROUTES.HR_AUDIT} className={navLinkClass}>Audit Trail</NavLink>
            <NavLink to={ROUTES.HR_REPORTS} className={navLinkClass}>Reports</NavLink>
          </nav>
        </aside>

        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
