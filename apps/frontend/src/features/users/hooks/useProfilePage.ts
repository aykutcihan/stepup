import { useState } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { updateMe } from '@/features/users/services/userService'

export function useProfilePage() {
  const user = useAuthStore((state) => state.user)
  const setUser = useAuthStore((state) => state.setUser)
  const [firstName, setFirstName] = useState(user?.first_name ?? '')
  const [lastName, setLastName] = useState(user?.last_name ?? '')
  const [success, setSuccess] = useState(false)
  const [pageError, setPageError] = useState('')

  async function handleSave() {
    try {
      const updated = await updateMe({ first_name: firstName, last_name: lastName })
      setUser(updated)
      setSuccess(true)
      setPageError('')
    } catch {
      setPageError('Something went wrong. Please try again.')
      setSuccess(false)
    }
  }

  return {
    user,
    firstName,
    setFirstName,
    lastName,
    setLastName,
    success,
    pageError,
    handleSave,
  }
}
