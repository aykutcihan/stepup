import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import ManagerTaskReviewPage from './ManagerTaskReviewPage'

const { mockGetPendingApprovals, mockApproveTask, mockReturnTask, mockNavigate } = vi.hoisted(() => ({
  mockGetPendingApprovals: vi.fn(),
  mockApproveTask: vi.fn(),
  mockReturnTask: vi.fn(),
  mockNavigate: vi.fn(),
}))

vi.mock('@/features/plan/services/managerService', () => ({
  getPendingApprovals: mockGetPendingApprovals,
  approveTask: mockApproveTask,
  returnTask: mockReturnTask,
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return { ...actual, useNavigate: () => mockNavigate }
})

const mockTask = {
  id: 'task-1',
  plan_id: 'plan-1',
  title: 'Setup laptop',
  description: 'Install all required software',
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
    <MemoryRouter initialEntries={['/manager/tasks/task-1']}>
      <Routes>
        <Route path="/manager/tasks/:id" element={<ManagerTaskReviewPage />} />
      </Routes>
    </MemoryRouter>
  )
}

describe('ManagerTaskReviewPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetPendingApprovals.mockResolvedValue([mockTask])
  })

  it('renders task detail with approve and return buttons', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Setup laptop')).toBeInTheDocument()
      expect(screen.getByText('John Employee')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /approve/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /return/i })).toBeInTheDocument()
    })
  })

  it('approve button calls approveTask and navigates back', async () => {
    mockApproveTask.mockResolvedValue({ ...mockTask, status: 'approved' })
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /approve/i }))

    await waitFor(() => {
      expect(mockApproveTask).toHaveBeenCalledWith('task-1')
      expect(mockNavigate).toHaveBeenCalledWith('/manager/approvals')
    })
  })

  it('return button opens modal', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /^return$/i }))

    expect(screen.getByText('Return Task')).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/feedback comment/i)).toBeInTheDocument()
  })

  it('submit is disabled when comment is empty', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /^return$/i }))

    expect(screen.getByRole('button', { name: /submit/i })).toBeDisabled()
  })

  it('submit with comment calls returnTask and navigates back', async () => {
    mockReturnTask.mockResolvedValue({ ...mockTask, status: 'in_progress' })
    renderPage()

    await waitFor(() => screen.getByText('Setup laptop'))
    await userEvent.click(screen.getByRole('button', { name: /^return$/i }))
    await userEvent.type(screen.getByPlaceholderText(/feedback comment/i), 'Please redo this.')
    await userEvent.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(mockReturnTask).toHaveBeenCalledWith('task-1', 'Please redo this.')
      expect(mockNavigate).toHaveBeenCalledWith('/manager/approvals')
    })
  })
})
