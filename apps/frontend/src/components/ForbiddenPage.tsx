import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'

export default function ForbiddenPage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)

  function handleBack() {
    if (!user) {
      navigate(ROUTES.LOGIN)
      return
    }
    if (user.role === USER_ROLES.HR_ADMIN) navigate(ROUTES.HR_DASHBOARD)
    else if (user.role === USER_ROLES.MANAGER) navigate(ROUTES.MANAGER_DASHBOARD)
    else navigate(ROUTES.EMPLOYEE_DASHBOARD)
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="text-center">
        <p className="text-8xl font-extrabold text-blue-800 mb-4">403</p>
        <h1 className="text-xl font-semibold text-gray-900 mb-2">Access denied</h1>
        <p className="text-sm text-gray-500 mb-8">
          You do not have permission to access this page.
        </p>
        <button
          onClick={handleBack}
          className="bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium px-5 py-2.5 rounded-lg transition-colors"
        >
          Go to my dashboard
        </button>
      </div>
    </div>
  )
}
