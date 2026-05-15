import { useEffect } from 'react'
import { useThemeStore } from '@/stores/themeStore'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useThemeStore((state) => state.theme)

  useEffect(() => {
    const root = document.documentElement

    function applyTheme(t: string) {
      if (t === 'dark') {
        root.classList.add('dark')
      } else if (t === 'light') {
        root.classList.remove('dark')
      } else {
        root.classList.toggle('dark', window.matchMedia('(prefers-color-scheme: dark)').matches)
      }
    }

    applyTheme(theme)

    if (theme === 'system') {
      const mq = window.matchMedia('(prefers-color-scheme: dark)')
      const handler = (e: MediaQueryListEvent) => root.classList.toggle('dark', e.matches)
      mq.addEventListener('change', handler)
      return () => mq.removeEventListener('change', handler)
    }
  }, [theme])

  return <>{children}</>
}
