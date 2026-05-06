import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { createInvitation } from '@/services/invitationService'
import { getErrorMessage } from '@/utils/getErrorMessage'
import { useState } from 'react'

const schema = z.object({
  email: z.string().email('Invalid email address'),
  role: z.enum(['employee', 'manager', 'hr_admin']),
})

type FormData = z.infer<typeof schema>

export default function InviteUserPage() {
  const [pageError, setPageError] = useState('')
  const [success, setSuccess] = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    try {
      await createInvitation(data)
      setSuccess(true)
      reset()
    } catch (err) {
      setPageError(getErrorMessage(err))
    }
  }

  return (
    <div>
      <h1>Invite User</h1>
      {pageError && <p>{pageError}</p>}
      {success && <p>Invitation sent successfully.</p>}
      <form onSubmit={handleSubmit(onSubmit)}>
        <input {...register('email')} placeholder="Email" />
        {errors.email && <p>{errors.email.message}</p>}
        <select {...register('role')}>
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="hr_admin">HR Admin</option>
        </select>
        {errors.role && <p>{errors.role.message}</p>}
        <button type="submit">Send Invitation</button>
      </form>
    </div>
  )
}
