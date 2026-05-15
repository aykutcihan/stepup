import apiClient from '@/lib/apiClient'
import { API } from '@/constants/apiEndpoints'

export type AuditActionType =
  | 'user.invited'
  | 'user.registered'
  | 'user.deactivated'
  | 'user.reactivated'
  | 'user.updated'
  | 'plan.created'
  | 'plan.task_cancelled'
  | 'task.started'
  | 'task.completed'
  | 'task.approved'
  | 'task.returned'

export type AuditEntityType = 'user' | 'invitation' | 'plan' | 'task'

export interface AuditLog {
  id: string
  actor_id: string
  action: AuditActionType
  entity_type: AuditEntityType
  entity_id: string
  detail: string | null
  created_at: string
}

export interface AuditLogListResponse {
  items: AuditLog[]
  total: number
  page: number
  page_size: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

export interface AuditLogFilters {
  action?: AuditActionType
  entity_type?: AuditEntityType
  actor_id?: string
  date_from?: string
  date_to?: string
  page?: number
  page_size?: number
}

export async function getAuditLogs(filters?: AuditLogFilters): Promise<AuditLogListResponse> {
  const res = await apiClient.get(API.AUDIT.LIST, { params: filters })
  return res.data
}
