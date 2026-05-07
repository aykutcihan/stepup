import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { login } from '@/services/authService'
import { getErrorMessage } from '@/utils/getErrorMessage'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'


const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
})

type FormData = z.infer<typeof schema>

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  async function onSubmit(data: FormData) {
    try {
      await login(data)
    } catch (err) {
      console.error(getErrorMessage(err))
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="email" {...register('email')} placeholder="Email" />
      {errors.email && <p>{errors.email.message}</p>}

      <input type="password" {...register('password')} placeholder="Password" />
      {errors.password && <p>{errors.password.message}</p>}

      <button type="submit">Login</button>
    </form>
  )
}
