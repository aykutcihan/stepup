import apiClient from '@/lib/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type TemplateResponse = components['schemas']['TemplateResponse']
type TemplateCreate = components['schemas']['TemplateCreate']
type TemplateUpdate = components['schemas']['TemplateUpdate']
type TaskResponse = components['schemas']['TaskResponse']
type TaskCreate = components['schemas']['TaskCreate']
type TaskUpdate = components['schemas']['TaskUpdate']

export async function getTemplates(params?: {
  department_id?: string
  is_active?: boolean
}): Promise<TemplateResponse[]> {
  const res = await apiClient.get(API.TEMPLATES.LIST, { params })
  return res.data
}

export async function createTemplate(data: TemplateCreate): Promise<TemplateResponse> {
  const res = await apiClient.post(API.TEMPLATES.CREATE, data)
  return res.data
}

export async function updateTemplate(id: string, data: TemplateUpdate): Promise<TemplateResponse> {
  const res = await apiClient.patch(API.TEMPLATES.UPDATE(id), data)
  return res.data
}

export async function activateTemplate(id: string): Promise<TemplateResponse> {
  const res = await apiClient.patch(API.TEMPLATES.ACTIVATE(id))
  return res.data
}

export async function deactivateTemplate(id: string): Promise<TemplateResponse> {
  const res = await apiClient.patch(API.TEMPLATES.DEACTIVATE(id))
  return res.data
}

export async function cloneTemplate(id: string): Promise<TemplateResponse> {
  const res = await apiClient.post(API.TEMPLATES.CLONE(id))
  return res.data
}

export async function getTasks(templateId: string): Promise<TaskResponse[]> {
  const res = await apiClient.get(API.TEMPLATES.GET_TASKS(templateId))
  return res.data
}

export async function addTask(templateId: string, data: TaskCreate): Promise<TaskResponse> {
  const res = await apiClient.post(API.TEMPLATES.ADD_TASK(templateId), data)
  return res.data
}

export async function updateTask(templateId: string, taskId: string, data: TaskUpdate): Promise<TaskResponse> {
  const res = await apiClient.patch(API.TEMPLATES.UPDATE_TASK(templateId, taskId), data)
  return res.data
}

export async function deleteTask(templateId: string, taskId: string): Promise<void> {
  await apiClient.delete(API.TEMPLATES.DELETE_TASK(templateId, taskId))
}

export async function reorderTask(templateId: string, taskId: string, newOrder: number): Promise<TaskResponse> {
  const res = await apiClient.patch(API.TEMPLATES.REORDER_TASK(templateId, taskId), { new_order: newOrder })
  return res.data
}
