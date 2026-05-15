import { Link } from 'react-router-dom'
import { usePlanDetailPage } from '@/features/plan/hooks/usePlanDetailPage'
import { ROUTES } from '@/constants/routes'

const inputCls = 'w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500'
const btnSm = 'text-xs border border-gray-200 dark:border-gray-600 px-2.5 py-1 rounded-lg transition-colors'

export default function PlanDetailPage() {
  const {
    plan, managers,
    editingManagerId, setEditingManagerId,
    editingTaskId, setEditingTaskId,
    editingDeadline, setEditingDeadline,
    cancelConfirmTaskId, setCancelConfirmTaskId,
    showAddForm, setShowAddForm,
    newTitle, setNewTitle,
    newDescription, setNewDescription,
    newDeadline, setNewDeadline,
    newIsRequired, setNewIsRequired,
    handleChangeManager,
    startEditDeadline,
    handleUpdateDeadline,
    handleAddTask,
    handleCancelTask,
    getManagerName,
  } = usePlanDetailPage()

  if (!plan) return null

  return (
    <div className="max-w-3xl mx-auto">
      <div className="flex items-center gap-3 mb-6 flex-wrap">
        <Link to={ROUTES.HR_PLAN_NEW} className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors">
          ← Plans
        </Link>
        <span className="text-gray-300 dark:text-gray-600">/</span>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Onboarding Plan</h2>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${
          plan.is_active
            ? 'bg-green-50 text-green-700 border-green-100 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800'
            : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600'
        }`}>
          {plan.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-5 mb-4 space-y-3">
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-24">Start date</span>
          <span className="text-gray-900 dark:text-gray-100 font-medium">{plan.start_date}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500 dark:text-gray-400 w-24">Manager</span>
          {editingManagerId !== null ? (
            <div className="flex items-center gap-2">
              <select
                value={editingManagerId}
                onChange={(e) => setEditingManagerId(e.target.value)}
                className="border border-gray-300 dark:border-gray-600 rounded px-2 py-1 text-xs bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {managers.map((m) => (
                  <option key={m.id} value={m.id}>{m.first_name} {m.last_name}</option>
                ))}
              </select>
              <button onClick={() => handleChangeManager(editingManagerId)} className={`${btnSm} text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-700`}>Save</button>
              <button onClick={() => setEditingManagerId(null)} className={`${btnSm} text-gray-500 dark:text-gray-400`}>Cancel</button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <span className="text-gray-900 dark:text-gray-100 font-medium">{getManagerName(plan.manager_id)}</span>
              <button onClick={() => setEditingManagerId(plan.manager_id)} className={`${btnSm} text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200`}>Edit</button>
            </div>
          )}
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50 rounded-tl-xl rounded-tr-xl">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Tasks</span>
          <button
            onClick={() => setShowAddForm((v) => !v)}
            className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors"
          >
            {showAddForm ? 'Cancel' : '+ Add Task'}
          </button>
        </div>

        <ul className="divide-y divide-gray-100 dark:divide-gray-700">
          {plan.tasks.map((task) => (
            <li key={task.id} className="px-5 py-4">
              <div className="flex items-start gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`text-sm font-medium ${task.status === 'cancelled' ? 'line-through text-gray-400 dark:text-gray-500' : 'text-gray-900 dark:text-gray-100'}`}>
                      {task.title}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${
                      task.status === 'cancelled'
                        ? 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600'
                        : 'bg-blue-50 text-blue-700 border-blue-100 dark:bg-blue-900/30 dark:text-blue-400 dark:border-blue-800'
                    }`}>
                      {task.status === 'not_started' ? 'Not started' : 'Cancelled'}
                    </span>
                    <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {task.is_required ? 'Required' : 'Optional'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Due: {task.deadline}</p>
                </div>

                {task.status !== 'cancelled' && (
                  <div className="flex items-center gap-2 shrink-0">
                    <button onClick={() => startEditDeadline(task)} className={`${btnSm} text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200`}>Edit deadline</button>
                    {cancelConfirmTaskId === task.id ? (
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-gray-600 dark:text-gray-400">Cancel task?</span>
                        <button onClick={() => handleCancelTask(task.id)} className={`${btnSm} text-red-600 dark:text-red-400 border-red-200 dark:border-red-700`}>Yes</button>
                        <button onClick={() => setCancelConfirmTaskId(null)} className={`${btnSm} text-gray-500 dark:text-gray-400`}>No</button>
                      </div>
                    ) : (
                      <button onClick={() => setCancelConfirmTaskId(task.id)} className={`${btnSm} text-red-600 dark:text-red-400 border-red-200 dark:border-red-700`}>Cancel</button>
                    )}
                  </div>
                )}
              </div>

              {editingTaskId === task.id && (
                <div className="mt-3 flex items-center gap-2">
                  <input
                    type="date"
                    value={editingDeadline}
                    onChange={(e) => setEditingDeadline(e.target.value)}
                    className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button onClick={handleUpdateDeadline} className={`${btnSm} text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-700`}>Save</button>
                  <button onClick={() => setEditingTaskId(null)} className={`${btnSm} text-gray-500 dark:text-gray-400`}>Cancel</button>
                </div>
              )}
            </li>
          ))}
        </ul>

        {showAddForm && (
          <div className="px-5 py-5 border-t border-gray-100 dark:border-gray-700 space-y-3">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">New Task</p>
            <input value={newTitle} onChange={(e) => setNewTitle(e.target.value)} placeholder="Title" className={inputCls} />
            <input value={newDescription} onChange={(e) => setNewDescription(e.target.value)} placeholder="Description (optional)" className={inputCls} />
            <div className="flex gap-3 items-center">
              <input
                type="date"
                value={newDeadline}
                onChange={(e) => setNewDeadline(e.target.value)}
                className="border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                <input type="checkbox" checked={newIsRequired} onChange={(e) => setNewIsRequired(e.target.checked)} className="rounded" />
                Required
              </label>
            </div>
            <button onClick={handleAddTask} className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition-colors">Add Task</button>
          </div>
        )}
      </div>
    </div>
  )
}
