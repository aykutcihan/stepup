import { useAuthStore } from '@/stores/authStore'
import DashboardLayout from '@/components/DashboardLayout'

export default function ManagerDashboard() {
  const user = useAuthStore((state) => state.user)

  return (
    <DashboardLayout>
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-8 py-10 text-center">
          <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-blue-700 text-xl font-bold">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </span>
          </div>
          <h2 className="text-xl font-semibold text-gray-900">
            Welcome, {user?.first_name}
          </h2>
          <p className="text-sm text-gray-500 mt-2">You're signed in as Manager.</p>
        </div>
      </div>
    </DashboardLayout>
  )
}
