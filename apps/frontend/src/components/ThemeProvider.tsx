import { useEffect } from 'react'
import { useThemeStore, applyTheme, readTheme } from '@/stores/themeStore'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useThemeStore((s) => s.theme)

  // Apply theme whenever store changes — this is the React-side guarantee
  useEffect(() => {
    applyTheme(theme)
  }, [theme])

  // Apply on mount in case module-level call ran before DOM was ready
  useEffect(() => {
    applyTheme(readTheme())
  }, [])

  // System mode: keep in sync with OS changes
  useEffect(() => {
    if (theme !== 'system') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => applyTheme('system')
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [theme])

  return <>{children}</>
}
