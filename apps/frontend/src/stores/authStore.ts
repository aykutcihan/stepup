import { create } from 'zustand'
import type { components } from '@/types/api'

type User = components['schemas']['UserResponse']

type AuthStore = {
  user: User | null
  isLoading: boolean
  setUser: (user: User) => void
  clearUser: () => void
  setLoading: (isLoading: boolean) => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isLoading: true,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
  setLoading: (isLoading) => set({ isLoading }),
}))
