import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getPlan, updatePlan, addTask, updateTaskDeadline, cancelTask } from '@/features/plan/services/planService'
import { getUsers } from '@/features/users/services/userService'
import type { components } from '@/types/api'

type OnboardingPlanResponse = components['schemas']['OnboardingPlanResponse']
type OnboardingPlanTaskResponse = components['schemas']['OnboardingPlanTaskResponse']
type UserResponse = components['schemas']['UserResponse']

export function usePlanDetailPage() {
  const { id } = useParams<{ id: string }>()

  const [plan, setPlan] = useState<OnboardingPlanResponse | null>(null)
  const [managers, setManagers] = useState<UserResponse[]>([])

  const [editingManagerId, setEditingManagerId] = useState<string | null>(null)
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [editingDeadline, setEditingDeadline] = useState('')
  const [cancelConfirmTaskId, setCancelConfirmTaskId] = useState<string | null>(null)

  const [showAddForm, setShowAddForm] = useState(false)
  const [newTitle, setNewTitle] = useState('')
  const [newDescription, setNewDescription] = useState('')
  const [newDeadline, setNewDeadline] = useState('')
  const [newIsRequired, setNewIsRequired] = useState(true)

  useEffect(() => {
    if (!id) return
    getPlan(id).then(setPlan).catch(() => {})
    getUsers().then((u) => setManagers(u.filter((m) => m.role === 'manager' && m.is_active))).catch(() => {})
  }, [id])

  async function handleChangeManager(managerId: string) {
    if (!id) return
    const updated = await updatePlan(id, { manager_id: managerId })
    setPlan(updated)
    setEditingManagerId(null)
  }

  function startEditDeadline(task: OnboardingPlanTaskResponse) {
    setEditingTaskId(task.id)
    setEditingDeadline(task.deadline)
  }

  async function handleUpdateDeadline() {
    if (!id || !editingTaskId || !editingDeadline) return
    const updated = await updateTaskDeadline(id, editingTaskId, { deadline: editingDeadline })
    setPlan((prev) => prev ? { ...prev, tasks: prev.tasks.map((t) => t.id === updated.id ? updated : t) } : prev)
    setEditingTaskId(null)
  }

  async function handleAddTask() {
    if (!id || !newTitle.trim() || !newDeadline) return
    const created = await addTask(id, {
      title: newTitle.trim(),
      description: newDescription.trim() || undefined,
      deadline: newDeadline,
      is_required: newIsRequired,
    })
    setPlan((prev) => prev ? { ...prev, tasks: [...prev.tasks, created] } : prev)
    setShowAddForm(false)
    setNewTitle('')
    setNewDescription('')
    setNewDeadline('')
    setNewIsRequired(true)
  }

  async function handleCancelTask(taskId: string) {
    if (!id) return
    const updated = await cancelTask(id, taskId)
    setPlan((prev) => prev ? { ...prev, tasks: prev.tasks.map((t) => t.id === updated.id ? updated : t) } : prev)
    setCancelConfirmTaskId(null)
  }

  function getManagerName(managerId: string): string {
    const m = managers.find((u) => u.id === managerId)
    return m ? `${m.first_name} ${m.last_name}` : '—'
  }

  return {
    plan, managers,
    editingManagerId, setEditingManagerId,
    editingTaskId, setEditingTaskId,
    editingDeadline, setEditingDeadline,
    cancelConfirmTaskId, setCancelConfirmTaskId,
    showAddForm, setShowAddForm,
    newTitle, setNewTitle,
    newDescription, setNewDescription,
    newDeadline, setNewDeadline,
    newIsRequired, setNewIsRequired,
    handleChangeManager,
    startEditDeadline,
    handleUpdateDeadline,
    handleAddTask,
    handleCancelTask,
    getManagerName,
  }
}
