import { useState, useRef, useEffect } from 'react'
import { Outlet, Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { useThemeStore, type Theme } from '@/stores/themeStore'
import { useLanguageStore, type Language } from '@/stores/languageStore'
import { useTranslation } from '@/i18n/useTranslation'
import { ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'

export default function DashboardLayout() {
  const user = useAuthStore((state) => state.user)
  const clearUser = useAuthStore((state) => state.clearUser)
  const { theme, setTheme } = useThemeStore()
  const { language, setLanguage } = useLanguageStore()
  const t = useTranslation()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const [showTheme, setShowTheme] = useState(false)
  const [showLanguage, setShowLanguage] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  const THEME_OPTIONS: { value: Theme; label: string }[] = [
    { value: 'light', label: t.theme.light },
    { value: 'dark', label: t.theme.dark },
    { value: 'system', label: t.theme.system },
  ]

  const LANGUAGE_OPTIONS: { value: Language; label: string }[] = [
    { value: 'en', label: t.languages.en },
    { value: 'nl', label: t.languages.nl },
  ]

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false)
        setShowTheme(false)
        setShowLanguage(false)
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
    <div className="min-h-screen bg-slate-50 dark:bg-gray-900">
      <nav className="bg-blue-800 dark:bg-gray-950 text-white px-6 py-3 flex items-center justify-between shadow-md">
        <Link
          to={user?.role === USER_ROLES.MANAGER ? ROUTES.MANAGER_DASHBOARD : ROUTES.EMPLOYEE_DASHBOARD}
          className="text-xl font-bold tracking-tight hover:opacity-80 transition-opacity"
        >StepUp</Link>
        <div className="flex items-center gap-3">
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => { setOpen((v) => !v); setShowTheme(false); setShowLanguage(false) }}
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
                  to={user?.role === USER_ROLES.MANAGER ? ROUTES.MANAGER_PROFILE : ROUTES.EMPLOYEE_PROFILE}
                  onClick={() => setOpen(false)}
                  className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  {t.menu.myProfile}
                </Link>

                <button
                  onClick={() => { setShowTheme((v) => !v); setShowLanguage(false) }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center justify-between"
                >
                  <span>{t.menu.appearance}</span>
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
                  onClick={() => { setShowLanguage((v) => !v); setShowTheme(false) }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center justify-between"
                >
                  <span>{t.menu.language}</span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">{showLanguage ? '▲' : '▼'}</span>
                </button>

                {showLanguage && (
                  <div className="px-3 pb-2 flex gap-1">
                    {LANGUAGE_OPTIONS.map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => { setLanguage(opt.value); setShowLanguage(false) }}
                        className={`flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors ${
                          language === opt.value
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
                  {t.menu.logout}
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  )
}
