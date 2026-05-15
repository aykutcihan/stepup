import { useDepartmentsPage } from '@/features/department/hooks/useDepartmentsPage'
import KebabMenu from '@/components/KebabMenu'

export default function DepartmentsPage() {
  const {
    departments,
    showAddForm,
    setShowAddForm,
    newName,
    setNewName,
    editingId,
    editingName,
    setEditingName,
    pageError,
    handleCreate,
    startEdit,
    cancelEdit,
    handleUpdate,
    handleDeactivate,
    handleReactivate,
  } = useDepartmentsPage()

  return (
    <div className="max-w-3xl mx-auto">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Departments</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Manage your organisation's departments.</p>
        </div>
        <button
          onClick={() => setShowAddForm((v) => !v)}
          className="text-sm bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {showAddForm ? 'Cancel' : '+ Add Department'}
        </button>
      </div>

      {pageError && (
        <div className="mb-4 text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-3">
          {pageError}
        </div>
      )}

      {showAddForm && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-5 py-4 mb-4 flex gap-2">
          <input
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Department name"
            className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleCreate}
            className="bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            Add
          </button>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50 text-left">
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400 rounded-tl-xl">Name</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400">Status</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 dark:text-gray-400 text-right rounded-tr-xl">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {departments.map((d) => (
              <tr key={d.id} className="hover:bg-slate-50 dark:hover:bg-gray-700/50 transition-colors">
                <td className="px-5 py-3.5">
                  {editingId === d.id ? (
                    <input
                      value={editingName}
                      onChange={(e) => setEditingName(e.target.value)}
                      className="border border-gray-300 dark:border-gray-600 rounded px-2 py-1 text-sm w-full bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <span className="font-medium text-gray-900 dark:text-gray-100">{d.name}</span>
                  )}
                </td>
                <td className="px-5 py-3.5">
                  <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium border ${
                    d.is_active
                      ? 'bg-green-50 text-green-700 border-green-100 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800'
                      : 'bg-gray-100 text-gray-500 border-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600'
                  }`}>
                    {d.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-right">
                  {editingId === d.id ? (
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={handleUpdate}
                        className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 border border-blue-200 dark:border-blue-700 hover:border-blue-300 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 border border-gray-200 dark:border-gray-600 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <KebabMenu items={[
                      { label: 'Rename', onClick: () => startEdit(d) },
                      d.is_active
                        ? { label: 'Deactivate', onClick: () => handleDeactivate(d.id), variant: 'danger' }
                        : { label: 'Reactivate', onClick: () => handleReactivate(d.id), variant: 'success' },
                    ]} />
                  )}
                </td>
              </tr>
            ))}
            {departments.length === 0 && (
              <tr>
                <td colSpan={3} className="px-5 py-8 text-center text-gray-400 dark:text-gray-500 text-sm">
                  No departments yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
