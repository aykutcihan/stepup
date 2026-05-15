import { Link } from 'react-router-dom'
import { useManagerTaskReviewPage } from '@/features/plan/hooks/useManagerTaskReviewPage'
import { ROUTES } from '@/constants/routes'

export default function ManagerTaskReviewPage() {
  const {
    task,
    showReturnModal, setShowReturnModal,
    returnComment, setReturnComment,
    handleApprove, handleReturn,
  } = useManagerTaskReviewPage()

  if (!task) return null

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Link to={ROUTES.MANAGER_APPROVALS} className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors">
          ← Approvals
        </Link>
        <span className="text-gray-300 dark:text-gray-600">/</span>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Task Review</h2>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5 space-y-3 mb-4">
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-28">Employee</span>
          <span className="text-gray-900 dark:text-gray-100 font-medium">{task.employee_name}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-28">Task</span>
          <span className="text-gray-900 dark:text-gray-100 font-medium">{task.title}</span>
        </div>
        {task.description && (
          <div className="flex gap-2 text-sm">
            <span className="text-gray-500 dark:text-gray-400 w-28 shrink-0">Description</span>
            <span className="text-gray-700 dark:text-gray-300">{task.description}</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-28">Deadline</span>
          <span className="text-gray-900 dark:text-gray-100">{task.deadline}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-28">Required</span>
          <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`}>
            {task.is_required ? 'Yes' : 'No'}
          </span>
        </div>
        {(task as any).attachments?.length > 0 && (
          <div className="flex gap-2 text-sm">
            <span className="text-gray-500 dark:text-gray-400 w-28 shrink-0">Attachments</span>
            <ul className="space-y-1">
              {(task as any).attachments.map((att: any) => (
                <li key={att.id}>
                  <a href={att.download_url} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-600 dark:text-blue-400 hover:underline">
                    {att.file_name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
        {(task as any).return_comment && (
          <div className="flex gap-2 text-sm">
            <span className="text-gray-500 dark:text-gray-400 w-28 shrink-0">Last feedback</span>
            <span className="text-gray-700 dark:text-gray-300 italic">{(task as any).return_comment}</span>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <button onClick={handleApprove} className="bg-green-700 hover:bg-green-800 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
          Approve
        </button>
        <button onClick={() => setShowReturnModal(true)} className="border border-red-300 dark:border-red-700 hover:border-red-400 text-red-700 dark:text-red-400 text-sm font-medium px-4 py-2 rounded-lg transition-colors">
          Return
        </button>
      </div>

      {showReturnModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 w-full max-w-md mx-4 border border-gray-200 dark:border-gray-700">
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100 mb-3">Return Task</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">Provide feedback so the employee knows what to fix.</p>
            <textarea
              value={returnComment}
              onChange={(e) => setReturnComment(e.target.value)}
              placeholder="Feedback comment (required)"
              rows={4}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <div className="flex gap-2 mt-4 justify-end">
              <button
                onClick={() => { setShowReturnModal(false); setReturnComment('') }}
                className="text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleReturn}
                disabled={!returnComment.trim()}
                className="text-sm bg-red-700 hover:bg-red-800 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium px-4 py-2 rounded-lg transition-colors"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
