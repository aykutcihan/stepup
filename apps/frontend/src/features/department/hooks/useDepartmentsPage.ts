import { useEffect, useState } from 'react'
import {
  getDepartments,
  createDepartment,
  updateDepartment,
  deactivateDepartment,
  reactivateDepartment,
} from '@/features/department/services/departmentService'
import type { components } from '@/types/api'
import { ERROR_MESSAGES } from '@/constants/errorMessages'

type DepartmentResponse = components['schemas']['DepartmentResponse']

export function useDepartmentsPage() {
  const [departments, setDepartments] = useState<DepartmentResponse[]>([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [newName, setNewName] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editingName, setEditingName] = useState('')
  const [pageError, setPageError] = useState('')

  useEffect(() => {
    getDepartments().then(setDepartments).catch(() => {})
  }, [])

  async function handleCreate() {
    if (!newName.trim()) return
    const created = await createDepartment({ name: newName.trim() })
    setDepartments((prev) => [...prev, created])
    setNewName('')
    setShowAddForm(false)
  }

  function startEdit(department: DepartmentResponse) {
    setEditingId(department.id)
    setEditingName(department.name)
  }

  function cancelEdit() {
    setEditingId(null)
    setEditingName('')
  }

  async function handleUpdate() {
    if (!editingId || !editingName.trim()) return
    const updated = await updateDepartment(editingId, { name: editingName.trim() })
    setDepartments((prev) => prev.map((d) => (d.id === updated.id ? updated : d)))
    setEditingId(null)
    setEditingName('')
  }

  async function handleDeactivate(id: string) {
    setDepartments((prev) => prev.map((d) => (d.id === id ? { ...d, is_active: false } : d)))
    try {
      const updated = await deactivateDepartment(id)
      setDepartments((prev) => prev.map((d) => (d.id === updated.id ? updated : d)))
      setPageError('')
    } catch (err: unknown) {
      setDepartments((prev) => prev.map((d) => (d.id === id ? { ...d, is_active: true } : d)))
      const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
      setPageError(ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong.')
    }
  }

  async function handleReactivate(id: string) {
    setDepartments((prev) => prev.map((d) => (d.id === id ? { ...d, is_active: true } : d)))
    try {
      const updated = await reactivateDepartment(id)
      setDepartments((prev) => prev.map((d) => (d.id === updated.id ? updated : d)))
    } catch {
      setDepartments((prev) => prev.map((d) => (d.id === id ? { ...d, is_active: false } : d)))
    }
  }

  return {
    departments,
    showAddForm,
    setShowAddForm,
    newName,
    setNewName,
    editingId,
    editingName,
    setEditingName,
    pageError,
    handleCreate,
    startEdit,
    cancelEdit,
    handleUpdate,
    handleDeactivate,
    handleReactivate,
  }
}
