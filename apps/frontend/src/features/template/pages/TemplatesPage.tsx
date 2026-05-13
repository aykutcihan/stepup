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

                <KebabMenu items={[
                  { label: 'Clone', onClick: () => handleClone(t.id) },
                  t.is_active
                    ? { label: 'Deactivate', onClick: () => handleDeactivate(t.id), variant: 'danger' }
                    : { label: 'Activate', onClick: () => handleActivate(t.id), variant: 'success' },
                ]} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
