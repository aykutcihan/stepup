import { useManagerApprovalsPage } from '@/features/plan/hooks/useManagerApprovalsPage'

export default function ManagerApprovalsPage() {
  const { tasks, isLoading, handleApprove, handleReview } = useManagerApprovalsPage()

  if (isLoading) return null

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Pending Approvals</h2>

      {tasks.length === 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-8 py-10 text-center">
          <p className="text-gray-500 dark:text-gray-400 text-sm">No tasks pending approval.</p>
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm divide-y divide-gray-100 dark:divide-gray-700">
          {tasks.map((task) => (
            <div key={task.id} className="px-5 py-4 flex items-center justify-between gap-4">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{task.title}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                  {task.employee_name} · Due: {task.deadline}
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleApprove(task.id)}
                  className="text-xs bg-green-700 hover:bg-green-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors"
                >
                  Approve
                </button>
                <button
                  onClick={() => handleReview(task.id)}
                  className="text-xs border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 text-gray-700 dark:text-gray-300 font-medium px-3 py-1.5 rounded-lg transition-colors"
                >
                  Review
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
