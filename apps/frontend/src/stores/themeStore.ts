import { create } from 'zustand'

export type Theme = 'light' | 'dark' | 'system'

const KEY = 'stepup-theme'

function readTheme(): Theme {
  try {
    const v = localStorage.getItem(KEY)
    if (v === 'light' || v === 'dark' || v === 'system') return v
  } catch {}
  return 'system'
}

export function applyTheme(theme: Theme) {
  const isDark =
    theme === 'dark' ||
    (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
  document.documentElement.classList.toggle('dark', isDark)
}

// Apply immediately when this module loads (before React mounts)
applyTheme(readTheme())

// Keep dark class in sync when OS preference changes and theme is 'system'
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  if (readTheme() === 'system') applyTheme('system')
})

interface ThemeState {
  theme: Theme
  setTheme: (theme: Theme) => void
}

export const useThemeStore = create<ThemeState>()((set) => ({
  theme: readTheme(),
  setTheme: (theme) => {
    localStorage.setItem(KEY, theme)
    applyTheme(theme)
    set({ theme })
  },
}))
