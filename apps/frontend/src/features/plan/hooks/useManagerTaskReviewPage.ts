import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getPendingApprovals, approveTask, returnTask } from '@/features/plan/services/managerService'
import { ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type ApprovalTaskResponse = components['schemas']['ApprovalTaskResponse']

export function useManagerTaskReviewPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [task, setTask] = useState<ApprovalTaskResponse | null>(null)
  const [showReturnModal, setShowReturnModal] = useState(false)
  const [returnComment, setReturnComment] = useState('')

  useEffect(() => {
    if (!id) return
    getPendingApprovals()
      .then((tasks) => setTask(tasks.find((t) => t.id === id) ?? null))
      .catch(() => {})
  }, [id])

  async function handleApprove() {
    if (!id) return
    await approveTask(id)
    navigate(ROUTES.MANAGER_APPROVALS)
  }

  async function handleReturn() {
    if (!id || !returnComment.trim()) return
    await returnTask(id, returnComment)
    navigate(ROUTES.MANAGER_APPROVALS)
  }

  return {
    task,
    showReturnModal,
    setShowReturnModal,
    returnComment,
    setReturnComment,
    handleApprove,
    handleReturn,
  }
}
