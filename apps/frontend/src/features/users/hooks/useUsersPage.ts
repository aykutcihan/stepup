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
    const updated = await updateUser(userId, { department_id: departmentId || null })
    setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)))
  }

  async function handleChangeRole(userId: string, role: UserRole) {
    const updated = await updateUser(userId, { role })
    setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)))
  }

  async function handleDeactivate(userId: string) {
    await deactivateUser(userId)
    setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, is_active: false } : u)))
  }

  async function handleReactivate(userId: string) {
    const updated = await reactivateUser(userId)
    setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)))
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
