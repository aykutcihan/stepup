import { useCallback, useEffect, useState } from 'react'
import {
  getCompletionTime,
  getTaskCompletionRates,
  getBottlenecks,
  type DepartmentCompletionRow,
  type TemplateCompletionRow,
  type BottleneckRow,
  type ReportFilters,
} from '@/features/reports/services/reportsService'

export function useReports(filters: ReportFilters) {
  const [completionTime, setCompletionTime] = useState<DepartmentCompletionRow[]>([])
  const [taskRates, setTaskRates] = useState<TemplateCompletionRow[]>([])
  const [bottlenecks, setBottlenecks] = useState<BottleneckRow[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    const [ct, tr, bn] = await Promise.all([
      getCompletionTime(filters),
      getTaskCompletionRates(filters),
      getBottlenecks(filters),
    ])
    setCompletionTime(ct)
    setTaskRates(tr)
    setBottlenecks(bn)
    setLoading(false)
  }, [filters.start_date, filters.end_date])

  useEffect(() => { load() }, [load])

  return { completionTime, taskRates, bottlenecks, loading, reload: load }
}
