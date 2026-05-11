import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  getTemplates,
  getTasks,
  addTask,
  updateTask,
  deleteTask,
  reorderTask,
  activateTemplate,
  deactivateTemplate,
} from '@/features/template/services/templateService'
import type { components } from '@/types/api'

type TemplateResponse = components['schemas']['TemplateResponse']
type TaskResponse = components['schemas']['TaskResponse']

export function useTemplateDetailPage() {
  const { id } = useParams<{ id: string }>()

  const [template, setTemplate] = useState<TemplateResponse | null>(null)
  const [tasks, setTasks] = useState<TaskResponse[]>([])

  const [showAddForm, setShowAddForm] = useState(false)
  const [newTitle, setNewTitle] = useState('')
  const [newDescription, setNewDescription] = useState('')
  const [newDeadlineDays, setNewDeadlineDays] = useState(1)
  const [newIsRequired, setNewIsRequired] = useState(true)

  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')
  const [editDeadlineDays, setEditDeadlineDays] = useState(1)
  const [editIsRequired, setEditIsRequired] = useState(true)

  useEffect(() => {
    if (!id) return
    getTemplates().then((list) => {
      const found = list.find((t) => t.id === id)
      if (found) setTemplate(found)
    }).catch(() => {})
    getTasks(id).then(setTasks).catch(() => {})
  }, [id])

  function startEdit(task: TaskResponse) {
    setEditingTaskId(task.id)
    setEditTitle(task.title)
    setEditDescription(task.description ?? '')
    setEditDeadlineDays(task.deadline_days)
    setEditIsRequired(task.is_required)
  }

  function cancelEdit() {
    setEditingTaskId(null)
  }

  async function handleAddTask() {
    if (!id || !newTitle.trim()) return
    const created = await addTask(id, {
      title: newTitle.trim(),
      description: newDescription.trim() || undefined,
      deadline_days: newDeadlineDays,
      is_required: newIsRequired,
    })
    setTasks((prev) => [...prev, created])
    setShowAddForm(false)
    setNewTitle('')
    setNewDescription('')
    setNewDeadlineDays(1)
    setNewIsRequired(true)
  }

  async function handleUpdateTask() {
    if (!id || !editingTaskId) return
    const updated = await updateTask(id, editingTaskId, {
      title: editTitle.trim(),
      description: editDescription.trim() || undefined,
      deadline_days: editDeadlineDays,
      is_required: editIsRequired,
    })
    setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    setEditingTaskId(null)
  }

  async function handleDeleteTask(taskId: string) {
    if (!id) return
    await deleteTask(id, taskId)
    setTasks((prev) => prev.filter((t) => t.id !== taskId))
  }

  async function handleReorder(taskId: string, newOrder: number) {
    if (!id) return
    const updated = await reorderTask(id, taskId, newOrder)
    setTasks((prev) =>
      prev.map((t) => {
        if (t.id === updated.id) return updated
        if (newOrder <= t.order && t.order < prev.find((x) => x.id === taskId)!.order) return { ...t, order: t.order + 1 }
        if (newOrder >= t.order && t.order > prev.find((x) => x.id === taskId)!.order) return { ...t, order: t.order - 1 }
        return t
      }).sort((a, b) => a.order - b.order)
    )
  }

  async function handleActivate() {
    if (!id) return
    const updated = await activateTemplate(id)
    setTemplate(updated)
  }

  async function handleDeactivate() {
    if (!id) return
    const updated = await deactivateTemplate(id)
    setTemplate(updated)
  }

  return {
    template,
    tasks: [...tasks].sort((a, b) => a.order - b.order),
    showAddForm,
    setShowAddForm,
    newTitle,
    setNewTitle,
    newDescription,
    setNewDescription,
    newDeadlineDays,
    setNewDeadlineDays,
    newIsRequired,
    setNewIsRequired,
    editingTaskId,
    editTitle,
    setEditTitle,
    editDescription,
    setEditDescription,
    editDeadlineDays,
    setEditDeadlineDays,
    editIsRequired,
    setEditIsRequired,
    startEdit,
    cancelEdit,
    handleAddTask,
    handleUpdateTask,
    handleDeleteTask,
    handleReorder,
    handleActivate,
    handleDeactivate,
  }
}
