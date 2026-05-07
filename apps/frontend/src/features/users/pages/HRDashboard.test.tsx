import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import HRDashboard from './HRDashboard'
import { useAuthStore } from '@/stores/authStore'

const mockNavigate = vi.fn()
const { mockUserServiceGetUsers, mockUserServiceDeactivate, mockAuthServiceLogout } = vi.hoisted(() => ({
  mockUserServiceGetUsers: vi.fn(),
  mockUserServiceDeactivate: vi.fn(),
  mockAuthServiceLogout: vi.fn(),
}))

vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>()
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('@/features/users/services/userService', () => ({
  getUsers: mockUserServiceGetUsers,
  deactivateUser: mockUserServiceDeactivate,
}))

vi.mock('@/features/auth/services/authService', () => ({
  logout: mockAuthServiceLogout,
}))

const mockCurrentUser = { id: '1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const }
const mockOtherUser = { id: '2', email: 'emp@example.com', first_name: 'John', last_name: 'Doe', role: 'employee' as const }

function renderPage() {
  render(
    <MemoryRouter>
      <HRDashboard />
    </MemoryRouter>,
  )
}

describe('HRDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: mockCurrentUser, isLoading: false })
    mockUserServiceGetUsers.mockResolvedValue([mockCurrentUser, mockOtherUser])
    mockUserServiceDeactivate.mockResolvedValue(undefined)
    mockAuthServiceLogout.mockResolvedValue(undefined)
  })

  it('displays user list on load', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument()
    })
  })

  it('removes user from list after deactivation', async () => {
    renderPage()

    await waitFor(() => screen.getByText(/john doe/i))

    await userEvent.click(screen.getByRole('button', { name: /deactivate/i }))

    await waitFor(() => {
      expect(screen.queryByText(/john doe/i)).not.toBeInTheDocument()
    })
  })

  it('navigates to login after logout', async () => {
    renderPage()

    await userEvent.click(screen.getByRole('button', { name: /logout/i }))

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login')
    })
  })
})
