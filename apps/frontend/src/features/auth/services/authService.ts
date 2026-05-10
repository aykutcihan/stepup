import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type RegisterRequest = components['schemas']['RegisterRequest']
type UserResponse = components['schemas']['UserResponse']
type LoginRequest = components['schemas']['LoginRequest']

export async function register(data: RegisterRequest): Promise<UserResponse> {
  const res = await apiClient.post(API.AUTH.REGISTER, data)
  return res.data
}

export async function login(data: LoginRequest): Promise<UserResponse> {
  const res = await apiClient.post(API.AUTH.LOGIN, data)
  return res.data
}

export async function getMe(): Promise<UserResponse> {
  const res = await apiClient.get(API.USERS.ME)
  return res.data
}

export async function logout(): Promise<void> {
  await apiClient.post(API.AUTH.LOGOUT)
}
