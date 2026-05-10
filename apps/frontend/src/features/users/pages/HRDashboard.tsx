import { useEffect, useState } from 'react'
import { getUsers, deactivateUser } from '@/features/users/services/userService'
import { useAuthStore } from '@/stores/authStore'
import { ROLE_LABELS } from '@/constants/userRoles'
import type { components } from '@/types/api'

type UserResponse = components['schemas']['UserResponse']

export default function HRDashboard() {
  const currentUser = useAuthStore((state) => state.user)
  const [users, setUsers] = useState<UserResponse[]>([])

  useEffect(() => {
    getUsers().then(setUsers).catch(() => {})
  }, [])

  async function handleDeactivate(id: string) {
    await deactivateUser(id)
    setUsers((prev) => prev.filter((u) => u.id !== id))
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Team members</h2>
        <p className="text-sm text-gray-500 mt-0.5">Manage your organisation's users.</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50 text-left">
              <th className="px-5 py-3.5 font-medium text-gray-600">Name</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Email</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Role</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3.5 font-medium text-gray-900">
                  {u.first_name} {u.last_name}
                  {u.id === currentUser?.id && (
                    <span className="ml-2 text-xs text-blue-600 font-normal">(you)</span>
                  )}
                </td>
                <td className="px-5 py-3.5 text-gray-600">{u.email}</td>
                <td className="px-5 py-3.5">
                  <span className="inline-block text-xs bg-blue-50 text-blue-700 border border-blue-100 px-2 py-0.5 rounded-full font-medium">
                    {ROLE_LABELS[u.role] ?? u.role}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-right">
                  {u.id !== currentUser?.id && (
                    <button
                      onClick={() => handleDeactivate(u.id)}
                      className="text-xs text-red-600 hover:text-red-800 border border-red-200 hover:border-red-300 px-3 py-1.5 rounded-lg transition-colors"
                    >
                      Deactivate
                    </button>
                  )}
                </td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td colSpan={4} className="px-5 py-8 text-center text-gray-400 text-sm">
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
