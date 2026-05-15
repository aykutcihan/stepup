import { useEffect, useState } from 'react'
import { getUsers, updateUser, deactivateUser, reactivateUser } from '@/features/users/services/userService'
import { getDepartments } from '@/features/department/services/departmentService'
import type { components } from '@/types/api'

type UserResponse = components['schemas']['UserResponse']
type DepartmentResponse = components['schemas']['DepartmentResponse']
type UserRole = components['schemas']['UserRole']

export function useUsersPage() {
  const [users, setUsers] = useState<UserResponse[]>([])
  const [departments, setDepartments] = useState<DepartmentResponse[]>([])
  const [filterRole, setFilterRole] = useState<UserRole | ''>('')
  const [filterDepartmentId, setFilterDepartmentId] = useState<string>('')
  const [filterStatus, setFilterStatus] = useState<'active' | 'inactive' | ''>('')

  useEffect(() => {
    getUsers().then(setUsers).catch(() => {})
    getDepartments().then(setDepartments).catch(() => {})
  }, [])

  const filteredUsers = users.filter((u) => {
    if (filterRole && u.role !== filterRole) return false
    if (filterDepartmentId && u.department_id !== filterDepartmentId) return false
    if (filterStatus === 'active' && !u.is_active) return false
    if (filterStatus === 'inactive' && u.is_active) return false
    return true
  })

  const activeDepartments = departments.filter((d) => d.is_active)

  function getDepartmentName(departmentId: string | null): string {
    if (!departmentId) return '—'
    return departments.find((d) => d.id === departmentId)?.name ?? '—'
  }

  async function handleAssignDepartment(userId: string, departmentId: string) {
    const prev = users.find((u) => u.id === userId)?.department_id ?? null
    setUsers((all) => all.map((u) => (u.id === userId ? { ...u, department_id: departmentId || null } : u)))
    try {
      const updated = await updateUser(userId, { department_id: departmentId || null })
      setUsers((all) => all.map((u) => (u.id === updated.id ? updated : u)))
    } catch {
      setUsers((all) => all.map((u) => (u.id === userId ? { ...u, department_id: prev } : u)))
    }
  }

  async function handleChangeRole(userId: string, role: UserRole) {
    const prev = users.find((u) => u.id === userId)?.role
    setUsers((all) => all.map((u) => (u.id === userId ? { ...u, role } : u)))
    try {
      const updated = await updateUser(userId, { role })
      setUsers((all) => all.map((u) => (u.id === updated.id ? updated : u)))
    } catch {
      if (prev) setUsers((all) => all.map((u) => (u.id === userId ? { ...u, role: prev } : u)))
    }
  }

  async function handleDeactivate(userId: string) {
    setUsers((all) => all.map((u) => (u.id === userId ? { ...u, is_active: false } : u)))
    try {
      await deactivateUser(userId)
    } catch {
      setUsers((all) => all.map((u) => (u.id === userId ? { ...u, is_active: true } : u)))
    }
  }

  async function handleReactivate(userId: string) {
    setUsers((all) => all.map((u) => (u.id === userId ? { ...u, is_active: true } : u)))
    try {
      const updated = await reactivateUser(userId)
      setUsers((all) => all.map((u) => (u.id === updated.id ? updated : u)))
    } catch {
      setUsers((all) => all.map((u) => (u.id === userId ? { ...u, is_active: false } : u)))
    }
  }

  return {
    filteredUsers,
    departments,
    activeDepartments,
    filterRole,
    setFilterRole,
    filterDepartmentId,
    setFilterDepartmentId,
    filterStatus,
    setFilterStatus,
    getDepartmentName,
    handleAssignDepartment,
    handleChangeRole,
    handleDeactivate,
    handleReactivate,
  }
}
