import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import TemplateDetailPage from './TemplateDetailPage'

const { mockGetTemplates, mockGetTasks, mockAddTask, mockUpdateTask, mockDeleteTask, mockReorderTask } = vi.hoisted(() => ({
  mockGetTemplates: vi.fn(),
  mockGetTasks: vi.fn(),
  mockAddTask: vi.fn(),
  mockUpdateTask: vi.fn(),
  mockDeleteTask: vi.fn(),
  mockReorderTask: vi.fn(),
}))

vi.mock('@/features/template/services/templateService', () => ({
  getTemplates: mockGetTemplates,
  getTasks: mockGetTasks,
  addTask: mockAddTask,
  updateTask: mockUpdateTask,
  deleteTask: mockDeleteTask,
  reorderTask: mockReorderTask,
  activateTemplate: vi.fn(),
  deactivateTemplate: vi.fn(),
}))

const mockTemplate = { id: 'tmpl-1', name: 'Engineering Onboarding', department_id: 'dept-1', is_active: false, created_at: '2024-01-01T00:00:00Z' }
const mockTask = { id: 'task-1', template_id: 'tmpl-1', title: 'Sign contract', description: null, order: 1, deadline_days: 1, is_required: true, created_at: '2024-01-01T00:00:00Z' }

function renderPage() {
  render(
    <MemoryRouter initialEntries={['/hr/templates/tmpl-1']}>
      <Routes>
        <Route path="/hr/templates/:id" element={<TemplateDetailPage />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('TemplateDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetTemplates.mockResolvedValue([mockTemplate])
    mockGetTasks.mockResolvedValue([mockTask])
    mockAddTask.mockResolvedValue({ ...mockTask, id: 'task-2', title: 'Setup laptop', order: 2 })
    mockUpdateTask.mockResolvedValue({ ...mockTask, title: 'Sign contract updated' })
    mockDeleteTask.mockResolvedValue(undefined)
    mockReorderTask.mockResolvedValue({ ...mockTask, order: 2 })
  })

  it('displays task list on load', async () => {
    renderPage()

    await waitFor(() => {
      expect(screen.getByText('Sign contract')).toBeInTheDocument()
    })
  })

  it('opens add task form on button click', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Sign contract'))

    await userEvent.click(screen.getByRole('button', { name: /\+ add task/i }))

    expect(screen.getByPlaceholderText('Title')).toBeInTheDocument()
  })

  it('adds a new task', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Sign contract'))

    await userEvent.click(screen.getByRole('button', { name: /\+ add task/i }))
    await userEvent.type(screen.getByPlaceholderText('Title'), 'Setup laptop')
    await userEvent.click(screen.getByRole('button', { name: /^add task$/i }))

    expect(mockAddTask).toHaveBeenCalledWith('tmpl-1', expect.objectContaining({ title: 'Setup laptop' }))
  })

  it('opens edit form and updates task', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Sign contract'))

    await userEvent.click(screen.getByRole('button', { name: /edit/i }))

    const titleInputs = screen.getAllByPlaceholderText('Title')
    await userEvent.clear(titleInputs[0])
    await userEvent.type(titleInputs[0], 'Sign contract updated')
    await userEvent.click(screen.getByRole('button', { name: /^save$/i }))

    expect(mockUpdateTask).toHaveBeenCalledWith('tmpl-1', 'task-1', expect.objectContaining({ title: 'Sign contract updated' }))
  })

  it('deletes a task', async () => {
    renderPage()

    await waitFor(() => screen.getByText('Sign contract'))

    await userEvent.click(screen.getByRole('button', { name: /delete/i }))

    expect(mockDeleteTask).toHaveBeenCalledWith('tmpl-1', 'task-1')
  })

  it('calls reorder when down arrow clicked', async () => {
    mockGetTasks.mockResolvedValue([
      mockTask,
      { ...mockTask, id: 'task-2', title: 'Setup laptop', order: 2 },
    ])
    renderPage()

    await waitFor(() => screen.getByText('Sign contract'))

    const downButtons = screen.getAllByText('↓')
    await userEvent.click(downButtons[0])

    expect(mockReorderTask).toHaveBeenCalledWith('tmpl-1', 'task-1', 2)
  })
})
