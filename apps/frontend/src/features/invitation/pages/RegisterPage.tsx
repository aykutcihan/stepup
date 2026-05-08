import { useRegisterForm } from '@/features/invitation/hooks/useRegisterForm'

export default function RegisterPage() {
  const { registerField, handleSubmit, errors, onSubmit, email, pageError } = useRegisterForm()

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-blue-800 rounded-t-2xl px-8 py-6 text-white text-center">
          <h1 className="text-2xl font-bold tracking-tight">StepUp</h1>
          <p className="text-blue-200 text-sm mt-1">Complete your registration</p>
        </div>

        <div className="bg-white rounded-b-2xl shadow-lg px-8 py-8 border border-t-0 border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-1">Account details</h2>
          <p className="text-sm text-gray-500 mb-6">Fill in the fields below to set up your account.</p>

          {pageError && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-5">
              {pageError}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Email address
              </label>
              <input
                value={email}
                readOnly
                placeholder="Email"
                className="w-full border border-gray-200 rounded-lg px-3.5 py-2.5 text-sm text-gray-500 bg-gray-50 cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                First name
              </label>
              <input
                {...registerField('first_name')}
                placeholder="First name"
                className="w-full border border-gray-300 rounded-lg px-3.5 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
              {errors.first_name && (
                <p className="mt-1.5 text-xs text-red-600">{errors.first_name.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Last name
              </label>
              <input
                {...registerField('last_name')}
                placeholder="Last name"
                className="w-full border border-gray-300 rounded-lg px-3.5 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
              {errors.last_name && (
                <p className="mt-1.5 text-xs text-red-600">{errors.last_name.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Password
              </label>
              <input
                {...registerField('password')}
                type="password"
                placeholder="Password"
                className="w-full border border-gray-300 rounded-lg px-3.5 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
              {errors.password && (
                <p className="mt-1.5 text-xs text-red-600">{errors.password.message}</p>
              )}
            </div>

            <button
              type="submit"
              className="w-full bg-blue-700 hover:bg-blue-800 text-white font-medium py-2.5 rounded-lg transition-colors text-sm mt-2"
            >
              Create account
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
