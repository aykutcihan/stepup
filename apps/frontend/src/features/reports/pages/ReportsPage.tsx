import { useState } from 'react'
import { useReports } from '@/features/reports/hooks/useReports'
import { downloadCsv } from '@/features/reports/services/reportsService'
import { API } from '@/constants/apiEndpoints'

export default function ReportsPage() {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const filters = {
    start_date: startDate || undefined,
    end_date: endDate || undefined,
  }

  const { completionTime, taskRates, bottlenecks, loading } = useReports(filters)

  function handleExport(endpoint: string, filename: string) {
    downloadCsv(endpoint, filename, filters)
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Reports</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Onboarding activity analysis and export.</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex flex-col gap-0.5">
            <label className="text-xs text-gray-500 dark:text-gray-400">From</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex flex-col gap-0.5">
            <label className="text-xs text-gray-500 dark:text-gray-400">To</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {loading ? (
        <p className="text-sm text-gray-400 dark:text-gray-500">Loading...</p>
      ) : (
        <>
          <section>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300">Average Completion Time by Department</h3>
              <button
                onClick={() => handleExport(API.REPORTS.COMPLETION_TIME, 'completion-time.csv')}
                className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
              >
                Export CSV
              </button>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
              {completionTime.length === 0 ? (
                <p className="text-sm text-gray-400 dark:text-gray-500 px-5 py-4">No completed plans found.</p>
              ) : (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 dark:border-gray-700">
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Department</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Completed Plans</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Avg. Days to Complete</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {completionTime.map((row) => (
                      <tr key={row.department_name} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                        <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-200">{row.department_name}</td>
                        <td className="px-5 py-3 text-gray-600 dark:text-gray-400">{row.total_plans}</td>
                        <td className="px-5 py-3 text-gray-600 dark:text-gray-400">
                          {row.avg_completion_days_rounded != null ? `${row.avg_completion_days_rounded} days` : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>

          <section>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300">Task Completion Rates by Template</h3>
              <button
                onClick={() => handleExport(API.REPORTS.TASK_COMPLETION_RATES, 'task-completion-rates.csv')}
                className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
              >
                Export CSV
              </button>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
              {taskRates.length === 0 ? (
                <p className="text-sm text-gray-400 dark:text-gray-500 px-5 py-4">No data found.</p>
              ) : (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 dark:border-gray-700">
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Template</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Total Tasks</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Completed</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Completion Rate</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {taskRates.map((row) => (
                      <tr key={row.template_name} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                        <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-200">{row.template_name}</td>
                        <td className="px-5 py-3 text-gray-600 dark:text-gray-400">{row.total_tasks}</td>
                        <td className="px-5 py-3 text-gray-600 dark:text-gray-400">{row.completed_tasks}</td>
                        <td className="px-5 py-3">
                          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                            row.completion_rate >= 75
                              ? 'text-green-700 bg-green-50 dark:text-green-400 dark:bg-green-900/30'
                              : row.completion_rate >= 40
                              ? 'text-yellow-700 bg-yellow-50 dark:text-yellow-400 dark:bg-yellow-900/30'
                              : 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/30'
                          }`}>
                            {row.completion_rate}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>

          <section>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300">Bottlenecks — Most Returned & Overdue Tasks</h3>
              <button
                onClick={() => handleExport(API.REPORTS.BOTTLENECKS, 'bottlenecks.csv')}
                className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
              >
                Export CSV
              </button>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
              {bottlenecks.length === 0 ? (
                <p className="text-sm text-gray-400 dark:text-gray-500 px-5 py-4">No bottlenecks found.</p>
              ) : (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 dark:border-gray-700">
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Task</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Times Returned</th>
                      <th className="text-left text-xs font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Times Overdue</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                    {bottlenecks.map((row) => (
                      <tr key={row.task_title} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                        <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-200">{row.task_title}</td>
                        <td className="px-5 py-3">
                          {row.returned_count > 0 ? (
                            <span className="text-xs font-medium px-2 py-0.5 rounded-full text-orange-600 bg-orange-50 dark:text-orange-400 dark:bg-orange-900/30">
                              {row.returned_count}
                            </span>
                          ) : (
                            <span className="text-gray-400 dark:text-gray-500">0</span>
                          )}
                        </td>
                        <td className="px-5 py-3">
                          {row.overdue_count > 0 ? (
                            <span className="text-xs font-medium px-2 py-0.5 rounded-full text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/30">
                              {row.overdue_count}
                            </span>
                          ) : (
                            <span className="text-gray-400 dark:text-gray-500">0</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>
        </>
      )}
    </div>
  )
}
