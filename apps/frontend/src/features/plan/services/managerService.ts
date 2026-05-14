import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type ApprovalTaskResponse = components['schemas']['ApprovalTaskResponse']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']

export async function getPendingApprovals(): Promise<ApprovalTaskResponse[]> {
  const res = await apiClient.get(API.MANAGER.APPROVALS)
  return res.data
}

export async function approveTask(taskId: string): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.TASKS.APPROVE(taskId))
  return res.data
}

export async function returnTask(taskId: string, content: string): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.TASKS.RETURN(taskId), { content })
  return res.data
}
