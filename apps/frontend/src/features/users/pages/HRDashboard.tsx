import { useAuthStore } from '@/stores/authStore'
import { useHRDashboard } from '@/features/dashboard/hooks/useHRDashboard'

function StatCard({ label, value }: { label: string; value: number | undefined }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5">
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mt-1">{value ?? '—'}</p>
    </div>
  )
}

export default function HRDashboard() {
  const user = useAuthStore((state) => state.user)
  const { stats } = useHRDashboard()

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-8 py-8">
        <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/40 rounded-full flex items-center justify-center mb-4">
          <span className="text-blue-700 dark:text-blue-400 text-xl font-bold">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </span>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Welcome, {user?.first_name}</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">You're signed in as HR Admin.</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <StatCard label="Active Users" value={stats?.active_users} />
        <StatCard label="Active Plans" value={stats?.active_plans} />
        <StatCard label="Active Departments" value={stats?.active_departments} />
        <StatCard label="Pending Approvals" value={stats?.pending_approvals} />
      </div>
    </div>
  )
}
