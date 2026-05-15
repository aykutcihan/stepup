import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { useEmployeeDashboard } from '@/features/dashboard/hooks/useEmployeeDashboard'

function StatCard({ label, value }: { label: string; value: string | number | undefined }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-semibold text-gray-900 mt-1">{value ?? '—'}</p>
    </div>
  )
}

export default function EmployeeDashboard() {
  const user = useAuthStore((state) => state.user)
  const { stats } = useEmployeeDashboard()

  const progressPct = stats && stats.total_tasks > 0
    ? Math.round(((stats.approved_tasks) / stats.total_tasks) * 100)
    : null

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-8 py-8">
        <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mb-4">
          <span className="text-blue-700 text-xl font-bold">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </span>
        </div>
        <h2 className="text-xl font-semibold text-gray-900">Welcome, {user?.first_name}</h2>
        <p className="text-sm text-gray-500 mt-1">You're signed in as Employee.</p>
      </div>

      {stats && stats.total_tasks > 0 ? (
        <>
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium text-gray-700">Plan Progress</p>
              <p className="text-sm font-semibold text-gray-900">{progressPct}%</p>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${progressPct}%` }}
              />
            </div>
            <p className="text-xs text-gray-500 mt-2">
              {stats.approved_tasks} of {stats.total_tasks} tasks approved
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <StatCard label="In Progress" value={stats.in_progress_tasks} />
            <StatCard label="Completed" value={stats.completed_tasks} />
            <StatCard
              label="Next Deadline"
              value={stats.next_deadline ? format(new Date(stats.next_deadline), 'dd MMM yyyy') : 'None'}
            />
          </div>
        </>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5">
          <p className="text-sm text-gray-400">No active onboarding plan assigned.</p>
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Quick links</h3>
        <Link
          to={ROUTES.EMPLOYEE_PLAN}
          className="inline-flex items-center gap-2 text-sm text-blue-700 hover:text-blue-900 font-medium transition-colors"
        >
          My Onboarding Plan →
        </Link>
      </div>
    </div>
  )
}
