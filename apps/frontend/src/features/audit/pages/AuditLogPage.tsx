import { useState } from 'react'
import { format } from 'date-fns'
import { useAuditLog } from '@/features/audit/hooks/useAuditLog'
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
  'user.invited': 'text-blue-700 bg-blue-50',
  'user.registered': 'text-blue-700 bg-blue-50',
  'user.deactivated': 'text-red-600 bg-red-50',
  'user.reactivated': 'text-green-700 bg-green-50',
  'user.updated': 'text-gray-600 bg-gray-100',
  'plan.created': 'text-purple-700 bg-purple-50',
  'plan.task_cancelled': 'text-red-600 bg-red-50',
  'task.started': 'text-amber-700 bg-amber-50',
  'task.completed': 'text-green-600 bg-green-50',
  'task.approved': 'text-green-700 bg-green-100',
  'task.returned': 'text-orange-600 bg-orange-50',
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
          <h2 className="text-xl font-semibold text-gray-900">Audit Trail</h2>
          <p className="text-sm text-gray-500 mt-0.5">System activity log for all key actions.</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-5 py-4 mb-4">
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500">Action</label>
            <select
              value={selectedAction}
              onChange={(e) => setSelectedAction(e.target.value as AuditActionType | '')}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {ACTION_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500">Entity</label>
            <select
              value={selectedEntityType}
              onChange={(e) => setSelectedEntityType(e.target.value as AuditEntityType | '')}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {ENTITY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500">From</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-500">To</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {hasActiveFilters && (
            <button
              onClick={handleClearFilters}
              className="px-3 py-1.5 text-sm text-gray-500 hover:text-gray-700 border border-gray-300 rounded-lg hover:border-gray-400 transition-colors"
            >
              Clear filters
            </button>
          )}
        </div>

        {!loading && (
          <p className="text-xs text-gray-400 mt-3">
            {total} {total === 1 ? 'entry' : 'entries'} found
          </p>
        )}
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        {loading ? (
          <p className="text-sm text-gray-400 px-5 py-4">Loading...</p>
        ) : logs.length === 0 ? (
          <p className="text-sm text-gray-400 px-5 py-4">No audit logs found.</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left text-xs font-medium text-gray-500 px-5 py-3">Date</th>
                <th className="text-left text-xs font-medium text-gray-500 px-5 py-3">Action</th>
                <th className="text-left text-xs font-medium text-gray-500 px-5 py-3">Entity</th>
                <th className="text-left text-xs font-medium text-gray-500 px-5 py-3">Detail</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50">
                  <td className="px-5 py-3 text-gray-500 whitespace-nowrap">
                    {format(new Date(log.created_at), 'dd MMM yyyy HH:mm')}
                  </td>
                  <td className="px-5 py-3">
                    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${ACTION_COLORS[log.action]}`}>
                      {ACTION_LABELS[log.action]}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-gray-500 font-mono text-xs">
                    {log.entity_type} · {log.entity_id.slice(0, 8)}…
                  </td>
                  <td className="px-5 py-3 text-gray-500 truncate max-w-[200px]">
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
