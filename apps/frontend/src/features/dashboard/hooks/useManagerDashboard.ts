import { useEffect, useState } from 'react'
import { getManagerDashboard, type ManagerDashboardStats } from '@/features/dashboard/services/dashboardService'

export function useManagerDashboard() {
  const [stats, setStats] = useState<ManagerDashboardStats | null>(null)

  useEffect(() => {
    getManagerDashboard().then(setStats).catch(() => {})
  }, [])

  return { stats }
}
