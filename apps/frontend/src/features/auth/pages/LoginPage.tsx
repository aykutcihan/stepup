import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { login, getMe } from '@/features/auth/services/authService'
import { getErrorMessage } from '@/utils/getErrorMessage'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { USER_ROLES } from '@/constants/userRoles'
import { ERROR_MESSAGES } from '@/constants/errorMessages'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
})

type FormData = z.infer<typeof schema>

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const setUser = useAuthStore((state) => state.setUser)

  const errorCode = searchParams.get('error')
  const pageError = errorCode ? (ERROR_MESSAGES[errorCode] ?? 'Something went wrong.') : ''

  async function onSubmit(data: FormData) {
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

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {pageError && <p>{pageError}</p>}
      <input type="email" {...register('email')} placeholder="Email" />
      {errors.email && <p>{errors.email.message}</p>}

      <input type="password" {...register('password')} placeholder="Password" />
      {errors.password && <p>{errors.password.message}</p>}

      <button type="submit">Login</button>
    </form>
  )
}
