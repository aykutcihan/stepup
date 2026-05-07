import axios from 'axios'
import { API } from '@/constants/apiEndpoints'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        await apiClient.post(API.AUTH.REFRESH)
        return apiClient(original)
      } catch {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
