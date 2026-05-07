import { useRegisterForm } from '@/features/invitation/hooks/useRegisterForm'

export default function RegisterPage() {
  const { registerField, handleSubmit, errors, onSubmit, email, pageError } = useRegisterForm()

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
