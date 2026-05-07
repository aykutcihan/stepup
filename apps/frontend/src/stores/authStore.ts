import { create } from 'zustand'
import type { components } from '@/types/api'

type User = components['schemas']['UserResponse']

type AuthStore = {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}))
