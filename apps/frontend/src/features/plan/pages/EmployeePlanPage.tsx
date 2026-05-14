import { useEmployeePlanPage } from '@/features/plan/hooks/useEmployeePlanPage'
import type { components } from '@/types/api'

type OnboardingPlanTaskStatus = components['schemas']['OnboardingPlanTaskStatus']

const STATUS_LABELS: Record<OnboardingPlanTaskStatus, string> = {
  not_started: 'Not started',
  in_progress: 'In progress',
  completed: 'Completed',
  approved: 'Approved',
  returned: 'Returned',
  cancelled: 'Cancelled',
}

const STATUS_STYLES: Record<OnboardingPlanTaskStatus, string> = {
  not_started: 'bg-gray-100 text-gray-500 border-gray-200',
  in_progress: 'bg-amber-50 text-amber-700 border-amber-100',
  completed: 'bg-green-50 text-green-700 border-green-100',
  approved: 'bg-green-100 text-green-800 border-green-200',
  returned: 'bg-red-50 text-red-700 border-red-100',
  cancelled: 'bg-gray-100 text-gray-400 border-gray-200',
}

export default function EmployeePlanPage() {
  const { plan, notFound, completedCount, totalCount, handleStartTask, handleCompleteTask } =
    useEmployeePlanPage()

  if (notFound) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-8 py-10 text-center">
          <p className="text-gray-500 text-sm">No active onboarding plan assigned to you yet.</p>
        </div>
      </div>
    )
  }

  if (!plan) return null

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">My Onboarding Plan</h2>
        <span className="text-sm text-gray-500">
          {completedCount} / {totalCount} tasks done
        </span>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm divide-y divide-gray-100">
        {plan.tasks.map((task) => {
          const isOverdue = task.status === 'not_started' || task.status === 'in_progress'
            ? new Date(task.deadline) < new Date()
            : false

          return (
            <div key={task.id} className="px-5 py-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`text-sm font-medium ${task.status === 'cancelled' ? 'line-through text-gray-400' : 'text-gray-900'}`}>
                      {task.title}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${STATUS_STYLES[task.status]}`}>
                      {STATUS_LABELS[task.status]}
                    </span>
                    <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600' : 'text-gray-400'}`}>
                      {task.is_required ? 'Required' : 'Optional'}
                    </span>
                  </div>
                  <p className={`text-xs mt-0.5 ${isOverdue ? 'text-red-500 font-medium' : 'text-gray-500'}`}>
                    Due: {task.deadline}{isOverdue ? ' · Overdue' : ''}
                  </p>
                </div>

                <div className="shrink-0">
                  {task.status === 'not_started' && (
                    <button
                      onClick={() => handleStartTask(task.id)}
                      className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors"
                    >
                      Start
                    </button>
                  )}
                  {task.status === 'in_progress' && (
                    <button
                      onClick={() => handleCompleteTask(task.id)}
                      className="text-xs bg-green-700 hover:bg-green-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors"
                    >
                      Mark as Complete
                    </button>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
