import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import HRDashboard from './HRDashboard'
import { useAuthStore } from '@/stores/authStore'

const mockCurrentUser = { id: '1', email: 'hr@example.com', first_name: 'HR', last_name: 'Admin', role: 'hr_admin' as const, is_active: true, department_id: null }

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
  })

  it('displays welcome message with user name', () => {
    renderPage()
    expect(screen.getByText(/good (morning|afternoon|evening), hr/i)).toBeInTheDocument()
    expect(screen.getByText(/hr admin/i)).toBeInTheDocument()
  })
})
