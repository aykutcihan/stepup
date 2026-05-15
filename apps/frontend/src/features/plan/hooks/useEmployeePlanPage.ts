import { useEffect, useState } from 'react'
import { getMyPlan, startTask, completeTask } from '@/features/plan/services/planService'
import { uploadAttachment, deleteAttachment, addComment } from '@/features/plan/services/attachmentService'
import type { components } from '@/types/api'

type OnboardingPlanResponse = components['schemas']['OnboardingPlanResponse']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']
type TaskAttachmentResponse = components['schemas']['TaskAttachmentResponse']

export function useEmployeePlanPage() {
  const [plan, setPlan] = useState<OnboardingPlanResponse | null>(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    getMyPlan()
      .then(setPlan)
      .catch(() => setNotFound(true))
  }, [])

  function updateTask(updated: OnboardingPlanTaskResponse) {
    setPlan((prev) =>
      prev
        ? { ...prev, tasks: prev.tasks.map((t) => (t.id === updated.id ? { ...t, ...updated } : t)) }
        : prev
    )
  }

  async function handleStartTask(taskId: string) {
    const updated = await startTask(taskId)
    updateTask(updated)
  }

  async function handleCompleteTask(taskId: string) {
    const updated = await completeTask(taskId)
    updateTask(updated)
  }

  async function handleUpload(taskId: string, file: File) {
    const att = await uploadAttachment(taskId, file)
    setPlan((prev) =>
      prev
        ? { ...prev, tasks: prev.tasks.map((t) => t.id === taskId ? { ...t, attachments: [...t.attachments, att] } : t) }
        : prev
    )
  }

  async function handleDeleteAttachment(taskId: string, attachmentId: string) {
    await deleteAttachment(taskId, attachmentId)
    setPlan((prev) =>
      prev
        ? { ...prev, tasks: prev.tasks.map((t) => t.id === taskId ? { ...t, attachments: t.attachments.filter((a: TaskAttachmentResponse) => a.id !== attachmentId) } : t) }
        : prev
    )
  }

  async function handleAddComment(taskId: string, content: string) {
    const comment = await addComment(taskId, content)
    setPlan((prev) =>
      prev
        ? { ...prev, tasks: prev.tasks.map((t) => t.id === taskId ? { ...t, comments: [...t.comments, comment] } : t) }
        : prev
    )
  }

  const completedCount = plan?.tasks.filter((t) => t.status === 'completed' || t.status === 'approved').length ?? 0
  const totalCount = plan?.tasks.filter((t) => t.status !== 'cancelled').length ?? 0

  return {
    plan,
    notFound,
    completedCount,
    totalCount,
    handleStartTask,
    handleCompleteTask,
    handleUpload,
    handleDeleteAttachment,
    handleAddComment,
  }
}
