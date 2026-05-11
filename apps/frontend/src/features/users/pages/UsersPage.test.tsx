import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import UsersPage from './UsersPage'
import { useAuthStore } from '@/stores/authStore'

const { mockGetUsers, mockUpdateUser, mockDeactivateUser, mockGetDepartments } = vi.hoisted(() => ({
  mockGetUsers: vi.fn(),
  mockUpdateUser: vi.fn(),
  mockDeactivateUser: vi.fn(),
  mockGetDepartments: vi.fn(),
}))

vi.mock('@/features/users/services/userService', () => ({
  getUsers: mockGetUsers,
  updateUser: mockUpdateUser,
  deactivateUser: mockDeactivateUser,
}))

vi.mock('@/features/department/services/departmentService', () => ({
  getDepartments: mockGetDepartments,
}))

const mockDepartment = { id: 'dept-1', name: 'Engineering', is_active: true, created_at: '2024-01-01T00:00:00Z' }
const mockCurrentUser = { id: 'user-1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const, is_active: true, department_id: null }
const mockEmployee = { id: 'user-2', email: 'emp@example.com', first_name: 'John', last_name: 'Doe', role: 'employee' as const, is_active: true, department_id: null }
const mockManager = { id: 'user-3', email: 'mgr@example.com', first_name: 'Jane', last_name: 'Smith', role: 'manager' as const, is_active: true, department_id: 'dept-1' }

function renderPage() {
  render(
    <MemoryRouter>
      <UsersPage />
    </MemoryRouter>,
  )
}

describe('UsersPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: mockCurrentUser, isLoading: false })
    mockGetUsers.mockResolvedValue([mockCurrentUser, mockEmployee, mockManager])
    mockGetDepartments.mockResolvedValue([mockDepartment])
    mockUpdateUser.mockResolvedValue(mockEmployee)
    mockDeactivateUser.mockResolvedValue(undefined)
  })

  it('displays user list on load', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    })
  })

  it('filters users by role', async () => {
    renderPage()

    await waitFor(() => screen.getByText('John Doe'))

    await userEvent.selectOptions(screen.getByDisplayValue('All roles'), 'manager')

    expect(screen.queryByText('John Doe')).not.toBeInTheDocument()
    expect(screen.getByText('Jane Smith')).toBeInTheDocument()
  })

  it('filters users by status', async () => {
    mockGetUsers.mockResolvedValue([
      mockCurrentUser,
      mockEmployee,
      { ...mockManager, is_active: false },
    ])
    renderPage()

    await waitFor(() => screen.getByText('Jane Smith'))

    await userEvent.selectOptions(screen.getByDisplayValue('All statuses'), 'active')

    expect(screen.getByText('John Doe')).toBeInTheDocument()
    expect(screen.queryByText('Jane Smith')).not.toBeInTheDocument()
  })

  it('assigns department to user', async () => {
    mockUpdateUser.mockResolvedValue({ ...mockEmployee, department_id: 'dept-1' })
    renderPage()

    await waitFor(() => screen.getByText('John Doe'))

    const departmentSelects = screen.getAllByDisplayValue('No department')
    await userEvent.selectOptions(departmentSelects[1], 'dept-1')

    expect(mockUpdateUser).toHaveBeenCalledWith('user-2', { department_id: 'dept-1' })
  })

  it('deactivates a user', async () => {
    renderPage()

    await waitFor(() => screen.getByText('John Doe'))

    const menuButtons = screen.getAllByRole('button', { name: /actions/i })
    await userEvent.click(menuButtons[0])
    await userEvent.click(screen.getByRole('button', { name: /deactivate/i }))

    expect(mockDeactivateUser).toHaveBeenCalledWith('user-2')
  })
})
