import { format } from 'date-fns'
import { useInviteUserForm } from '@/features/invitation/hooks/useInviteUserForm'
import { ROLE_LABELS } from '@/constants/userRoles'

const inputCls = 'w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500'

export default function InviteUserPage() {
  const { register, handleSubmit, errors, onSubmit, handleResend, invitations, departments, pageError, success } = useInviteUserForm()

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Invite User</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Send an invitation email to onboard a new user.</p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5 mb-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input {...register('email')} placeholder="name@company.com" className={inputCls} />
            {errors.email && <p className="text-xs text-red-600 dark:text-red-400 mt-1">{errors.email.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
            <select {...register('role')} className={inputCls}>
              <option value="employee">Employee</option>
              <option value="manager">Manager</option>
              <option value="hr_admin">HR Admin</option>
            </select>
            {errors.role && <p className="text-xs text-red-600 dark:text-red-400 mt-1">{errors.role.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Department</label>
            <select {...register('department_id')} className={inputCls}>
              <option value="">No department</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>

          {pageError && (
            <p className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-800 rounded-lg px-3.5 py-2">
              {pageError}
            </p>
          )}
          {success && (
            <p className="text-sm text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800 rounded-lg px-3.5 py-2">
              Invitation sent successfully.
            </p>
          )}

          <button type="submit" className="bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
            Send Invitation
          </button>
        </form>
      </div>

      <div>
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Pending Invitations</h3>
        {invitations.length === 0 ? (
          <p className="text-sm text-gray-400 dark:text-gray-500">No pending invitations.</p>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm divide-y divide-gray-100 dark:divide-gray-700">
            {invitations.map((inv) => (
              <div key={inv.id} className="px-5 py-3.5 flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{inv.email}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {ROLE_LABELS[inv.role] ?? inv.role} · Expires {format(new Date(inv.expires_at), 'dd MMM yyyy')}
                  </p>
                </div>
                <button
                  onClick={() => handleResend(inv.id)}
                  className="text-xs border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 text-gray-600 dark:text-gray-400 font-medium px-3 py-1.5 rounded-lg transition-colors shrink-0"
                >
                  Resend
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
