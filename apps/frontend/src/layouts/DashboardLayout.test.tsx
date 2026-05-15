import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import DashboardLayout from './DashboardLayout'
import { useAuthStore } from '@/stores/authStore'

const mockNavigate = vi.fn()
const { mockAuthServiceLogout } = vi.hoisted(() => ({
  mockAuthServiceLogout: vi.fn(),
}))

vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>()
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('@/features/auth/services/authService', () => ({
  logout: mockAuthServiceLogout,
}))

const mockUser = { id: '1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const, is_active: true, department_id: null }

function renderLayout() {
  render(
    <MemoryRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route index element={<div>Dashboard content</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  )
}

describe('DashboardLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: mockUser, isLoading: false })
    mockAuthServiceLogout.mockResolvedValue(undefined)
  })

  it('navigates to login after logout', async () => {
    renderLayout()

    await userEvent.click(screen.getByRole('button', { name: /user menu/i }))
    await userEvent.click(screen.getByRole('button', { name: /logout/i }))

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login')
    })
  })
})
