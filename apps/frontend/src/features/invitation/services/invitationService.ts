import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type InvitationCreate = components['schemas']['InvitationCreate']
type InvitationResponse = components['schemas']['InvitationResponse']

export async function createInvitation(data: InvitationCreate): Promise<InvitationResponse> {
  const res = await apiClient.post(API.INVITATIONS.CREATE, data)
  return res.data
}

export async function getInvitations(): Promise<InvitationResponse[]> {
  const res = await apiClient.get(API.INVITATIONS.LIST)
  return res.data
}

export async function resendInvitation(id: string): Promise<InvitationResponse> {
  const res = await apiClient.post(API.INVITATIONS.RESEND(id))
  return res.data
}
