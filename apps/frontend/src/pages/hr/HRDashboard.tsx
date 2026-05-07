import { useNavigate } from 'react-router-dom'
import { logout } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

export default function HRDashboard() {
  const navigate = useNavigate()
  const clearUser = useAuthStore((state) => state.clearUser)

  async function handleLogout() {
    await logout()
    clearUser()
    navigate('/login')
  }

  return (
    <div>
      <h1>HR Dashboard</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  )
}
