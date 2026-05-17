import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import type { components } from '@/types/api'
import { createInvitation, getInvitations, resendInvitation } from '@/features/invitation/services/invitationService'
import { getDepartments } from '@/features/department/services/departmentService'
import { getErrorMessage } from '@/utils/getErrorMessage'
import { inviteSchema, type InviteFormData } from '@/features/invitation/schemas/inviteSchema'

type InvitationResponse = components['schemas']['InvitationResponse']
type DepartmentResponse = components['schemas']['DepartmentResponse']

export function useInviteUserForm() {
  const [formError, setFormError] = useState('')
  const [success, setSuccess] = useState(false)
  const [invitations, setInvitations] = useState<InvitationResponse[]>([])
  const [departments, setDepartments] = useState<DepartmentResponse[]>([])

  const { register, handleSubmit, reset, formState: { errors } } = useForm<InviteFormData>({
    resolver: zodResolver(inviteSchema),
  })

  useEffect(() => {
    getInvitations()
      .then((data) => setInvitations(data))
      .catch(() => {})
    getDepartments()
      .then((data) => setDepartments(data.filter((d) => d.is_active)))
      .catch(() => {})
  }, [])

  const handleResend = async (id: string) => {
    try {
      await resendInvitation(id)
      getInvitations().then((data) => setInvitations(data))
    } catch (err) {
      setFormError(getErrorMessage(err))
    }
  }

  const onSubmit = async (data: InviteFormData) => {
    try {
      setFormError('')
      setSuccess(false)
      await createInvitation(data)
      setSuccess(true)
      reset()
      getInvitations().then((data) => setInvitations(data))
    } catch (err) {
      setFormError(getErrorMessage(err))
    }
  }

  return { register, handleSubmit, errors, onSubmit, handleResend, invitations, departments, pageError: formError, success }
}
