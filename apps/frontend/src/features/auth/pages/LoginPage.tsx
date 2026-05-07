import { useLoginForm } from '@/features/auth/hooks/useLoginForm'

export default function LoginPage() {
  const { register, handleSubmit, errors, onSubmit, pageError } = useLoginForm()

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
