import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import InviteUserPage from './InviteUserPage'

const { mockInvitationServiceGetInvitations, mockInvitationServiceCreate, mockInvitationServiceResend, mockGetDepartments } = vi.hoisted(
  () => ({
    mockInvitationServiceGetInvitations: vi.fn(),
    mockInvitationServiceCreate: vi.fn(),
    mockInvitationServiceResend: vi.fn(),
    mockGetDepartments: vi.fn(),
  }),
)

vi.mock('@/features/invitation/services/invitationService', () => ({
  getInvitations: mockInvitationServiceGetInvitations,
  createInvitation: mockInvitationServiceCreate,
  resendInvitation: mockInvitationServiceResend,
}))

vi.mock('@/features/department/services/departmentService', () => ({
  getDepartments: mockGetDepartments,
}))

const mockInvitation = {
  id: 'inv-1',
  email: 'newuser@example.com',
  role: 'employee' as const,
  expires_at: '2026-06-01T00:00:00Z',
}

function renderPage() {
  render(
    <MemoryRouter>
      <InviteUserPage />
    </MemoryRouter>,
  )
}

describe('InviteUserPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockInvitationServiceGetInvitations.mockResolvedValue([])
    mockGetDepartments.mockResolvedValue([])
  })

  it('displays pending invitations on load', async () => {
    mockInvitationServiceGetInvitations.mockResolvedValue([mockInvitation])

    renderPage()

    await waitFor(() => {
      expect(screen.getByText(/newuser@example.com/i)).toBeInTheDocument()
    })
  })

  it('shows success message after sending invitation', async () => {
    mockInvitationServiceCreate.mockResolvedValue(mockInvitation)
    mockInvitationServiceGetInvitations.mockResolvedValue([mockInvitation])

    renderPage()

    await userEvent.type(screen.getByPlaceholderText(/name@company.com/i), 'newuser@example.com')
    await userEvent.click(screen.getByRole('button', { name: /send invitation/i }))

    await waitFor(() => {
      expect(screen.getByText('Invitation sent successfully.')).toBeInTheDocument()
    })
  })

  it('calls resendInvitation when resend button is clicked', async () => {
    mockInvitationServiceGetInvitations.mockResolvedValue([mockInvitation])
    mockInvitationServiceResend.mockResolvedValue(mockInvitation)

    renderPage()

    await waitFor(() => screen.getByText(/newuser@example.com/i))

    await userEvent.click(screen.getByRole('button', { name: /resend/i }))

    await waitFor(() => {
      expect(mockInvitationServiceResend).toHaveBeenCalledWith('inv-1')
    })
  })
})
