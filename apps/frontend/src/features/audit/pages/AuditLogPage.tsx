import { useState } from 'react'
import { format } from 'date-fns'
import { useAuditLog } from '@/features/audit/hooks/useAuditLog'
import { useTranslation } from '@/i18n/useTranslation'
import type { AuditActionType, AuditEntityType } from '@/features/audit/services/auditService'

const ACTION_LABELS: Record<AuditActionType, string> = {
  'user.invited': 'User Invited',
  'user.registered': 'User Registered',
  'user.deactivated': 'User Deactivated',
  'user.reactivated': 'User Reactivated',
  'user.updated': 'User Updated',
  'plan.created': 'Plan Created',
  'plan.task_cancelled': 'Task Cancelled',
  'task.started': 'Task Started',
  'task.completed': 'Task Completed',
  'task.approved': 'Task Approved',
  'task.returned': 'Task Returned',
}

const ACTION_COLORS: Record<AuditActionType, string> = {
  'user.invited': 'text-blue-700 bg-blue-50 dark:text-blue-400 dark:bg-blue-900/30',
  'user.registered': 'text-blue-700 bg-blue-50 dark:text-blue-400 dark:bg-blue-900/30',
  'user.deactivated': 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/30',
  'user.reactivated': 'text-green-700 bg-green-50 dark:text-green-400 dark:bg-green-900/30',
  'user.updated': 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-700',
  'plan.created': 'text-purple-700 bg-purple-50 dark:text-purple-400 dark:bg-purple-900/30',
  'plan.task_cancelled': 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/30',
  'task.started': 'text-amber-700 bg-amber-50 dark:text-amber-400 dark:bg-amber-900/30',
  'task.completed': 'text-green-600 bg-green-50 dark:text-green-400 dark:bg-green-900/30',
  'task.approved': 'text-green-700 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
  'task.returned': 'text-orange-600 bg-orange-50 dark:text-orange-400 dark:bg-orange-900/30',
}

const ACTION_OPTIONS: { value: AuditActionType | ''; label: string }[] = [
  { value: '', label: 'All actions' },
  { value: 'user.invited', label: 'User Invited' },
  { value: 'user.registered', label: 'User Registered' },
  { value: 'user.deactivated', label: 'User Deactivated' },
  { value: 'user.reactivated', label: 'User Reactivated' },
  { value: 'user.updated', label: 'User Updated' },
  { value: 'plan.created', label: 'Plan Created' },
  { value: 'plan.task_cancelled', label: 'Task Cancelled' },
  { value: 'task.started', label: 'Task Started' },
  { value: 'task.completed', label: 'Task Completed' },
  { value: 'task.approved', label: 'Task Approved' },
  { value: 'task.returned', label: 'Task Returned' },
]

const ENTITY_OPTIONS: { value: AuditEntityType | ''; label: string }[] = [
  { value: '', label: 'All entities' },
  { value: 'user', label: 'User' },
  { value: 'invitation', label: 'Invitation' },
  { value: 'plan', label: 'Plan' },
  { value: 'task', label: 'Task' },
]

export default function AuditLogPage() {
  const t = useTranslation()
  const [selectedAction, setSelectedAction] = useState<AuditActionType | ''>('')
  const [selectedEntityType, setSelectedEntityType] = useState<AuditEntityType | ''>('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')

  const { logs, total, loading } = useAuditLog({
    action: selectedAction || undefined,
    entity_type: selectedEntityType || undefined,
    date_from: dateFrom ? `${dateFrom}T00:00:00` : undefined,
    date_to: dateTo ? `${dateTo}T23:59:59` : undefined,
  })

  function handleClearFilters() {
    setSelectedAction('')
    setSelectedEntityType('')
    setDateFrom('')
    setDateTo('')
  }

  const hasActiveFilters = selectedAction || selectedEntityType || dateFrom || dateTo

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">{t.audit.title}</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{t.audit.subtitle}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-5 py-4 mb-4">
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500 dark:text-gray-400">{t.audit.filters.action}</label>
            <select
              value={selectedAction}
              onChange={(e) => setSelectedAction(e.target.value as AuditActionType | '')}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {ACTION_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500 dark:text-gray-400">{t.audit.filters.entity}</label>
            <select
              value={selectedEntityType}
              onChange={(e) => setSelectedEntityType(e.target.value as AuditEntityType | '')}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {ENTITY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500 dark:text-gray-400">{t.audit.filters.from}</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500 dark:text-gray-400">{t.audit.filters.to}</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {hasActiveFilters && (
            <button
              onClick={handleClearFilters}
              className="px-3 py-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
            >
              {t.audit.filters.clearFilters}
            </button>
          )}
        </div>

        {!loading && (
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-3">
            {t.audit.entries(total)}
          </p>
        )}
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        {loading ? (
          <p className="text-sm text-gray-400 dark:text-gray-500 px-5 py-4">{t.audit.loading}</p>
        ) : logs.length === 0 ? (
          <p className="text-sm text-gray-400 dark:text-gray-500 px-5 py-4">{t.audit.noLogs}</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
                <th className="text-left text-xs font-medium text-gray-600 dark:text-gray-400 px-5 py-3.5 rounded-tl-xl">{t.audit.columns.date}</th>
                <th className="text-left text-xs font-medium text-gray-600 dark:text-gray-400 px-5 py-3.5">{t.audit.columns.actor}</th>
                <th className="text-left text-xs font-medium text-gray-600 dark:text-gray-400 px-5 py-3.5">{t.audit.columns.action}</th>
                <th className="text-left text-xs font-medium text-gray-600 dark:text-gray-400 px-5 py-3.5">{t.audit.columns.entity}</th>
                <th className="text-left text-xs font-medium text-gray-600 dark:text-gray-400 px-5 py-3.5 rounded-tr-xl">{t.audit.columns.detail}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-gray-700/50 transition-colors">
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap">
                    {format(new Date(log.created_at), 'dd MMM yyyy HH:mm')}
                  </td>
                  <td className="px-5 py-3 text-gray-700 dark:text-gray-300 text-xs font-medium whitespace-nowrap">
                    {log.actor_name}
                  </td>
                  <td className="px-5 py-3">
                    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${ACTION_COLORS[log.action]}`}>
                      {ACTION_LABELS[log.action]}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400 font-mono text-xs">
                    {log.entity_type} · {log.entity_id.slice(0, 8)}…
                  </td>
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400 truncate max-w-[200px]">
                    {log.detail ?? '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
