import apiClient from '@/lib/apiClient'
import { API } from '@/constants/apiEndpoints'
import type { components } from '@/types/api'

type TaskAttachmentResponse = components['schemas']['TaskAttachmentResponse']
type TaskCommentResponse = components['schemas']['TaskCommentResponse']

export async function uploadAttachment(taskId: string, file: File): Promise<TaskAttachmentResponse> {
  const form = new FormData()
  form.append('file', file)
  const res = await apiClient.post(API.TASKS.UPLOAD_ATTACHMENT(taskId), form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export async function deleteAttachment(taskId: string, attachmentId: string): Promise<void> {
  await apiClient.delete(API.TASKS.DELETE_ATTACHMENT(taskId, attachmentId))
}

export async function addComment(taskId: string, content: string): Promise<TaskCommentResponse> {
  const res = await apiClient.post(API.TASKS.ADD_COMMENT(taskId), { content })
  return res.data
}
