import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { ClipboardList, Clock, Users, ArrowRight } from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { useManagerDashboard } from '@/features/dashboard/hooks/useManagerDashboard'

const API_URL = import.meta.env.VITE_API_URL ?? ''

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

export default function ManagerDashboard() {
  const user = useAuthStore((state) => state.user)
  const { stats } = useManagerDashboard()

  const avatarSrc = user?.avatar_url ? `${API_URL}${user.avatar_url}` : null
  const initials = `${user?.first_name?.[0] ?? ''}${user?.last_name?.[0] ?? ''}`

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl px-8 py-8 text-white">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-full overflow-hidden bg-white/20 flex items-center justify-center shrink-0">
            {avatarSrc ? (
              <img src={avatarSrc} alt="Avatar" className="w-full h-full object-cover" />
            ) : (
              <span className="text-white text-xl font-bold">{initials}</span>
            )}
          </div>
          <div>
            <span className="inline-block text-xs font-semibold bg-white/20 px-3 py-1 rounded-full mb-2">
              Manager
            </span>
            <h2 className="text-2xl font-bold">{getGreeting()}, {user?.first_name}</h2>
            <p className="text-blue-100 text-sm mt-1">Here's your team overview for today.</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <StatCard label="Active Plans" value={stats?.active_plans} icon={<ClipboardList size={20} />} color="emerald" />
        <StatCard label="Pending Approvals" value={stats?.pending_approvals} icon={<Clock size={20} />} color="amber" />
        <StatCard label="Employees" value={stats?.total_employees} icon={<Users size={20} />} color="blue" />
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-4">
          Quick Links
        </h3>
        <Link
          to={ROUTES.MANAGER_APPROVALS}
          className="flex items-center justify-between group px-4 py-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-amber-50 dark:bg-amber-900/30 rounded-lg flex items-center justify-center">
              <Clock size={16} className="text-amber-600 dark:text-amber-400" />
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Pending Approvals</span>
          </div>
          <ArrowRight size={16} className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors" />
        </Link>
      </div>
    </div>
  )
}
