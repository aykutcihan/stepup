import { useEffect } from 'react'
import { getMe } from '@/features/auth/services/authService'
import { useAuthStore } from '@/stores/authStore'

export function useAuthInit() {
  const setUser = useAuthStore((state) => state.setUser)
  const clearUser = useAuthStore((state) => state.clearUser)
  const setLoading = useAuthStore((state) => state.setLoading)

  useEffect(() => {
    getMe()
      .then(setUser)
      .catch(() => clearUser())
      .finally(() => setLoading(false))
  }, [setUser, clearUser, setLoading])
}
