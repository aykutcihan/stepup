import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  getTemplates,
  createTemplate,
  updateTemplate,
  activateTemplate,
  deactivateTemplate,
  cloneTemplate,
} from '@/features/template/services/templateService'
import { getDepartments } from '@/features/department/services/departmentService'
import { ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type TemplateResponse = components['schemas']['TemplateResponse']
type DepartmentResponse = components['schemas']['DepartmentResponse']

export function useTemplatesPage() {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<TemplateResponse[]>([])
  const [departments, setDepartments] = useState<DepartmentResponse[]>([])
  const [filterDepartmentId, setFilterDepartmentId] = useState('')
  const [filterStatus, setFilterStatus] = useState<'active' | 'inactive' | ''>('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTemplateName, setNewTemplateName] = useState('')
  const [newTemplateDepartmentId, setNewTemplateDepartmentId] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editingName, setEditingName] = useState('')

  useEffect(() => {
    getTemplates().then(setTemplates).catch(() => {})
    getDepartments().then(setDepartments).catch(() => {})
  }, [])

  const filteredTemplates = templates.filter((t) => {
    if (filterDepartmentId && t.department_id !== filterDepartmentId) return false
    if (filterStatus === 'active' && !t.is_active) return false
    if (filterStatus === 'inactive' && t.is_active) return false
    return true
  })

  function getDepartmentName(departmentId: string): string {
    return departments.find((d) => d.id === departmentId)?.name ?? '—'
  }

  async function handleCreate() {
    if (!newTemplateName.trim() || !newTemplateDepartmentId) return
    const created = await createTemplate({
      name: newTemplateName.trim(),
      department_id: newTemplateDepartmentId,
    })
    setShowCreateForm(false)
    setNewTemplateName('')
    setNewTemplateDepartmentId('')
    navigate(ROUTES.HR_TEMPLATE_DETAIL(created.id))
  }

  function startRename(id: string, currentName: string) {
    setEditingId(id)
    setEditingName(currentName)
  }

  function cancelRename() {
    setEditingId(null)
    setEditingName('')
  }

  async function handleRename() {
    if (!editingId || !editingName.trim()) return
    const updated = await updateTemplate(editingId, { name: editingName.trim() })
    setTemplates((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    setEditingId(null)
    setEditingName('')
  }

  async function handleActivate(id: string) {
    const updated = await activateTemplate(id)
    setTemplates((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
  }

  async function handleDeactivate(id: string) {
    const updated = await deactivateTemplate(id)
    setTemplates((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
  }

  async function handleClone(id: string) {
    const cloned = await cloneTemplate(id)
    setTemplates((prev) => [...prev, cloned])
  }

  return {
    filteredTemplates,
    departments,
    filterDepartmentId,
    setFilterDepartmentId,
    filterStatus,
    setFilterStatus,
    showCreateForm,
    setShowCreateForm,
    newTemplateName,
    setNewTemplateName,
    newTemplateDepartmentId,
    setNewTemplateDepartmentId,
    editingId,
    editingName,
    setEditingName,
    getDepartmentName,
    handleCreate,
    startRename,
    cancelRename,
    handleRename,
    handleActivate,
    handleDeactivate,
    handleClone,
  }
}
