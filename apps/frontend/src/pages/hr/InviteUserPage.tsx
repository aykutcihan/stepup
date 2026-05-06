import { useEffect, useState } from 'react'
import { format } from 'date-fns'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import type { components } from '@/types/api'
import { createInvitation, getInvitations, resendInvitation } from '@/services/invitationService'
import { getErrorMessage } from '@/utils/getErrorMessage'

type InvitationResponse = components['schemas']['InvitationResponse']

const schema = z.object({
  email: z.string().email('Invalid email address'),
  role: z.enum(['employee', 'manager', 'hr_admin']),
})

type FormData = z.infer<typeof schema>

export default function InviteUserPage() {
  const [pageError, setPageError] = useState('')
  const [success, setSuccess] = useState(false)
  const [invitations, setInvitations] = useState<InvitationResponse[]>([])

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  useEffect(() => {
    getInvitations()
      .then((data) => setInvitations(data))
      .catch((err) => setPageError(getErrorMessage(err)))
  }, [])

  const handleResend = async (id: string) => {
    try {
      await resendInvitation(id)
      getInvitations().then((data) => setInvitations(data))
    } catch (err) {
      setPageError(getErrorMessage(err))
    }
  }

  const onSubmit = async (data: FormData) => {
    try {
      await createInvitation(data)
      setSuccess(true)
      reset()
      getInvitations().then((data) => setInvitations(data))
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

      <h2>Pending Invitations</h2>
      <ul>
        {invitations.map((inv) => (
          <li key={inv.id}>
            {inv.email} — {inv.role} — {format(new Date(inv.expires_at), 'dd/MM/yyyy')}
            <button onClick={() => handleResend(inv.id)}>Resend</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
