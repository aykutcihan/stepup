import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { z } from 'zod'
import { validateInvitation, register } from '@/features/auth/services/authService'
import { ERROR_MESSAGES } from '@/constants/errorMessages'
import { ROUTES } from '@/constants/routes'

const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

type FormData = z.infer<typeof schema>

export default function RegisterPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [pageError, setPageError] = useState('')
  const token = searchParams.get('token') ?? ''

  const { register: registerField, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  useEffect(() => {
    if (!token) {
      setPageError('Invalid or missing invitation link.')
      return
    }
    validateInvitation(token)
      .then((data) => setEmail(data.email))
      .catch((err) => {
        const code = err.response?.data?.error_code
        setPageError(ERROR_MESSAGES[code] ?? 'This invitation link is invalid.')
      })
  }, [token])

  const onSubmit = async (data: FormData) => {
    try {
      await register({ token, ...data })
      navigate(ROUTES.LOGIN)
    } catch (err: unknown) {
      const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
      setPageError(ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong. Please try again.')
    }
  }

  return (
    <div>
      <h1>Complete Registration</h1>
      {pageError && <p>{pageError}</p>}
      <form onSubmit={handleSubmit(onSubmit)}>
        <input value={email} readOnly placeholder="Email" />
        <input {...registerField('first_name')} placeholder="First name" />
        {errors.first_name && <p>{errors.first_name.message}</p>}
        <input {...registerField('last_name')} placeholder="Last name" />
        {errors.last_name && <p>{errors.last_name.message}</p>}
        <input {...registerField('password')} type="password" placeholder="Password" />
        {errors.password && <p>{errors.password.message}</p>}
        <button type="submit">Register</button>
      </form>
    </div>
  )
}
