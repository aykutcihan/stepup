import { useCreatePlanPage } from '@/features/plan/hooks/useCreatePlanPage'

const selectCls = 'w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500'

export default function CreatePlanPage() {
  const {
    employees, managers, templates,
    userId, setUserId,
    templateId, setTemplateId,
    managerId, setManagerId,
    startDate, setStartDate,
    error, submitting,
    handleSubmit,
  } = useCreatePlanPage()

  return (
    <div className="max-w-xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Create Onboarding Plan</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Assign an onboarding plan to an employee.</p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-6 py-6 space-y-4">
        {error && (
          <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Employee</label>
          <select value={userId} onChange={(e) => setUserId(e.target.value)} className={selectCls}>
            <option value="">Select employee</option>
            {employees.map((u) => (
              <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Template</label>
          <select value={templateId} onChange={(e) => setTemplateId(e.target.value)} className={selectCls}>
            <option value="">Select template</option>
            {templates.map((t) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Manager</label>
          <select value={managerId} onChange={(e) => setManagerId(e.target.value)} className={selectCls}>
            <option value="">Select manager</option>
            {managers.map((u) => (
              <option key={u.id} value={u.id}>{u.first_name} {u.last_name}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className={selectCls}
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={submitting || !userId || !templateId || !managerId || !startDate}
          className="w-full bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white text-sm font-medium px-4 py-2.5 rounded-lg transition-colors"
        >
          {submitting ? 'Creating...' : 'Create Plan'}
        </button>
      </div>
    </div>
  )
}
