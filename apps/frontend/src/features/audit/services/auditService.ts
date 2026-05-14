import apiClient from '@/lib/apiClient'
import { API } from '@/constants/apiEndpoints'

export interface AuditLog {
  id: string
  actor_id: string
  action: string
  entity_type: string
  entity_id: string
  detail: string | null
  created_at: string
}

export async function getAuditLogs(params?: { action?: string; limit?: number; offset?: number }): Promise<AuditLog[]> {
  const res = await apiClient.get(API.AUDIT.LIST, { params })
  return res.data
}
