import type { ReactNode } from 'react'
import { Users, ClipboardList, Building2, Clock } from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'
import { useHRDashboard } from '@/features/dashboard/hooks/useHRDashboard'


type Color = 'blue' | 'emerald' | 'violet' | 'amber'

const colorClasses: Record<Color, string> = {
  blue: 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
  emerald: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400',
  violet: 'bg-violet-50 text-violet-600 dark:bg-violet-900/30 dark:text-violet-400',
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

export default function HRDashboard() {
  const user = useAuthStore((state) => state.user)
  const { stats } = useHRDashboard()

  const avatarSrc = user?.avatar_url ?? null
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
              HR Admin
            </span>
            <h2 className="text-2xl font-bold">{getGreeting()}, {user?.first_name}</h2>
            <p className="text-blue-100 text-sm mt-1">Here's an overview of your platform today.</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <StatCard label="Active Users" value={stats?.active_users} icon={<Users size={20} />} color="blue" />
        <StatCard label="Active Plans" value={stats?.active_plans} icon={<ClipboardList size={20} />} color="emerald" />
        <StatCard label="Active Departments" value={stats?.active_departments} icon={<Building2 size={20} />} color="violet" />
        <StatCard label="Pending Approvals" value={stats?.pending_approvals} icon={<Clock size={20} />} color="amber" />
      </div>
    </div>
  )
}
