import { Link } from 'react-router-dom'
import { useTemplateDetailPage } from '@/features/template/hooks/useTemplateDetailPage'
import { ROUTES } from '@/constants/routes'

const inputCls = 'w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500'

export default function TemplateDetailPage() {
  const {
    template, tasks,
    showAddForm, setShowAddForm,
    newTitle, setNewTitle,
    newDescription, setNewDescription,
    newDeadlineDays, setNewDeadlineDays,
    newIsRequired, setNewIsRequired,
    editingTaskId,
    editTitle, setEditTitle,
    editDescription, setEditDescription,
    editDeadlineDays, setEditDeadlineDays,
    editIsRequired, setEditIsRequired,
    startEdit, cancelEdit,
    handleAddTask, handleUpdateTask, handleDeleteTask,
    handleReorder, handleActivate, handleDeactivate,
  } = useTemplateDetailPage()

  if (!template) return null

  return (
    <div className="max-w-3xl mx-auto">
      <div className="flex items-center gap-3 mb-6 flex-wrap">
        <Link to={ROUTES.HR_TEMPLATES} className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors">
          ← Templates
        </Link>
        <span className="text-gray-300 dark:text-gray-600">/</span>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">{template.name}</h2>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${
          template.is_active
            ? 'bg-green-50 text-green-700 border-green-100 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800'
            : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600'
        }`}>
          {template.is_active ? 'Active' : 'Inactive'}
        </span>
        <div className="ml-auto">
          {template.is_active ? (
            <button onClick={handleDeactivate} className="text-xs text-red-600 dark:text-red-400 hover:text-red-800 border border-red-200 dark:border-red-700 hover:border-red-300 px-3 py-1.5 rounded-lg transition-colors">
              Deactivate
            </button>
          ) : (
            <button onClick={handleActivate} className="text-xs text-green-600 dark:text-green-400 hover:text-green-800 border border-green-200 dark:border-green-700 hover:border-green-300 px-3 py-1.5 rounded-lg transition-colors">
              Activate
            </button>
          )}
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden mb-4">
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Tasks</span>
          <button
            onClick={() => setShowAddForm((v) => !v)}
            className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-3 py-1.5 rounded-lg transition-colors"
          >
            {showAddForm ? 'Cancel' : '+ Add Task'}
          </button>
        </div>

        {tasks.length === 0 && !showAddForm && (
          <p className="px-5 py-8 text-center text-gray-400 dark:text-gray-500 text-sm">No tasks yet.</p>
        )}

        <ul className="divide-y divide-gray-100 dark:divide-gray-700">
          {tasks.map((task, index) => (
            <li key={task.id} className="px-5 py-4">
              <div className="flex items-center gap-3">
                <span className="text-xs text-gray-400 dark:text-gray-500 w-5 text-right">{task.order}</span>
                <div className="flex-1 min-w-0">
                  <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{task.title}</span>
                  <div className="flex gap-3 mt-0.5">
                    <span className="text-xs text-gray-500 dark:text-gray-400">{task.deadline_days} day{task.deadline_days !== 1 ? 's' : ''}</span>
                    <span className={`text-xs font-medium ${task.is_required ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`}>
                      {task.is_required ? 'Required' : 'Optional'}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  <button onClick={() => handleReorder(task.id, task.order - 1)} disabled={index === 0} className="text-xs text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 disabled:opacity-30 px-1.5 py-1 rounded">↑</button>
                  <button onClick={() => handleReorder(task.id, task.order + 1)} disabled={index === tasks.length - 1} className="text-xs text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 disabled:opacity-30 px-1.5 py-1 rounded">↓</button>
                  <button onClick={() => startEdit(task)} className="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 border border-gray-200 dark:border-gray-600 hover:border-gray-300 px-2.5 py-1 rounded-lg transition-colors ml-1">Edit</button>
                  <button onClick={() => handleDeleteTask(task.id)} className="text-xs text-red-600 dark:text-red-400 hover:text-red-800 border border-red-200 dark:border-red-700 hover:border-red-300 px-2.5 py-1 rounded-lg transition-colors">Delete</button>
                </div>
              </div>

              {editingTaskId === task.id && (
                <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 space-y-3">
                  <input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} placeholder="Title" className={inputCls} />
                  <input value={editDescription} onChange={(e) => setEditDescription(e.target.value)} placeholder="Description (optional)" className={inputCls} />
                  <div className="flex gap-3">
                    <input type="number" min={1} value={editDeadlineDays} onChange={(e) => setEditDeadlineDays(Number(e.target.value))} placeholder="Deadline (days)" className="w-36 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                    <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                      <input type="checkbox" checked={editIsRequired} onChange={(e) => setEditIsRequired(e.target.checked)} className="rounded" />
                      Required
                    </label>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={handleUpdateTask} className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition-colors">Save</button>
                    <button onClick={cancelEdit} className="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-800 border border-gray-200 dark:border-gray-600 px-4 py-2 rounded-lg transition-colors">Cancel</button>
                  </div>
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
            <div className="flex gap-3">
              <input type="number" min={1} value={newDeadlineDays} onChange={(e) => setNewDeadlineDays(Number(e.target.value))} placeholder="Deadline (days)" className="w-36 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
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
