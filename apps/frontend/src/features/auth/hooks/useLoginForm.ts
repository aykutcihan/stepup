import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { login, getMe } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'
import { ERROR_MESSAGES } from '@/constants/errorMessages'
import { getErrorMessage } from '@/utils/getErrorMessage'
import { loginSchema, type LoginFormData } from '@/features/auth/schemas/loginSchema'

export function useLoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const setUser = useAuthStore((state) => state.setUser)

  const errorCode = searchParams.get('error')
  const pageError = errorCode ? (ERROR_MESSAGES[errorCode] ?? 'Something went wrong.') : ''

  async function onSubmit(data: LoginFormData) {
    try {
      await login(data)
      const user = await getMe()
      setUser(user)
      if (user.role === USER_ROLES.HR_ADMIN) navigate(ROUTES.HR_DASHBOARD)
      else if (user.role === USER_ROLES.MANAGER) navigate(ROUTES.MANAGER_DASHBOARD)
      else navigate(ROUTES.EMPLOYEE_DASHBOARD)
    } catch (err) {
      console.error(getErrorMessage(err))
    }
  }

  return { register, handleSubmit, errors, onSubmit, pageError }
}
