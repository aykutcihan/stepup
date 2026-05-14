import { Link } from 'react-router-dom'
import { useTemplatesPage } from '@/features/template/hooks/useTemplatesPage'
import KebabMenu from '@/components/KebabMenu'
import { ROUTES } from '@/constants/routes'

export default function TemplatesPage() {
  const {
    filteredTemplates,
    departments,
    filterDepartmentId,
    setFilterDepartmentId,
    filterStatus,
    setFilterStatus,
    showCreateForm,
    setShowCreateForm,
    newTemplateName,
    setNewTemplateName,
    newTemplateDepartmentId,
    setNewTemplateDepartmentId,
    editingId,
    editingName,
    setEditingName,
    getDepartmentName,
    handleCreate,
    startRename,
    cancelRename,
    handleRename,
    handleActivate,
    handleDeactivate,
    handleClone,
  } = useTemplatesPage()

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Templates</h2>
          <p className="text-sm text-gray-500 mt-0.5">Manage onboarding templates per department.</p>
        </div>
        <button
          onClick={() => setShowCreateForm((v) => !v)}
          className="text-sm bg-blue-700 hover:bg-blue-800 text-white font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {showCreateForm ? 'Cancel' : '+ New Template'}
        </button>
      </div>

      {showCreateForm && (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm px-5 py-4 mb-4 flex gap-2">
          <input
            value={newTemplateName}
            onChange={(e) => setNewTemplateName(e.target.value)}
            placeholder="Template name"
            className="flex-1 border border-gray-300 rounded-lg px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={newTemplateDepartmentId}
            onChange={(e) => setNewTemplateDepartmentId(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select department</option>
            {departments.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
          <button
            onClick={handleCreate}
            disabled={!newTemplateName.trim() || !newTemplateDepartmentId}
            className="bg-blue-700 hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            Create
          </button>
        </div>
      )}

      <div className="flex gap-3 mb-6">
        <select
          value={filterDepartmentId}
          onChange={(e) => setFilterDepartmentId(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All departments</option>
          {departments.map((d) => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as 'active' | 'inactive' | '')}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      {filteredTemplates.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-12">No templates found.</p>
      ) : (
        <div className="grid gap-4">
          {filteredTemplates.map((t) => (
            <div key={t.id} className="relative bg-white rounded-xl border border-gray-200 shadow-sm">
              {editingId === t.id ? (
                <div className="px-6 py-4 flex items-center gap-2">
                  <input
                    value={editingName}
                    onChange={(e) => setEditingName(e.target.value)}
                    className="flex-1 border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    autoFocus
                  />
                  <button
                    onClick={handleRename}
                    className="text-xs text-blue-600 hover:text-blue-800 border border-blue-200 px-3 py-1.5 rounded-lg transition-colors"
                  >
                    Save
                  </button>
                  <button
                    onClick={cancelRename}
                    className="text-xs text-gray-500 hover:text-gray-700 border border-gray-200 px-3 py-1.5 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <Link
                  to={ROUTES.HR_TEMPLATE_DETAIL(t.id)}
                  className="block px-6 py-5 hover:bg-slate-50 rounded-xl transition-colors pr-14"
                >
                  <div className="flex items-center gap-3">
                    <h3 className="text-sm font-semibold text-gray-900">{t.name}</h3>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${
                      t.is_active
                        ? 'bg-green-50 text-green-700 border-green-100'
                        : 'bg-gray-100 text-gray-500 border-gray-200'
                    }`}>
                      {t.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{getDepartmentName(t.department_id)}</p>
                </Link>
              )}

              {editingId !== t.id && (
                <div className="absolute right-4 top-1/2 -translate-y-1/2">
                  <KebabMenu items={[
                    { label: 'Rename', onClick: () => startRename(t.id, t.name) },
                    { label: 'Clone', onClick: () => handleClone(t.id) },
                    t.is_active
                      ? { label: 'Deactivate', onClick: () => handleDeactivate(t.id), variant: 'danger' }
                      : { label: 'Activate', onClick: () => handleActivate(t.id), variant: 'success' },
                  ]} />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
