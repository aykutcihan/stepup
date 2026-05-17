import { ERROR_MESSAGES } from '@/constants/errorMessages'

export function getErrorMessage(err: unknown): string {
  const data = (err as { response?: { data?: { error_code?: string; message?: string } } }).response?.data
  if (data?.error_code && ERROR_MESSAGES[data.error_code]) {
    return ERROR_MESSAGES[data.error_code]
  }
  if (data?.message) {
    return data.message
  }
  return 'Something went wrong. Please try again.'
}
