import { useLoginForm } from '@/features/auth/hooks/useLoginForm'

export default function LoginPage() {
  const { register, handleSubmit, errors, onSubmit, pageError } = useLoginForm()

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-blue-800 rounded-t-2xl px-8 py-6 text-white text-center">
          <h1 className="text-2xl font-bold tracking-tight">StepUp</h1>
          <p className="text-blue-200 text-sm mt-1">Human Resources Platform</p>
        </div>

        <div className="bg-white rounded-b-2xl shadow-lg px-8 py-8 border border-t-0 border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-1">Welcome back</h2>
          <p className="text-sm text-gray-500 mb-6">Sign in to your account to continue.</p>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            {pageError && (
              <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
                {pageError}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Email address
              </label>
              <input
                type="email"
                {...register('email')}
                placeholder="Email"
                className="w-full border border-gray-300 rounded-lg px-3.5 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
              {errors.email && (
                <p className="mt-1.5 text-xs text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Password
              </label>
              <input
                type="password"
                {...register('password')}
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
              Sign in
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
