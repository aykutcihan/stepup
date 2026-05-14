import { useEffect, useState } from 'react'
import { getMyPlan, startTask, completeTask } from '@/features/plan/services/planService'
import type { components } from '@/types/api'

type OnboardingPlanResponse = components['schemas']['OnboardingPlanResponse']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']

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
      prev ? { ...prev, tasks: prev.tasks.map((t) => (t.id === updated.id ? updated : t)) } : prev
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

  const completedCount = plan?.tasks.filter((t) => t.status === 'completed' || t.status === 'approved').length ?? 0
  const totalCount = plan?.tasks.length ?? 0

  return {
    plan,
    notFound,
    completedCount,
    totalCount,
    handleStartTask,
    handleCompleteTask,
  }
}
