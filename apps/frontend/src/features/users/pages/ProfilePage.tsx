import { Camera, Loader } from 'lucide-react'
import { useProfilePage } from '@/features/users/hooks/useProfilePage'
import { ROLE_LABELS } from '@/constants/userRoles'

export default function ProfilePage() {
  const {
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
  } = useProfilePage()

  const avatarSrc = user?.avatar_url ?? null
  const initials = `${user?.first_name?.[0] ?? ''}${user?.last_name?.[0] ?? ''}`

  return (
    <div className="max-w-xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">My Profile</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">View and update your personal details.</p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm px-8 py-8 space-y-5">
        {success && (
          <div className="text-sm text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg px-4 py-3">
            Profile updated successfully.
          </div>
        )}
        {pageError && (
          <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-3">
            {pageError}
          </div>
        )}

        {/* Avatar */}
        <div className="flex justify-center pb-2">
          <div className="relative group">
            <div className="w-24 h-24 rounded-full overflow-hidden bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center">
              {avatarSrc ? (
                <img src={avatarSrc} alt="Profile photo" className="w-full h-full object-cover" />
              ) : (
                <span className="text-blue-700 dark:text-blue-400 text-2xl font-bold">{initials}</span>
              )}
            </div>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={avatarUploading}
              className="absolute inset-0 rounded-full flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity disabled:cursor-not-allowed"
              aria-label="Upload photo"
            >
              {avatarUploading ? (
                <Loader size={20} className="text-white animate-spin" />
              ) : (
                <Camera size={20} className="text-white" />
              )}
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              className="hidden"
              onChange={handleAvatarChange}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">First name</label>
            <input
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Last name</label>
            <input
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Email</label>
          <input
            value={user?.email ?? ''}
            readOnly
            className="w-full border border-gray-200 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-sm text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50 cursor-not-allowed"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Role</label>
          <input
            value={ROLE_LABELS[user?.role ?? ''] ?? user?.role ?? ''}
            readOnly
            className="w-full border border-gray-200 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-sm text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50 cursor-not-allowed"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Department</label>
          <input
            value={user?.department_name ?? '—'}
            readOnly
            className="w-full border border-gray-200 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-sm text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/50 cursor-not-allowed"
          />
        </div>

        <div className="pt-2">
          <button
            onClick={handleSave}
            className="bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium px-5 py-2.5 rounded-lg transition-colors"
          >
            Save changes
          </button>
        </div>
      </div>
    </div>
  )
}
