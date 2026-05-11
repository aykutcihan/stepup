import { Link } from 'react-router-dom'
import { useTemplatesPage } from '@/features/template/hooks/useTemplatesPage'
import { ROUTES } from '@/constants/routes'

export default function TemplatesPage() {
  const {
    filteredTemplates,
    departments,
    filterDepartmentId,
    setFilterDepartmentId,
    filterStatus,
    setFilterStatus,
    openMenuId,
    setOpenMenuId,
    getDepartmentName,
    handleActivate,
    handleDeactivate,
    handleClone,
  } = useTemplatesPage()

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Templates</h2>
        <p className="text-sm text-gray-500 mt-0.5">Manage onboarding templates per department.</p>
      </div>

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
            <div
              key={t.id}
              className="bg-white rounded-xl border border-gray-200 shadow-sm px-6 py-5 flex items-center justify-between"
            >
              <div>
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
              </div>

              <div className="flex items-center gap-2">
                <Link
                  to={ROUTES.HR_TEMPLATE_DETAIL(t.id)}
                  className="text-xs text-blue-600 hover:text-blue-800 border border-blue-200 hover:border-blue-300 px-3 py-1.5 rounded-lg transition-colors"
                >
                  View
                </Link>

                <div className="relative">
                  <button
                    onClick={() => setOpenMenuId(openMenuId === t.id ? null : t.id)}
                    className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors text-lg"
                    aria-label="actions"
                  >
                    ⋮
                  </button>

                  {openMenuId === t.id && (
                    <>
                      <div
                        className="fixed inset-0 z-10"
                        onClick={() => setOpenMenuId(null)}
                      />
                      <div className="absolute right-0 bottom-full mb-1 z-20 bg-white border border-gray-200 rounded-lg shadow-lg py-1 min-w-[150px]">
                        <button
                          onClick={() => { handleClone(t.id); setOpenMenuId(null) }}
                          className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                        >
                          Clone
                        </button>
                        {t.is_active ? (
                          <button
                            onClick={() => { handleDeactivate(t.id); setOpenMenuId(null) }}
                            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                          >
                            Deactivate
                          </button>
                        ) : (
                          <button
                            onClick={() => { handleActivate(t.id); setOpenMenuId(null) }}
                            className="w-full text-left px-4 py-2 text-sm text-green-600 hover:bg-green-50 transition-colors"
                          >
                            Activate
                          </button>
                        )}
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
