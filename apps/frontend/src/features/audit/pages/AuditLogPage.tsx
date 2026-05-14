import { useState } from 'react'
import { format } from 'date-fns'
import { useAuditLog } from '@/features/audit/hooks/useAuditLog'

const ACTION_LABELS: Record<string, string> = {
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

const ACTION_COLORS: Record<string, string> = {
  'user.deactivated': 'text-red-600 bg-red-50',
  'user.reactivated': 'text-green-700 bg-green-50',
  'task.approved': 'text-green-700 bg-green-50',
  'task.returned': 'text-orange-600 bg-orange-50',
  'plan.task_cancelled': 'text-red-600 bg-red-50',
}

const ACTION_OPTIONS = [
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

export default function AuditLogPage() {
  const [selectedAction, setSelectedAction] = useState('')
  const { logs, loading } = useAuditLog(selectedAction || undefined)

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Audit Trail</h2>
          <p className="text-sm text-gray-500 mt-0.5">System activity log for all key actions.</p>
        </div>
        <select
          value={selectedAction}
          onChange={(e) => setSelectedAction(e.target.value)}
          className="border border-gray-300 rounded-lg px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {ACTION_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </div>

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
                    <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full ${ACTION_COLORS[log.action] ?? 'text-blue-700 bg-blue-50'}`}>
                      {ACTION_LABELS[log.action] ?? log.action}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-gray-500 font-mono text-xs truncate max-w-[180px]">
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
