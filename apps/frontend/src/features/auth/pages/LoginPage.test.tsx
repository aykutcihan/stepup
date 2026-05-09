import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import LoginPage from './LoginPage'

const mockNavigate = vi.fn()
const { mockAuthServiceLogin, mockAuthServiceGetMe } = vi.hoisted(() => ({
  mockAuthServiceLogin: vi.fn(),
  mockAuthServiceGetMe: vi.fn(),
}))

vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>()
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('@/features/auth/services/authService', () => ({
  login: mockAuthServiceLogin,
  getMe: mockAuthServiceGetMe,
}))

const mockHrAdmin = { id: '1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const }
const mockManager = { id: '2', email: 'mgr@example.com', first_name: 'Manager', last_name: 'User', role: 'manager' as const }
const mockEmployee = { id: '3', email: 'emp@example.com', first_name: 'Employee', last_name: 'User', role: 'employee' as const }

function renderPage(search = '') {
  render(
    <MemoryRouter initialEntries={[`/login${search}`]}>
      <LoginPage />
    </MemoryRouter>,
  )
}

async function fillAndSubmit(email: string, password: string) {
  await userEvent.type(screen.getByPlaceholderText(/email/i), email)
  await userEvent.type(screen.getByPlaceholderText(/password/i), password)
  await userEvent.click(screen.getByRole('button', { name: /sign in/i }))
}

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockAuthServiceLogin.mockResolvedValue(undefined)
  })

  it('renders email and password inputs', () => {
    renderPage()

    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument()
  })

  it('shows error message from URL error param', () => {
    renderPage('?error=USER_DEACTIVATED')

    expect(screen.getByText('Your account has been deactivated. Please contact your HR Admin.')).toBeInTheDocument()
  })

  it('navigates to HR dashboard on successful login as hr_admin', async () => {
    mockAuthServiceGetMe.mockResolvedValue(mockHrAdmin)

    renderPage()
    await fillAndSubmit('hr@example.com', 'password123')

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/hr/dashboard')
    })
  })

  it('navigates to manager dashboard on successful login as manager', async () => {
    mockAuthServiceGetMe.mockResolvedValue(mockManager)

    renderPage()
    await fillAndSubmit('mgr@example.com', 'password123')

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/manager/dashboard')
    })
  })

  it('navigates to employee dashboard on successful login as employee', async () => {
    mockAuthServiceGetMe.mockResolvedValue(mockEmployee)

    renderPage()
    await fillAndSubmit('emp@example.com', 'password123')

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/employee/dashboard')
    })
  })
})
