import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import RegisterPage from './RegisterPage'

const mockNavigate = vi.fn()
const { mockAuthServiceValidateInvitation, mockAuthServiceRegister } = vi.hoisted(() => ({
  mockAuthServiceValidateInvitation: vi.fn(),
  mockAuthServiceRegister: vi.fn(),
}))

vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>()
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('@/features/auth/services/authService', () => ({
  validateInvitation: mockAuthServiceValidateInvitation,
  register: mockAuthServiceRegister,
}))

const mockUser = {
  id: '1',
  email: 'invited@example.com',
  first_name: 'Jane',
  last_name: 'Doe',
  role: 'employee' as const,
}

function renderWithToken(token: string) {
  render(
    <MemoryRouter initialEntries={[`/register?token=${token}`]}>
      <RegisterPage />
    </MemoryRouter>,
  )
}

describe('RegisterPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('pre-fills email from token validation', async () => {
    mockAuthServiceValidateInvitation.mockResolvedValue({ email: mockUser.email, role: mockUser.role })

    renderWithToken('valid-token')

    await waitFor(() => {
      expect(screen.getByDisplayValue(mockUser.email)).toBeInTheDocument()
    })
  })

  it('shows error message when token is expired', async () => {
    mockAuthServiceValidateInvitation.mockRejectedValue({
      response: { data: { error_code: 'INVITATION_EXPIRED' } },
    })

    renderWithToken('expired-token')

    await waitFor(() => {
      expect(screen.getByText('This invitation link has expired.')).toBeInTheDocument()
    })
  })

  it('navigates to login on successful registration', async () => {
    mockAuthServiceValidateInvitation.mockResolvedValue({ email: mockUser.email, role: mockUser.role })
    mockAuthServiceRegister.mockResolvedValue(mockUser)

    renderWithToken('valid-token')

    await waitFor(() => screen.getByDisplayValue(mockUser.email))

    await userEvent.type(screen.getByPlaceholderText(/first name/i), 'Jane')
    await userEvent.type(screen.getByPlaceholderText(/last name/i), 'Doe')
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'password123')
    await userEvent.click(screen.getByRole('button', { name: /register/i }))

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login')
    })
  })
})
