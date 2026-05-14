import { useEffect, useState } from 'react'
import { getEmployeeDashboard, type EmployeeDashboardStats } from '@/features/dashboard/services/dashboardService'

export function useEmployeeDashboard() {
  const [stats, setStats] = useState<EmployeeDashboardStats | null>(null)

  useEffect(() => {
    getEmployeeDashboard().then(setStats).catch(() => {})
  }, [])

  return { stats }
}
