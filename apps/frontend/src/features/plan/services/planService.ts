import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type OnboardingPlanResponse = components['schemas']['OnboardingPlanResponse']
type OnboardingPlanCreate = components['schemas']['OnboardingPlanCreate']
type OnboardingPlanUpdate = components['schemas']['OnboardingPlanUpdate']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']
type OnboardingPlanTaskAdd = components['schemas']['OnboardingPlanTaskAdd']
type OnboardingPlanTaskUpdate = components['schemas']['OnboardingPlanTaskUpdate']

export async function createPlan(data: OnboardingPlanCreate): Promise<OnboardingPlanResponse> {
  const res = await apiClient.post(API.PLANS.CREATE, data)
  return res.data
}

export async function getPlan(id: string): Promise<OnboardingPlanResponse> {
  const res = await apiClient.get(API.PLANS.GET(id))
  return res.data
}

export async function updatePlan(id: string, data: OnboardingPlanUpdate): Promise<OnboardingPlanResponse> {
  const res = await apiClient.patch(API.PLANS.UPDATE(id), data)
  return res.data
}

export async function addTask(planId: string, data: OnboardingPlanTaskAdd): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.post(API.PLANS.ADD_TASK(planId), data)
  return res.data
}

export async function updateTaskDeadline(planId: string, taskId: string, data: OnboardingPlanTaskUpdate): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.PLANS.UPDATE_TASK(planId, taskId), data)
  return res.data
}

export async function cancelTask(planId: string, taskId: string): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.PLANS.CANCEL_TASK(planId, taskId))
  return res.data
}

export async function getMyPlan(): Promise<OnboardingPlanResponse> {
  const res = await apiClient.get(API.PLANS.MY_PLAN)
  return res.data
}

export async function startTask(taskId: string): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.TASKS.START(taskId))
  return res.data
}

export async function completeTask(taskId: string): Promise<OnboardingPlanTaskResponse> {
  const res = await apiClient.patch(API.TASKS.COMPLETE(taskId))
  return res.data
}
