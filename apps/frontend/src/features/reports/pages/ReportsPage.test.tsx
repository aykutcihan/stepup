import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import ReportsPage from './ReportsPage'
import * as reportsService from '@/features/reports/services/reportsService'

vi.mock('@/features/reports/services/reportsService')

const mockCompletionTime = [
  { department_name: 'Engineering', total_plans: 3, avg_completion_days: 12.5, avg_completion_days_rounded: 12.5 },
]
const mockTaskRates = [
  { template_name: 'Dev Onboarding', total_tasks: 10, completed_tasks: 8, completion_rate: 80 },
]
const mockBottlenecks = [
  { task_title: 'Write Tests', returned_count: 3, overdue_count: 1 },
]

function renderPage() {
  render(
    <MemoryRouter>
      <ReportsPage />
    </MemoryRouter>,
  )
}

describe('ReportsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(reportsService.getCompletionTime).mockResolvedValue(mockCompletionTime)
    vi.mocked(reportsService.getTaskCompletionRates).mockResolvedValue(mockTaskRates)
    vi.mocked(reportsService.getBottlenecks).mockResolvedValue(mockBottlenecks)
  })

  it('renders section headings', async () => {
    renderPage()
    expect(await screen.findByText(/average completion time by department/i)).toBeInTheDocument()
    expect(screen.getByText(/task completion rates by template/i)).toBeInTheDocument()
    expect(screen.getByText(/bottlenecks/i)).toBeInTheDocument()
  })

  it('renders completion time data', async () => {
    renderPage()
    expect(await screen.findByText('Engineering')).toBeInTheDocument()
    expect(screen.getByText('12.5 days')).toBeInTheDocument()
  })

  it('renders task completion rate data', async () => {
    renderPage()
    expect(await screen.findByText('Dev Onboarding')).toBeInTheDocument()
    expect(screen.getByText('80%')).toBeInTheDocument()
  })

  it('renders bottleneck data', async () => {
    renderPage()
    expect(await screen.findByText('Write Tests')).toBeInTheDocument()
  })

  it('renders three export CSV buttons', async () => {
    renderPage()
    const buttons = await screen.findAllByText(/export csv/i)
    expect(buttons).toHaveLength(3)
  })
})
