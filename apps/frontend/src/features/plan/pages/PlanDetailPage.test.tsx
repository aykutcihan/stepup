import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import PlanDetailPage from './PlanDetailPage'

const { mockGetPlan, mockGetUsers, mockCancelTask } = vi.hoisted(() => ({
  mockGetPlan: vi.fn(),
  mockGetUsers: vi.fn(),
  mockCancelTask: vi.fn(),
}))

vi.mock('@/features/plan/services/planService', () => ({
  getPlan: mockGetPlan,
  updatePlan: vi.fn(),
  addTask: vi.fn(),
  updateTaskDeadline: vi.fn(),
  cancelTask: mockCancelTask,
}))
vi.mock('@/features/users/services/userService', () => ({ getUsers: mockGetUsers }))

const mockTask = {
  id: 'task-1', plan_id: 'plan-1', template_task_id: null,
  title: 'Setup environment', deadline: '2026-06-08',
  status: 'not_started' as const, is_required: true, order: 1, created_at: '', description: null,
}

const mockPlan = {
  id: 'plan-1', user_id: 'emp-1', template_id: 'tmpl-1',
  manager_id: 'mgr-1', start_date: '2026-06-01', is_active: true, created_at: '',
  tasks: [mockTask],
}

function renderPage() {
  render(
    <MemoryRouter initialEntries={['/hr/plans/plan-1']}>
      <Routes>
        <Route path="/hr/plans/:id" element={<PlanDetailPage />} />
      </Routes>
    </MemoryRouter>
  )
}

describe('PlanDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetPlan.mockResolvedValue(mockPlan)
    mockGetUsers.mockResolvedValue([])
  })

  it('renders task list with status badge', async () => {
    renderPage()
    await waitFor(() => {
      expect(screen.getByText('Setup environment')).toBeInTheDocument()
      expect(screen.getByText('Not started')).toBeInTheDocument()
    })
  })

  it('cancel button shows inline confirmation', async () => {
    renderPage()
    await waitFor(() => screen.getByText('Setup environment'))

    await userEvent.click(screen.getByRole('button', { name: /^cancel$/i }))

    expect(screen.getByText('Cancel task?')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /yes/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /no/i })).toBeInTheDocument()
  })

  it('confirms cancel and calls cancelTask', async () => {
    mockCancelTask.mockResolvedValue({ ...mockTask, status: 'cancelled' })
    renderPage()
    await waitFor(() => screen.getByText('Setup environment'))

    await userEvent.click(screen.getByRole('button', { name: /^cancel$/i }))
    await userEvent.click(screen.getByRole('button', { name: /yes/i }))

    await waitFor(() => expect(mockCancelTask).toHaveBeenCalledWith('plan-1', 'task-1'))
  })

  it('no button dismisses confirmation', async () => {
    renderPage()
    await waitFor(() => screen.getByText('Setup environment'))

    await userEvent.click(screen.getByRole('button', { name: /^cancel$/i }))
    await userEvent.click(screen.getByRole('button', { name: /no/i }))

    expect(screen.queryByText('Cancel task?')).not.toBeInTheDocument()
  })
})
