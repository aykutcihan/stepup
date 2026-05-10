import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type UserResponse = components['schemas']['UserResponse']
type UserUpdate = components['schemas']['UserUpdate']
type UserProfileUpdate = components['schemas']['UserProfileUpdate']

export async function updateMe(data: UserProfileUpdate): Promise<UserResponse> {
  const res = await apiClient.patch(API.USERS.UPDATE_ME, data)
  return res.data
}

export async function getUsers(): Promise<UserResponse[]> {
  const res = await apiClient.get(API.USERS.LIST)
  return res.data
}

export async function updateUser(id: string, data: UserUpdate): Promise<UserResponse> {
  const res = await apiClient.patch(API.USERS.UPDATE(id), data)
  return res.data
}

export async function deactivateUser(id: string): Promise<void> {
  await apiClient.patch(API.USERS.DEACTIVATE(id))
}
