import axios from 'axios'
import { API } from '@/constants/apiEndpoints'
import { ROUTES } from '@/constants/routes'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  withCredentials: true,
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    const isAuthEndpoint = original.url === API.USERS.ME || original.url === API.AUTH.REFRESH
    const errorCode = error.response?.data?.error_code

    if (errorCode === 'USER_DEACTIVATED') {
      window.location.href = `${ROUTES.LOGIN}?error=USER_DEACTIVATED`
      return Promise.reject(error)
    }

    if (error.response?.status === 401 && !original._retry && !isAuthEndpoint) {
      original._retry = true
      try {
        await apiClient.post(API.AUTH.REFRESH)
        return apiClient(original)
      } catch {
        window.location.href = ROUTES.LOGIN
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
