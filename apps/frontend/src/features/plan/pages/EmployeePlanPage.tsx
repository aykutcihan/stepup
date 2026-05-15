import { useRef, useState } from 'react'
import { useEmployeePlanPage } from '@/features/plan/hooks/useEmployeePlanPage'
import type { components } from '@/types/api'

type OnboardingPlanTaskStatus = components['schemas']['OnboardingPlanTaskStatus']
type TaskAttachmentResponse = components['schemas']['TaskAttachmentResponse']
type TaskCommentResponse = components['schemas']['TaskCommentResponse']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']

const STATUS_LABELS: Record<OnboardingPlanTaskStatus, string> = {
  not_started: 'Not started',
  in_progress: 'In progress',
  completed: 'Completed',
  approved: 'Approved',
  returned: 'Returned',
  overdue: 'Overdue',
  cancelled: 'Cancelled',
}

const STATUS_STYLES: Record<OnboardingPlanTaskStatus, string> = {
  not_started: 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600',
  in_progress: 'bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-900/30 dark:text-amber-400 dark:border-amber-800',
  completed: 'bg-green-50 text-green-700 border-green-100 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800',
  approved: 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/40 dark:text-green-300 dark:border-green-700',
  returned: 'bg-red-50 text-red-700 border-red-100 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800',
  overdue: 'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/40 dark:text-red-300 dark:border-red-700',
  cancelled: 'bg-gray-100 text-gray-400 border-gray-200 dark:bg-gray-700 dark:text-gray-500 dark:border-gray-600',
}

