import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import RequireRole from './RequireRole'
import { useAuthStore } from '@/stores/authStore'

const mockHrAdmin = { id: '1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const }
const mockEmployee = { id: '2', email: 'emp@example.com', first_name: 'Emp', last_name: 'User', role: 'employee' as const }

function renderWithRoutes(roles: ('hr_admin' | 'manager' | 'employee')[]) {
  render(
    <MemoryRouter initialEntries={['/protected']}>
      <Routes>
        <Route element={<RequireRole roles={roles} />}>
          <Route path="/protected" element={<div>Protected Content</div>} />
        </Route>
        <Route path="/login" element={<div>Login Page</div>} />
        <Route path="/403" element={<div>Forbidden Page</div>} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('RequireRole', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: null, isLoading: false })
  })

  it('renders nothing while loading', () => {
    useAuthStore.setState({ user: null, isLoading: true })

    renderWithRoutes(['hr_admin'])

    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument()
  })

  it('redirects to login when user is not authenticated', () => {
    useAuthStore.setState({ user: null, isLoading: false })

    renderWithRoutes(['hr_admin'])

    expect(screen.getByText('Login Page')).toBeInTheDocument()
  })

  it('redirects to 403 when user role is not allowed', () => {
    useAuthStore.setState({ user: mockEmployee, isLoading: false })

    renderWithRoutes(['hr_admin'])

    expect(screen.getByText('Forbidden Page')).toBeInTheDocument()
  })

  it('renders outlet when user role is allowed', () => {
    useAuthStore.setState({ user: mockHrAdmin, isLoading: false })

    renderWithRoutes(['hr_admin'])

    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })
})
