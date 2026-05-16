import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type DepartmentCreate = components['schemas']['DepartmentCreate']
type DepartmentUpdate = components['schemas']['DepartmentUpdate']
type DepartmentResponse = components['schemas']['DepartmentResponse']

export async function getDepartments(): Promise<DepartmentResponse[]> {
  const res = await apiClient.get(API.DEPARTMENTS.LIST)
  return res.data.items
}

export async function createDepartment(data: DepartmentCreate): Promise<DepartmentResponse> {
  const res = await apiClient.post(API.DEPARTMENTS.CREATE, data)
  return res.data
}

export async function updateDepartment(id: string, data: DepartmentUpdate): Promise<DepartmentResponse> {
  const res = await apiClient.patch(API.DEPARTMENTS.UPDATE(id), data)
  return res.data
}

export async function deactivateDepartment(id: string): Promise<DepartmentResponse> {
  const res = await apiClient.patch(API.DEPARTMENTS.DEACTIVATE(id))
  return res.data
}

export async function reactivateDepartment(id: string): Promise<DepartmentResponse> {
  const res = await apiClient.patch(API.DEPARTMENTS.REACTIVATE(id))
  return res.data
}
