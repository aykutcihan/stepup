import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPendingApprovals, approveTask } from '@/features/plan/services/managerService'
import { ROUTES } from '@/constants/routes'
import type { components } from '@/types/api'

type ApprovalTaskResponse = components['schemas']['ApprovalTaskResponse']

export function useManagerApprovalsPage() {
  const navigate = useNavigate()
  const [tasks, setTasks] = useState<ApprovalTaskResponse[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    getPendingApprovals()
      .then(setTasks)
      .catch(() => {})
      .finally(() => setIsLoading(false))
  }, [])

  async function handleApprove(taskId: string) {
    try {
      await approveTask(taskId)
      setTasks((prev) => prev.filter((t) => t.id !== taskId))
    } catch {
      // task stays in list on failure
    }
  }

  function handleReview(taskId: string) {
    navigate(ROUTES.MANAGER_TASK_REVIEW(taskId))
  }

  return { tasks, isLoading, handleApprove, handleReview }
}
