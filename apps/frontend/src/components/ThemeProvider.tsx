import { useEffect, useState } from 'react'
import { useThemeStore, applyTheme, readTheme } from '@/stores/themeStore'

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useThemeStore((s) => s.theme)
  const [htmlClass, setHtmlClass] = useState('')

  useEffect(() => {
    applyTheme(theme)
  }, [theme])

  useEffect(() => {
    applyTheme(readTheme())
  }, [])

  useEffect(() => {
    if (theme !== 'system') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => applyTheme('system')
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [theme])

  // DEBUG: watch html classList changes
  useEffect(() => {
    setHtmlClass(document.documentElement.className)
    const obs = new MutationObserver(() =>
      setHtmlClass(document.documentElement.className)
    )
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
    return () => obs.disconnect()
  }, [])

  return (
    <>
      {children}
      {/* DEBUG OVERLAY — remove after fix confirmed */}
      <div style={{
        position: 'fixed', bottom: 8, right: 8, zIndex: 99999,
        background: 'black', color: 'lime', padding: '6px 10px',
        fontSize: 11, fontFamily: 'monospace', borderRadius: 4,
        pointerEvents: 'none',
      }}>
        store: <b>{theme}</b> | html.class: "<b>{htmlClass}</b>"
      </div>
    </>
  )
}
