import { useDepartmentsPage } from '@/features/department/hooks/useDepartmentsPage'

export default function DepartmentsPage() {
  const {
    departments,
    newName,
    setNewName,
    editingId,
    editingName,
    setEditingName,
    pageError,
    openMenuId,
    setOpenMenuId,
    handleCreate,
    startEdit,
    cancelEdit,
    handleUpdate,
    handleDeactivate,
    handleReactivate,
  } = useDepartmentsPage()

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Departments</h2>
        <p className="text-sm text-gray-500 mt-0.5">Manage your organisation's departments.</p>
      </div>

      {pageError && (
        <div className="mb-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          {pageError}
        </div>
      )}

      <div className="flex gap-2 mb-6">
        <input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New department name"
          className="flex-1 border border-gray-300 rounded-lg px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleCreate}
          className="bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          Add
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50 text-left">
              <th className="px-5 py-3.5 font-medium text-gray-600 rounded-tl-xl">Name</th>
              <th className="px-5 py-3.5 font-medium text-gray-600">Status</th>
              <th className="px-5 py-3.5 font-medium text-gray-600 text-right rounded-tr-xl">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {departments.map((d) => (
              <tr key={d.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3.5">
                  {editingId === d.id ? (
                    <input
                      value={editingName}
                      onChange={(e) => setEditingName(e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <span className="font-medium text-gray-900">{d.name}</span>
                  )}
                </td>
                <td className="px-5 py-3.5">
                  <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium border ${
                    d.is_active
                      ? 'bg-green-50 text-green-700 border-green-100'
                      : 'bg-gray-100 text-gray-500 border-gray-200'
                  }`}>
                    {d.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-right">
                  {editingId === d.id ? (
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={handleUpdate}
                        className="text-xs text-blue-600 hover:text-blue-800 border border-blue-200 hover:border-blue-300 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="text-xs text-gray-500 hover:text-gray-700 border border-gray-200 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="relative flex justify-end">
                      <button
                        onClick={() => setOpenMenuId(openMenuId === d.id ? null : d.id)}
                        className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors text-lg"
                        aria-label="actions"
                      >
                        ⋮
                      </button>

                      {openMenuId === d.id && (
                        <>
                          <div
                            className="fixed inset-0 z-10"
                            onClick={() => setOpenMenuId(null)}
                          />
                          <div className="absolute right-0 bottom-full mb-1 z-20 bg-white border border-gray-200 rounded-lg shadow-lg py-1 min-w-[140px]">
                            <button
                              onClick={() => { startEdit(d); setOpenMenuId(null) }}
                              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                            >
                              Edit name
                            </button>
                            {d.is_active ? (
                              <button
                                onClick={() => { handleDeactivate(d.id); setOpenMenuId(null) }}
                                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                              >
                                Deactivate
                              </button>
                            ) : (
                              <button
                                onClick={() => { handleReactivate(d.id); setOpenMenuId(null) }}
                                className="w-full text-left px-4 py-2 text-sm text-green-600 hover:bg-green-50 transition-colors"
                              >
                                Reactivate
                              </button>
                            )}
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </td>
              </tr>
            ))}
            {departments.length === 0 && (
              <tr>
                <td colSpan={3} className="px-5 py-8 text-center text-gray-400 text-sm">
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
