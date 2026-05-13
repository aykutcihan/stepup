import { format } from 'date-fns'
import { useInviteUserForm } from '@/features/invitation/hooks/useInviteUserForm'

export default function InviteUserPage() {
  const { register, handleSubmit, errors, onSubmit, handleResend, invitations, pageError, success } = useInviteUserForm()

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
