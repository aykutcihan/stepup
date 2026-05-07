import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { validateInvitation, register } from '@/features/auth/services/authService'
import { ERROR_MESSAGES } from '@/constants/errorMessages'
import { ROUTES } from '@/constants/routes'
import { registerSchema, type RegisterFormData } from '@/features/invitation/schemas/registerSchema'

export function useRegisterForm() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [pageError, setPageError] = useState('')
  const token = searchParams.get('token') ?? ''

  const { register: registerField, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
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

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await register({ token, ...data })
      navigate(ROUTES.LOGIN)
    } catch (err: unknown) {
      const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
      setPageError(ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong. Please try again.')
    }
  }

  return { registerField, handleSubmit, errors, onSubmit, email, pageError }
}
