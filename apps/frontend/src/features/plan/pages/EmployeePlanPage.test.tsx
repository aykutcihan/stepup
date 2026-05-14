import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import EmployeePlanPage from './EmployeePlanPage'

const { mockGetMyPlan, mockStartTask, mockCompleteTask } = vi.hoisted(() => ({
  mockGetMyPlan: vi.fn(),
  mockStartTask: vi.fn(),
  mockCompleteTask: vi.fn(),
}))

vi.mock('@/features/plan/services/planService', () => ({
  getMyPlan: mockGetMyPlan,
  startTask: mockStartTask,
  completeTask: mockCompleteTask,
}))

const mockTaskNotStarted = {
  id: 'task-1', plan_id: 'plan-1', template_task_id: null,
  title: 'Setup laptop', deadline: '2026-12-31',
  status: 'not_started' as const, is_required: true, order: 1, created_at: '', description: null,
}

const mockTaskInProgress = {
  id: 'task-2', plan_id: 'plan-1', template_task_id: null,
  title: 'Read handbook', deadline: '2026-12-31',
  status: 'in_progress' as const, is_required: false, order: 2, created_at: '', description: null,
}

const mockTaskCompleted = {
  id: 'task-3', plan_id: 'plan-1', template_task_id: null,
  title: 'Meet the team', deadline: '2026-12-31',
  status: 'completed' as const, is_required: true, order: 3, created_at: '', description: null,
}

const mockPlan = {
  id: 'plan-1', user_id: 'emp-1', template_id: 'tmpl-1',
  manager_id: 'mgr-1', start_date: '2026-06-01', is_active: true, created_at: '',
  tasks: [mockTaskNotStarted, mockTaskInProgress, mockTaskCompleted],
}

function renderPage() {
  render(
    <MemoryRouter>
      <EmployeePlanPage />
    </MemoryRouter>
  )
}

describe('EmployeePlanPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders task list with correct status badges', async () => {
    mockGetMyPlan.mockResolvedValue(mockPlan)
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Setup laptop')).toBeInTheDocument()
      expect(screen.getByText('Read handbook')).toBeInTheDocument()
      expect(screen.getByText('Meet the team')).toBeInTheDocument()
      expect(screen.getByText('Not started')).toBeInTheDocument()
      expect(screen.getByText('In progress')).toBeInTheDocument()
      expect(screen.getByText('Completed')).toBeInTheDocument()
    })
  })

  it('shows progress count', async () => {
    mockGetMyPlan.mockResolvedValue(mockPlan)
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('1 / 3 tasks done')).toBeInTheDocument()
    })
  })

  it('start button calls startTask and updates status', async () => {
    mockGetMyPlan.mockResolvedValue(mockPlan)
    mockStartTask.mockResolvedValue({ ...mockTaskNotStarted, status: 'in_progress' })
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /start/i }))

    await waitFor(() => expect(mockStartTask).toHaveBeenCalledWith('task-1'))
  })

  it('complete button calls completeTask and updates status', async () => {
    mockGetMyPlan.mockResolvedValue(mockPlan)
    mockCompleteTask.mockResolvedValue({ ...mockTaskInProgress, status: 'completed' })
    renderPage()

    await waitFor(() => screen.getByText('Read handbook'))
    await userEvent.click(screen.getByRole('button', { name: /mark as complete/i }))

    await waitFor(() => expect(mockCompleteTask).toHaveBeenCalledWith('task-2'))
  })

  it('shows empty state when no active plan', async () => {
    mockGetMyPlan.mockRejectedValue(new Error('Not found'))
    renderPage()

    await waitFor(() => {
      expect(screen.getByText(/no active onboarding plan/i)).toBeInTheDocument()
    })
  })
})
