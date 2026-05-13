import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import CreatePlanPage from './CreatePlanPage'
import { useAuthStore } from '@/stores/authStore'

const { mockGetUsers, mockGetTemplates, mockCreatePlan, mockNavigate } = vi.hoisted(() => ({
  mockGetUsers: vi.fn(),
  mockGetTemplates: vi.fn(),
  mockCreatePlan: vi.fn(),
  mockNavigate: vi.fn(),
}))

vi.mock('@/features/users/services/userService', () => ({ getUsers: mockGetUsers }))
vi.mock('@/features/template/services/templateService', () => ({ getTemplates: mockGetTemplates }))
vi.mock('@/features/plan/services/planService', () => ({ createPlan: mockCreatePlan }))
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return { ...actual, useNavigate: () => mockNavigate }
})

const mockEmployee = { id: 'emp-1', email: 'e@test.com', first_name: 'John', last_name: 'Doe', role: 'employee' as const, is_active: true, department_id: null }
const mockManager = { id: 'mgr-1', email: 'm@test.com', first_name: 'Jane', last_name: 'Smith', role: 'manager' as const, is_active: true, department_id: null }
const mockTemplate = { id: 'tmpl-1', name: 'Engineering Onboarding', department_id: 'dept-1', is_active: true, created_at: '' }

function renderPage() {
  render(<MemoryRouter><CreatePlanPage /></MemoryRouter>)
}

describe('CreatePlanPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useAuthStore.setState({ user: { id: 'admin-1', role: 'hr_admin' } as any, isLoading: false })
    mockGetUsers.mockResolvedValue([mockEmployee, mockManager])
    mockGetTemplates.mockResolvedValue([mockTemplate])
    mockCreatePlan.mockResolvedValue({ id: 'plan-1' })
  })

  it('renders employee, template and manager options', async () => {
    renderPage()
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Engineering Onboarding')).toBeInTheDocument()
      expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    })
  })

  it('submits form and navigates to plan detail', async () => {
    renderPage()
    await waitFor(() => screen.getByText('John Doe'))

    const selects = screen.getAllByRole('combobox')
    await userEvent.selectOptions(selects[0], 'emp-1')
    await userEvent.selectOptions(selects[1], 'tmpl-1')
    await userEvent.selectOptions(selects[2], 'mgr-1')
    await userEvent.type(screen.getByDisplayValue(''), '2026-06-01')

    await userEvent.click(screen.getByRole('button', { name: /create plan/i }))

    await waitFor(() => {
      expect(mockCreatePlan).toHaveBeenCalledWith({
        user_id: 'emp-1',
        template_id: 'tmpl-1',
        manager_id: 'mgr-1',
        start_date: expect.any(String),
      })
      expect(mockNavigate).toHaveBeenCalledWith('/hr/plans/plan-1')
    })
  })
})
