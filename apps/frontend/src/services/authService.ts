import axios from 'axios'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type InvitationValidateResponse = components['schemas']['InvitationValidateResponse']
type RegisterRequest = components['schemas']['RegisterRequest']
type UserResponse = components['schemas']['UserResponse']

export async function validateInvitation(token: string): Promise<InvitationValidateResponse> {
  const res = await axios.get(API.INVITATIONS.VALIDATE, { params: { token } })
  return res.data
}

export async function register(data: RegisterRequest): Promise<UserResponse> {
  const res = await axios.post(API.AUTH.REGISTER, data)
  return res.data
}
