import { useRef, useState } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { updateMe, uploadAvatar } from '@/features/users/services/userService'

export function useProfilePage() {
  const user = useAuthStore((state) => state.user)
  const setUser = useAuthStore((state) => state.setUser)
  const [firstName, setFirstName] = useState(user?.first_name ?? '')
  const [lastName, setLastName] = useState(user?.last_name ?? '')
  const [success, setSuccess] = useState(false)
  const [pageError, setPageError] = useState('')
  const [avatarUploading, setAvatarUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

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

  async function handleAvatarChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    setAvatarUploading(true)
    setPageError('')
    try {
      const updated = await uploadAvatar(file)
      setUser(updated)
    } catch {
      setPageError('Avatar upload failed. Please use a JPEG, PNG or WebP image under 5MB.')
    } finally {
      setAvatarUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
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
    avatarUploading,
    fileInputRef,
    handleAvatarChange,
  }
}
