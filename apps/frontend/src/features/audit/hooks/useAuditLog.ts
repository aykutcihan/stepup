import { useEffect, useState } from 'react'
import {
  getAuditLogs,
  type AuditLog,
  type AuditLogFilters,
  type AuditLogListResponse,
} from '@/features/audit/services/auditService'

const DEFAULT_PAGE_SIZE = 50

export function useAuditLog(filters: AuditLogFilters = {}) {
  const [data, setData] = useState<AuditLogListResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const filtersKey = JSON.stringify(filters)

  useEffect(() => {
    setLoading(true)
    getAuditLogs({ page_size: DEFAULT_PAGE_SIZE, ...filters })
      .then(setData)
      .finally(() => setLoading(false))
  }, [filtersKey])

  return {
    logs: data?.items ?? [] as AuditLog[],
    total: data?.total ?? 0,
    page: data?.page ?? 1,
    totalPages: data?.total_pages ?? 1,
    hasNext: data?.has_next ?? false,
    hasPrev: data?.has_prev ?? false,
    loading,
  }
}
