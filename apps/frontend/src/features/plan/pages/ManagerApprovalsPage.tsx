import { useManagerApprovalsPage } from '@/features/plan/hooks/useManagerApprovalsPage'

export default function ManagerApprovalsPage() {
  const { tasks, isLoading, handleApprove, handleReview } = useManagerApprovalsPage()

  if (isLoading) return null

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Pending Approvals</h2>

      {tasks.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-8 py-10 text-center">
          <p className="text-gray-500 text-sm">No tasks pending approval.</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm divide-y divide-gray-100">
          {tasks.map((task) => (
            <div key={task.id} className="px-5 py-4 flex items-center justify-between gap-4">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">{task.title}</p>
                <p className="text-xs text-gray-500 mt-0.5">
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
                  className="text-xs border border-gray-300 hover:border-gray-400 text-gray-700 font-medium px-3 py-1.5 rounded-lg transition-colors"
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
