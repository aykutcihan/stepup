import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import DepartmentsPage from './DepartmentsPage'

const {
  mockGetDepartments,
  mockCreateDepartment,
  mockUpdateDepartment,
  mockDeactivateDepartment,
} = vi.hoisted(() => ({
  mockGetDepartments: vi.fn(),
  mockCreateDepartment: vi.fn(),
  mockUpdateDepartment: vi.fn(),
  mockDeactivateDepartment: vi.fn(),
}))

vi.mock('@/features/department/services/departmentService', () => ({
  getDepartments: mockGetDepartments,
  createDepartment: mockCreateDepartment,
  updateDepartment: mockUpdateDepartment,
  deactivateDepartment: mockDeactivateDepartment,
  reactivateDepartment: vi.fn(),
}))

const mockDepartment = { id: '1', name: 'Engineering', is_active: true, created_at: '2024-01-01T00:00:00Z' }

function renderPage() {
  render(
    <MemoryRouter>
      <DepartmentsPage />
    </MemoryRouter>,
  )
}

describe('DepartmentsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetDepartments.mockResolvedValue([mockDepartment])
  })

  it('displays department list on load', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Engineering')).toBeInTheDocument()
    })
  })

  it('creates a new department', async () => {
    mockCreateDepartment.mockResolvedValue({
      id: '2', name: 'Marketing', is_active: true, created_at: '2024-01-01T00:00:00Z',
    })
    renderPage()

    await waitFor(() => screen.getByText('Engineering'))

    await userEvent.click(screen.getByRole('button', { name: /\+ add department/i }))
    await userEvent.type(screen.getByPlaceholderText(/department name/i), 'Marketing')
    await userEvent.click(screen.getByRole('button', { name: /^add$/i }))

    await waitFor(() => {
      expect(screen.getByText('Marketing')).toBeInTheDocument()
    })
  })

  it('edits a department name', async () => {
    mockUpdateDepartment.mockResolvedValue({
      ...mockDepartment, name: 'Engineering Updated',
    })
    renderPage()

    await waitFor(() => screen.getByText('Engineering'))

    await userEvent.click(screen.getByRole('button', { name: /actions/i }))
    await userEvent.click(screen.getByRole('button', { name: /rename/i }))
    const input = screen.getByDisplayValue('Engineering')
    await userEvent.clear(input)
    await userEvent.type(input, 'Engineering Updated')
    await userEvent.click(screen.getByRole('button', { name: /save/i }))

    await waitFor(() => {
      expect(screen.getByText('Engineering Updated')).toBeInTheDocument()
    })
  })

  it('shows error when deactivating department with active users', async () => {
    mockDeactivateDepartment.mockRejectedValue({
      response: { data: { error_code: 'DEPARTMENT_HAS_ACTIVE_USERS' } },
    })
    renderPage()

    await waitFor(() => screen.getByText('Engineering'))
    await userEvent.click(screen.getByRole('button', { name: /actions/i }))
    await userEvent.click(screen.getByRole('button', { name: /deactivate/i }))

    await waitFor(() => {
      expect(screen.getByText(/cannot deactivate/i)).toBeInTheDocument()
    })
  })
})
