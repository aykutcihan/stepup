import apiClient from '@/lib/apiClient'
import { API } from '@/constants/apiEndpoints'

export interface DepartmentCompletionRow {
  department_name: string
  total_plans: number
  avg_completion_days: number | null
  avg_completion_days_rounded: number | null
}

export interface TemplateCompletionRow {
  template_name: string
  total_tasks: number
  completed_tasks: number
  completion_rate: number
}

export interface BottleneckRow {
  task_title: string
  returned_count: number
  overdue_count: number
}

export interface ReportFilters {
  start_date?: string
  end_date?: string
}

export async function getCompletionTime(filters: ReportFilters): Promise<DepartmentCompletionRow[]> {
  const res = await apiClient.get(API.REPORTS.COMPLETION_TIME, { params: filters })
  return res.data
}

export async function getTaskCompletionRates(filters: ReportFilters): Promise<TemplateCompletionRow[]> {
  const res = await apiClient.get(API.REPORTS.TASK_COMPLETION_RATES, { params: filters })
  return res.data
}

export async function getBottlenecks(filters: ReportFilters): Promise<BottleneckRow[]> {
  const res = await apiClient.get(API.REPORTS.BOTTLENECKS, { params: filters })
  return res.data
}

export async function downloadCsv(endpoint: string, filename: string, filters: ReportFilters): Promise<void> {
  const res = await apiClient.get(endpoint, {
    params: { ...filters, format: 'csv' },
    responseType: 'blob',
  })
  const url = URL.createObjectURL(new Blob([res.data], { type: 'text/csv' }))
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
