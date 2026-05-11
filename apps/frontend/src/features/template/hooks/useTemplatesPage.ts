import { useEffect, useState } from 'react'
import {
  getTemplates,
  activateTemplate,
  deactivateTemplate,
  cloneTemplate,
} from '@/features/template/services/templateService'
import { getDepartments } from '@/features/department/services/departmentService'
import type { components } from '@/types/api'

type TemplateResponse = components['schemas']['TemplateResponse']
type DepartmentResponse = components['schemas']['DepartmentResponse']

export function useTemplatesPage() {
  const [templates, setTemplates] = useState<TemplateResponse[]>([])
  const [departments, setDepartments] = useState<DepartmentResponse[]>([])
  const [filterDepartmentId, setFilterDepartmentId] = useState('')
  const [filterStatus, setFilterStatus] = useState<'active' | 'inactive' | ''>('')
  const [openMenuId, setOpenMenuId] = useState<string | null>(null)

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
    openMenuId,
    setOpenMenuId,
    getDepartmentName,
    handleActivate,
    handleDeactivate,
    handleClone,
  }
}
