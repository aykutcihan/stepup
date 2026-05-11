import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import TemplatesPage from './TemplatesPage'

const { mockGetTemplates, mockGetDepartments, mockActivateTemplate, mockDeactivateTemplate, mockCloneTemplate } = vi.hoisted(() => ({
  mockGetTemplates: vi.fn(),
  mockGetDepartments: vi.fn(),
  mockActivateTemplate: vi.fn(),
  mockDeactivateTemplate: vi.fn(),
  mockCloneTemplate: vi.fn(),
}))

vi.mock('@/features/template/services/templateService', () => ({
  getTemplates: mockGetTemplates,
  activateTemplate: mockActivateTemplate,
  deactivateTemplate: mockDeactivateTemplate,
  cloneTemplate: mockCloneTemplate,
}))

vi.mock('@/features/department/services/departmentService', () => ({
  getDepartments: mockGetDepartments,
}))

const mockDepartment = { id: 'dept-1', name: 'Engineering', is_active: true, created_at: '2024-01-01T00:00:00Z' }
const mockActiveTemplate = { id: 'tmpl-1', name: 'Engineering Onboarding', department_id: 'dept-1', is_active: true, created_at: '2024-01-01T00:00:00Z' }
const mockInactiveTemplate = { id: 'tmpl-2', name: 'Marketing Onboarding', department_id: 'dept-1', is_active: false, created_at: '2024-01-01T00:00:00Z' }

function renderPage() {
  render(
    <MemoryRouter>
      <TemplatesPage />
    </MemoryRouter>,
  )
}

describe('TemplatesPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetTemplates.mockResolvedValue([mockActiveTemplate, mockInactiveTemplate])
    mockGetDepartments.mockResolvedValue([mockDepartment])
    mockActivateTemplate.mockResolvedValue({ ...mockInactiveTemplate, is_active: true })
    mockDeactivateTemplate.mockResolvedValue({ ...mockActiveTemplate, is_active: false })
    mockCloneTemplate.mockResolvedValue({ ...mockActiveTemplate, id: 'tmpl-3', name: 'Engineering Onboarding (copy)', is_active: false })
  })

  it('displays template list on load', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Engineering Onboarding')).toBeInTheDocument()
      expect(screen.getByText('Marketing Onboarding')).toBeInTheDocument()
    })
  })

  it('filters templates by status', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Engineering Onboarding'))

    await userEvent.selectOptions(screen.getByDisplayValue('All statuses'), 'active')

    expect(screen.getByText('Engineering Onboarding')).toBeInTheDocument()
    expect(screen.queryByText('Marketing Onboarding')).not.toBeInTheDocument()
  })

  it('calls clone with correct id', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Engineering Onboarding'))

    const menuButtons = screen.getAllByRole('button', { name: /actions/i })
    await userEvent.click(menuButtons[0])
    await userEvent.click(screen.getByRole('button', { name: /^clone$/i }))

    expect(mockCloneTemplate).toHaveBeenCalledWith('tmpl-1')
  })

  it('calls deactivate and updates status', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Engineering Onboarding'))

    const menuButtons = screen.getAllByRole('button', { name: /actions/i })
    await userEvent.click(menuButtons[0])
    await userEvent.click(screen.getByRole('button', { name: /deactivate/i }))

    expect(mockDeactivateTemplate).toHaveBeenCalledWith('tmpl-1')
  })

  it('calls activate on inactive template', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Marketing Onboarding'))

    const menuButtons = screen.getAllByRole('button', { name: /actions/i })
    await userEvent.click(menuButtons[1])
    await userEvent.click(screen.getByRole('button', { name: /^activate$/i }))

    expect(mockActivateTemplate).toHaveBeenCalledWith('tmpl-2')
  })
})
