import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUsers } from '@/features/users/services/userService'
import { getTemplates } from '@/features/template/services/templateService'
import { createPlan } from '@/features/plan/services/planService'
import { ROUTES } from '@/constants/routes'
import { getErrorMessage } from '@/utils/getErrorMessage'
import type { components } from '@/types/api'

type UserResponse = components['schemas']['UserResponse']
type TemplateResponse = components['schemas']['TemplateResponse']

export function useCreatePlanPage() {
  const navigate = useNavigate()

  const [users, setUsers] = useState<UserResponse[]>([])
  const [templates, setTemplates] = useState<TemplateResponse[]>([])
  const [userId, setUserId] = useState('')
  const [templateId, setTemplateId] = useState('')
  const [managerId, setManagerId] = useState('')
  const [startDate, setStartDate] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    getUsers().then(setUsers).catch(() => {})
    getTemplates({ is_active: true }).then(setTemplates).catch(() => {})
  }, [])

  const employees = users.filter((u) => u.role === 'employee' && u.is_active)
  const managers = users.filter((u) => u.role === 'manager' && u.is_active)

  async function handleSubmit() {
    if (!userId || !templateId || !managerId || !startDate) return
    setSubmitting(true)
    setError('')
    try {
      const plan = await createPlan({ user_id: userId, template_id: templateId, manager_id: managerId, start_date: startDate })
      navigate(ROUTES.HR_PLAN_DETAIL(plan.id))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setSubmitting(false)
    }
  }

  return {
    employees, managers, templates,
    userId, setUserId,
    templateId, setTemplateId,
    managerId, setManagerId,
    startDate, setStartDate,
    error, submitting,
    handleSubmit,
  }
}
