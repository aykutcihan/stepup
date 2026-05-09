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

const STORAGE_KEY = 'auth_user'

function loadUser(): User | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as User) : null
  } catch {
    return null
  }
}

const cachedUser = loadUser()

export const useAuthStore = create<AuthStore>((set) => ({
  user: cachedUser,
  isLoading: cachedUser === null,
  setUser: (user) => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(user))
    set({ user })
  },
  clearUser: () => {
    sessionStorage.removeItem(STORAGE_KEY)
    set({ user: null })
  },
  setLoading: (isLoading) => set({ isLoading }),
}))
