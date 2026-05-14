import apiClient from '@/lib/apiClient'
import { API } from '@/constants/apiEndpoints'

export interface HRDashboardStats {
  active_users: number
  active_plans: number
  active_departments: number
  pending_approvals: number
}

export interface ManagerDashboardStats {
  active_plans: number
  pending_approvals: number
  total_employees: number
}

export interface EmployeeDashboardStats {
  total_tasks: number
  approved_tasks: number
  completed_tasks: number
  in_progress_tasks: number
  next_deadline: string | null
}

export async function getHRDashboard(): Promise<HRDashboardStats> {
  const res = await apiClient.get(API.DASHBOARD.HR)
  return res.data
}

export async function getManagerDashboard(): Promise<ManagerDashboardStats> {
  const res = await apiClient.get(API.DASHBOARD.MANAGER)
  return res.data
}

export async function getEmployeeDashboard(): Promise<EmployeeDashboardStats> {
  const res = await apiClient.get(API.DASHBOARD.EMPLOYEE)
  return res.data
}
