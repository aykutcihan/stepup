import { useAuthStore } from '@/stores/authStore'
import { ROLE_LABELS } from '@/constants/userRoles'
import { useUsersPage } from '@/features/users/hooks/useUsersPage'
import KebabMenu from '@/components/KebabMenu'
import type { components } from '@/types/api'

type UserRole = components['schemas']['UserRole']

export default function UsersPage() {
  const currentUser = useAuthStore((state) => state.user)
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
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Users</h2>
        <p className="text-sm text-gray-500 mt-0.5">Manage users, roles and department assignments.</p>
      </div>

      <div className="flex gap-3 mb-6">
        <select
          value={filterRole}
          onChange={(e) => setFilterRole(e.target.value as UserRole | '')}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All roles</option>
          <option value="hr_admin">HR Admin</option>
          <option value="manager">Manager</option>
          <option value="employee">Employee</option>
        </select>

        <select
          value={filterDepartmentId}
          onChange={(e) => setFilterDepartmentId(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All departments</option>
          {activeDepartments.map((d) => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as 'active' | 'inactive' | '')}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50 text-left">
              <th className="px-5 py-3.5 font-medium text-gray-600 rounded-tl-xl">Name</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Email</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Role</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Department</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Status</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 text-right rounded-tr-xl">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredUsers.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3.5 font-medium text-gray-900">
                  {u.first_name} {u.last_name}
                  {u.id === currentUser?.id && (
                    <span className="ml-2 text-xs text-blue-600 font-normal">(you)</span>
                  )}
                </td>
                <td className="px-5 py-3.5 text-gray-600">{u.email}</td>
                <td className="px-5 py-3.5">
                  {u.id === currentUser?.id ? (
                    <span className="inline-block text-xs bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-full font-medium">
                      {ROLE_LABELS[u.role] ?? u.role}
                    </span>
                  ) : (
                    <select
                      value={u.role}
                      onChange={(e) => handleChangeRole(u.id, e.target.value as UserRole)}
                      className="border border-gray-200 rounded px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                    className="border border-gray-200 rounded px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">No department</option>
                    {activeDepartments.map((d) => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </td>
                <td className="px-5 py-3.5">
                  <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium border ${
                    u.is_active
                      ? 'bg-green-50 text-green-700 border-green-100'
                      : 'bg-gray-100 text-gray-500 border-gray-200'
                  }`}>
                    {u.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-right">
                  {u.id !== currentUser?.id && (
                    <KebabMenu items={[
                      u.is_active
                        ? { label: 'Deactivate', onClick: () => handleDeactivate(u.id), variant: 'danger' }
                        : { label: 'Reactivate', onClick: () => handleReactivate(u.id), variant: 'success' },
                    ]} />
                  )}
                </td>
              </tr>
            ))}
            {filteredUsers.length === 0 && (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-gray-400 text-sm">
                  No users found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
