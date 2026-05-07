import apiClient from '@/services/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type UserResponse = components['schemas']['UserResponse']

export async function getUsers(): Promise<UserResponse[]> {
  const res = await apiClient.get(API.USERS.LIST)
  return res.data
}

export async function deactivateUser(id: string): Promise<void> {
  await apiClient.patch(API.USERS.DEACTIVATE(id))
}