function AttachmentList({ attachments, taskId, canDelete, onDelete }: {
  attachments: TaskAttachmentResponse[]
  taskId: string
  canDelete: boolean
  onDelete: (taskId: string, attId: string) => void
}) {
  if (attachments.length === 0) return null
  return (
    <ul className="mt-2 space-y-1">
      {attachments.map((att) => (
        <li key={att.id} className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400">
          <a href={att.download_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 hover:underline truncate max-w-[200px]">
            {att.file_name}
          </a>
          <span className="text-gray-400 dark:text-gray-500">({(att.file_size / 1024).toFixed(0)} KB)</span>
          {canDelete && (
            <button onClick={() => onDelete(taskId, att.id)} className="text-red-400 hover:text-red-600 text-xs">✕</button>
          )}
        </li>
      ))}
    </ul>
  )
}

function CommentList({ comments }: { comments: TaskCommentResponse[] }) {
  if (comments.length === 0) return null
  return (
    <ul className="mt-2 space-y-1">
      {comments.map((c) => (
        <li key={c.id} className="text-xs text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700 rounded px-2 py-1">
          {c.content}
        </li>
      ))}
    </ul>
  )
}

export default function EmployeePlanPage() {
  const {
    plan, notFound, completedCount, totalCount,
    handleStartTask, handleCompleteTask,
    handleUpload, handleDeleteAttachment, handleAddComment,
  } = useEmployeePlanPage()

  const [expandedTask, setExpandedTask] = useState<string | null>(null)
  const [commentText, setCommentText] = useState<Record<string, string>>({})
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [uploadingFor, setUploadingFor] = useState<string | null>(null)

  if (notFound) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-8 py-10 text-center">
          <p className="text-gray-500 dark:text-gray-400 text-sm">No active onboarding plan assigned to you yet.</p>
        </div>
      </div>
    )
  }

  if (!plan) return null

  function toggleExpand(taskId: string) {
    setExpandedTask((prev) => (prev === taskId ? null : taskId))
  }

  async function onFileChange(e: React.ChangeEvent<HTMLInputElement>, taskId: string) {
    const file = e.target.files?.[0]
    if (!file) return
    await handleUpload(taskId, file)
    e.target.value = ''
  }

  async function onAddComment(taskId: string) {
    const text = commentText[taskId]?.trim()
    if (!text) return
    await handleAddComment(taskId, text)
    setCommentText((prev) => ({ ...prev, [taskId]: '' }))
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">My Onboarding Plan</h2>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {completedCount} / {totalCount} tasks done
        </span>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm divide-y divide-gray-100 dark:divide-gray-700">
        {plan.tasks.map((task: OnboardingPlanTaskResponse) => {
          const isExpanded = expandedTask === task.id
          const attachments: TaskAttachmentResponse[] = task.attachments ?? []
          const comments: TaskCommentResponse[] = task.comments ?? []
          const canDelete = task.status !== 'approved' && task.status !== 'cancelled'

          return (
            <div key={task.id} className="px-5 py-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <button
                      onClick={() => toggleExpand(task.id)}
                      className={`text-sm font-medium text-left ${task.status === 'cancelled' ? 'line-through text-gray-400 dark:text-gray-500' : 'text-gray-900 dark:text-gray-100'}`}
                    >
                      {task.title}
                    </button>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${STATUS_STYLES[task.status]}`}>
                      {STATUS_LABELS[task.status]}
                    </span>
                    <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {task.is_required ? 'Required' : 'Optional'}
                    </span>
                  </div>
                  <p className="text-xs mt-0.5 text-gray-500 dark:text-gray-400">Due: {task.deadline}</p>
                </div>

                <div className="shrink-0 flex gap-2">
                  {(task.status === 'not_started' || task.status === 'overdue') && (
                    <button onClick={() => handleStartTask(task.id)} className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors">
                      Start
                    </button>
                  )}
                  {(task.status === 'in_progress' || task.status === 'overdue') && (
                    <button onClick={() => handleCompleteTask(task.id)} className="text-xs bg-green-700 hover:bg-green-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors">
                      Mark as Complete
                    </button>
                  )}
                </div>
              </div>

              {isExpanded && task.status !== 'cancelled' && (
                <div className="mt-3 space-y-3 border-t border-gray-100 dark:border-gray-700 pt-3">
                  {task.description && (
                    <p className="text-xs text-gray-600 dark:text-gray-400">{task.description}</p>
                  )}
                  {task.return_comment && (
                    <div className="bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                      <p className="text-xs font-medium text-red-700 mb-0.5">Manager feedback</p>
                      <p className="text-xs text-red-600">{task.return_comment}</p>
                    </div>
                  )}

                  <div>
                    <p className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Attachments</p>
                    <AttachmentList attachments={attachments} taskId={task.id} canDelete={canDelete} onDelete={handleDeleteAttachment} />
                    {canDelete && (
                      <>
                        <input
                          ref={uploadingFor === task.id ? fileInputRef : undefined}
                          type="file"
                          accept=".pdf,.docx,.png,.jpg,.jpeg"
                          className="hidden"
                          onChange={(e) => onFileChange(e, task.id)}
                          id={`file-${task.id}`}
                        />
                        <label
                          htmlFor={`file-${task.id}`}
                          onClick={() => setUploadingFor(task.id)}
                          className="mt-1 inline-block text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 cursor-pointer"
                        >
                          + Upload file
                        </label>
                        <p className="text-xs text-gray-400 dark:text-gray-500">PDF, DOCX, PNG or JPEG · max 10 MB</p>
                      </>
                    )}
                  </div>

                  <div>
                    <p className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">Comments</p>
                    <CommentList comments={comments} />
                    <div className="flex gap-2 mt-1">
                      <input
                        type="text"
                        placeholder="Add a comment…"
                        value={commentText[task.id] ?? ''}
                        onChange={(e) => setCommentText((prev) => ({ ...prev, [task.id]: e.target.value }))}
                        onKeyDown={(e) => e.key === 'Enter' && onAddComment(task.id)}
                        className="flex-1 text-xs border border-gray-300 dark:border-gray-600 rounded-lg px-2 py-1.5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <button
                        onClick={() => onAddComment(task.id)}
                        className="text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium px-2 py-1.5 rounded-lg transition-colors"
                      >
                        Send
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
