import { useEffect, useState } from 'react'
import { getHRDashboard, type HRDashboardStats } from '@/features/dashboard/services/dashboardService'

export function useHRDashboard() {
  const [stats, setStats] = useState<HRDashboardStats | null>(null)

  useEffect(() => {
    getHRDashboard().then(setStats).catch(() => {})
  }, [])

  return { stats }
}
