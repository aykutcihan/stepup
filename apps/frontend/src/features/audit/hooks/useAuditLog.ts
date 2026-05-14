import { useEffect, useState } from 'react'
import { getAuditLogs, type AuditLog } from '@/features/audit/services/auditService'

export function useAuditLog(action?: string) {
  const [logs, setLogs] = useState<AuditLog[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    getAuditLogs({ action: action || undefined, limit: 200 })
      .then(setLogs)
      .finally(() => setLoading(false))
  }, [action])

  return { logs, loading }
}
