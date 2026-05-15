import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { Loader, CheckCircle2, Calendar, ArrowRight, ClipboardList } from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { useEmployeeDashboard } from '@/features/dashboard/hooks/useEmployeeDashboard'

type Color = 'blue' | 'emerald' | 'amber'

const colorClasses: Record<Color, string> = {
  blue: 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
  emerald: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400',
  amber: 'bg-amber-50 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400',
}

function StatCard({
  label,
  value,
  icon,
  color,
}: {
  label: string
  value: number | string | undefined
  icon: ReactNode
  color: Color
}) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center mb-4 ${colorClasses[color]}`}>
        {icon}
      </div>
      <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{value ?? '—'}</p>
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{label}</p>
    </div>
  )
}

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

export default function EmployeeDashboard() {
  const user = useAuthStore((state) => state.user)
  const { stats } = useEmployeeDashboard()

  const progressPct =
    stats && stats.total_tasks > 0
      ? Math.round((stats.approved_tasks / stats.total_tasks) * 100)
      : null

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl px-8 py-8 text-white">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center shrink-0">
            <span className="text-white text-xl font-bold">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </span>
          </div>
          <div>
            <span className="inline-block text-xs font-semibold bg-white/20 px-3 py-1 rounded-full mb-2">
              Employee
            </span>
            <h2 className="text-2xl font-bold">{getGreeting()}, {user?.first_name}</h2>
            <p className="text-blue-100 text-sm mt-1">Track your onboarding progress here.</p>
          </div>
        </div>

        {progressPct !== null && (
          <div className="mt-6 pt-6 border-t border-white/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-100">Onboarding Progress</span>
              <span className="text-lg font-bold">{progressPct}%</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-2.5">
              <div
                className="bg-white h-2.5 rounded-full transition-all duration-500"
                style={{ width: `${progressPct}%` }}
              />
            </div>
            <p className="text-xs text-blue-100 mt-2">
              {stats?.approved_tasks} of {stats?.total_tasks} tasks approved
            </p>
          </div>
        )}
      </div>

      {stats && stats.total_tasks > 0 ? (
        <div className="grid grid-cols-3 gap-4">
          <StatCard
            label="In Progress"
            value={stats.in_progress_tasks}
            icon={<Loader size={20} />}
            color="blue"
          />
          <StatCard
            label="Completed"
            value={stats.completed_tasks}
            icon={<CheckCircle2 size={20} />}
            color="emerald"
          />
          <StatCard
            label="Next Deadline"
            value={stats.next_deadline ? format(new Date(stats.next_deadline), 'dd MMM yyyy') : 'None'}
            icon={<Calendar size={20} />}
            color="amber"
          />
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-10 text-center">
          <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-3">
            <ClipboardList size={20} className="text-gray-400" />
          </div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            No active onboarding plan assigned yet.
          </p>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-4">
          Quick Links
        </h3>
        <Link
          to={ROUTES.EMPLOYEE_PLAN}
          className="flex items-center justify-between group px-4 py-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-50 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <ClipboardList size={16} className="text-blue-600 dark:text-blue-400" />
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">My Onboarding Plan</span>
          </div>
          <ArrowRight size={16} className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors" />
        </Link>
      </div>
    </div>
  )
}
