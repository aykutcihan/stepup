import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import ManagerApprovalsPage from './ManagerApprovalsPage'

const { mockGetPendingApprovals, mockApproveTask, mockNavigate } = vi.hoisted(() => ({
  mockGetPendingApprovals: vi.fn(),
  mockApproveTask: vi.fn(),
  mockNavigate: vi.fn(),
}))

vi.mock('@/features/plan/services/managerService', () => ({
  getPendingApprovals: mockGetPendingApprovals,
  approveTask: mockApproveTask,
  returnTask: vi.fn(),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return { ...actual, useNavigate: () => mockNavigate }
})

const mockTask = {
  id: 'task-1',
  plan_id: 'plan-1',
  title: 'Setup laptop',
  description: null,
  deadline: '2026-06-08',
  status: 'completed' as const,
  is_required: true,
  order: 1,
  created_at: '',
  employee_name: 'John Employee',
  plan_start_date: '2026-06-01',
}

function renderPage() {
  render(
    <MemoryRouter>
      <ManagerApprovalsPage />
    </MemoryRouter>
  )
}

describe('ManagerApprovalsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders pending task list with employee name and deadline', async () => {
    mockGetPendingApprovals.mockResolvedValue([mockTask])
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Setup laptop')).toBeInTheDocument()
      expect(screen.getByText('John Employee · Due: 2026-06-08')).toBeInTheDocument()
    })
  })

  it('shows empty state when no pending tasks', async () => {
    mockGetPendingApprovals.mockResolvedValue([])
    renderPage()

    await waitFor(() => {
      expect(screen.getByText(/no tasks pending approval/i)).toBeInTheDocument()
    })
  })

  it('approve button calls approveTask and removes task from list', async () => {
    mockGetPendingApprovals.mockResolvedValue([mockTask])
    mockApproveTask.mockResolvedValue({ ...mockTask, status: 'approved' })
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /approve/i }))

    await waitFor(() => expect(mockApproveTask).toHaveBeenCalledWith('task-1'))
  })

  it('review button navigates to task review page', async () => {
    mockGetPendingApprovals.mockResolvedValue([mockTask])
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /review/i }))

    expect(mockNavigate).toHaveBeenCalledWith('/manager/tasks/task-1')
  })
})
