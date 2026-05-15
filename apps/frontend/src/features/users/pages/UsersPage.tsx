import { Link } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { ROLE_LABELS } from '@/constants/userRoles'
import { useUsersPage } from '@/features/users/hooks/useUsersPage'
import KebabMenu from '@/components/KebabMenu'
import { ROUTES } from '@/constants/routes'
import { useTranslation } from '@/i18n/useTranslation'
import type { components } from '@/types/api'

type UserRole = components['schemas']['UserRole']

export default function UsersPage() {
  const currentUser = useAuthStore((state) => state.user)
  const t = useTranslation()
  const {
    filteredUsers,
    activeDepartments,
    filterRole,
    setFilterRole,
    filterDepartmentId,
    setFilterDepartmentId,
    filterStatus,
    setFilterStatus,
    handleAssignDepartment,
    handleChangeRole,
    handleDeactivate,
    handleReactivate,
  } = useUsersPage()

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">{t.users.title}</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{t.users.subtitle}</p>
        </div>
        <Link
          to={ROUTES.HR_INVITE_USER}
          className="text-sm bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {t.users.inviteUser}
        </Link>
      </div>

      <div className="flex gap-3 mb-6">
        <select
          value={filterRole}
          onChange={(e) => setFilterRole(e.target.value as UserRole | '')}
          className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">{t.users.allRoles}</option>
          <option value="hr_admin">HR Admin</option>
          <option value="manager">Manager</option>
          <option value="employee">Employee</option>
        </select>

        <select
          value={filterDepartmentId}
          onChange={(e) => setFilterDepartmentId(e.target.value)}
          className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">{t.users.allDepartments}</option>
          {activeDepartments.map((d) => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as 'active' | 'inactive' | '')}
          className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">{t.users.allStatuses}</option>
          <option value="active">{t.users.active}</option>
          <option value="inactive">{t.users.inactive}</option>
        </select>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50 text-left">
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400 rounded-tl-xl">{t.users.columns.name}</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400">{t.users.columns.email}</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400">{t.users.columns.role}</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400">{t.users.columns.department}</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400">{t.users.columns.status}</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400 text-right rounded-tr-xl">{t.users.columns.actions}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {filteredUsers.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50 dark:hover:bg-gray-700/50 transition-colors">
                <td className="px-5 py-3.5 font-medium text-gray-900 dark:text-gray-100">
                  {u.first_name} {u.last_name}
                  {u.id === currentUser?.id && (
                    <span className="ml-2 text-xs text-blue-600 dark:text-blue-400 font-normal">{t.users.you}</span>
                  )}
                </td>
                <td className="px-5 py-3.5 text-gray-600 dark:text-gray-400">{u.email}</td>
                <td className="px-5 py-3.5">
                  {u.id === currentUser?.id ? (
                    <span className="inline-block text-xs bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-100 dark:border-blue-800 px-2 py-0.5 rounded-full font-medium">
                      {ROLE_LABELS[u.role] ?? u.role}
                    </span>
                  ) : (
                    <select
                      value={u.role}
                      onChange={(e) => handleChangeRole(u.id, e.target.value as UserRole)}
                      className="border border-gray-200 dark:border-gray-600 rounded px-2 py-1 text-xs bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="hr_admin">HR Admin</option>
                      <option value="manager">Manager</option>
                      <option value="employee">Employee</option>
                    </select>
                  )}
                </td>
                <td className="px-5 py-3.5">
                  <select
                    value={u.department_id ?? ''}
                    onChange={(e) => handleAssignDepartment(u.id, e.target.value)}
                    className="border border-gray-200 dark:border-gray-600 rounded px-2 py-1 text-xs bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">{t.users.noDepartment}</option>
                    {activeDepartments.map((d) => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </td>
                <td className="px-5 py-3.5">
                  <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium border ${
                    u.is_active
                      ? 'bg-green-50 text-green-700 border-green-100 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800'
                      : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600'
                  }`}>
                    {u.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-right">
                  {u.id !== currentUser?.id && (
                    <KebabMenu items={[
                      u.is_active
                        ? { label: t.users.actions.deactivate, onClick: () => handleDeactivate(u.id), variant: 'danger' }
                        : { label: t.users.actions.reactivate, onClick: () => handleReactivate(u.id), variant: 'success' },
                    ]} />
                  )}
                </td>
              </tr>
            ))}
            {filteredUsers.length === 0 && (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-gray-400 dark:text-gray-500 text-sm">
                  {t.users.noUsers}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
