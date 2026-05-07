import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { logout } from '@/services/authService'
import { getUsers, deactivateUser } from '@/services/userService'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type UserResponse = components['schemas']['UserResponse']

export default function HRDashboard() {
  const navigate = useNavigate()
  const clearUser = useAuthStore((state) => state.clearUser)
  const currentUser = useAuthStore((state) => state.user)
  const [users, setUsers] = useState<UserResponse[]>([])

  useEffect(() => {
    getUsers().then(setUsers).catch(() => {})
  }, [])

  async function handleLogout() {
    await logout()
    clearUser()
    navigate(ROUTES.LOGIN)
  }

  async function handleDeactivate(id: string) {
    await deactivateUser(id)
    setUsers((prev) => prev.filter((u) => u.id !== id))
  }

  return (
    <div>
      <h1>HR Dashboard</h1>
      <button onClick={handleLogout}>Logout</button>

      <h2>Users</h2>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.first_name} {u.last_name} — {u.email} — {u.role}
            {u.id !== currentUser?.id && (
              <button onClick={() => handleDeactivate(u.id)}>Deactivate</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
