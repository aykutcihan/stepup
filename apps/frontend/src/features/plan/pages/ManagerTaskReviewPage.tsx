import { Link } from 'react-router-dom'
import { useManagerTaskReviewPage } from '@/features/plan/hooks/useManagerTaskReviewPage'
import { ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type TaskAttachmentResponse = components['schemas']['TaskAttachmentResponse']

export default function ManagerTaskReviewPage() {
  const {
    task,
    showReturnModal,
    setShowReturnModal,
    returnComment,
    setReturnComment,
    handleApprove,
    handleReturn,
  } = useManagerTaskReviewPage()

  if (!task) return null

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Link
          to={ROUTES.MANAGER_APPROVALS}
          className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
        >
          ← Approvals
        </Link>
        <span className="text-gray-300">/</span>
        <h2 className="text-xl font-semibold text-gray-900">Task Review</h2>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5 space-y-3 mb-4">
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 w-28">Employee</span>
          <span className="text-gray-900 font-medium">{task.employee_name}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 w-28">Task</span>
          <span className="text-gray-900 font-medium">{task.title}</span>
        </div>
        {task.description && (
          <div className="flex gap-2 text-sm">
            <span className="text-gray-500 w-28 shrink-0">Description</span>
            <span className="text-gray-700">{task.description}</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 w-28">Deadline</span>
          <span className="text-gray-900">{task.deadline}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 w-28">Required</span>
          <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600' : 'text-gray-400'}`}>
            {task.is_required ? 'Yes' : 'No'}
          </span>
        </div>
      </div>

      {task.attachments.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5 mb-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Attachments</p>
          <ul className="space-y-1">
            {task.attachments.map((att: TaskAttachmentResponse) => (
              <li key={att.id} className="flex items-center gap-2 text-xs text-gray-600">
                <a href={att.download_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline truncate max-w-xs">
                  {att.file_name}
                </a>
                <span className="text-gray-400">({(att.file_size / 1024).toFixed(0)} KB)</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={handleApprove}
          className="bg-green-700 hover:bg-green-800 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          Approve
        </button>
        <button
          onClick={() => setShowReturnModal(true)}
          className="border border-red-300 hover:border-red-400 text-red-700 text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          Return
        </button>
      </div>

      {showReturnModal && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-base font-semibold text-gray-900 mb-3">Return Task</h3>
            <p className="text-sm text-gray-500 mb-3">
              Provide feedback so the employee knows what to fix.
            </p>
            <textarea
              value={returnComment}
              onChange={(e) => setReturnComment(e.target.value)}
              placeholder="Feedback comment (required)"
              rows={4}
              className="w-full border border-gray-300 rounded-lg px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <div className="flex gap-2 mt-4 justify-end">
              <button
                onClick={() => { setShowReturnModal(false); setReturnComment('') }}
                className="text-sm border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:border-gray-400 transition-colors"
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
