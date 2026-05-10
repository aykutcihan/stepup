import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import ProfilePage from './ProfilePage'
import { useAuthStore } from '@/stores/authStore'

const { mockUpdateMe } = vi.hoisted(() => ({
  mockUpdateMe: vi.fn(),
}))

vi.mock('@/features/users/services/userService', () => ({
  updateMe: mockUpdateMe,
}))

const mockUser = {
  id: 'user-1',
  email: 'hr@example.com',
  first_name: 'Jane',
  last_name: 'Doe',
  role: 'hr_admin' as const,
  is_active: true,
  department_id: null,
  department_name: 'Engineering',
}

function renderPage() {
  render(
    <MemoryRouter>
      <ProfilePage />
    </MemoryRouter>,
  )
}

describe('ProfilePage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: mockUser, isLoading: false })
  })

  it('renders user data correctly', () => {
    renderPage()

    expect(screen.getByDisplayValue('Jane')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Doe')).toBeInTheDocument()
    expect(screen.getByDisplayValue('hr@example.com')).toBeInTheDocument()
    expect(screen.getByDisplayValue('HR Admin')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Engineering')).toBeInTheDocument()
  })

  it('email and role inputs are read-only', () => {
    renderPage()

    expect(screen.getByDisplayValue('hr@example.com')).toHaveAttribute('readonly')
    expect(screen.getByDisplayValue('HR Admin')).toHaveAttribute('readonly')
  })

  it('updates name successfully', async () => {
    mockUpdateMe.mockResolvedValue({ ...mockUser, first_name: 'Janet', last_name: 'Doe' })
    renderPage()

    const firstNameInput = screen.getByDisplayValue('Jane')
    await userEvent.clear(firstNameInput)
    await userEvent.type(firstNameInput, 'Janet')

    await userEvent.click(screen.getByRole('button', { name: /save changes/i }))

    await waitFor(() => {
      expect(mockUpdateMe).toHaveBeenCalledWith({ first_name: 'Janet', last_name: 'Doe' })
      expect(screen.getByText('Profile updated successfully.')).toBeInTheDocument()
    })
  })

  it('shows error message on save failure', async () => {
    mockUpdateMe.mockRejectedValue(new Error('Network error'))
    renderPage()

    await userEvent.click(screen.getByRole('button', { name: /save changes/i }))

    await waitFor(() => {
      expect(screen.getByText('Something went wrong. Please try again.')).toBeInTheDocument()
    })
  })
})
