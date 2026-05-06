import { ERROR_MESSAGES } from '@/constants/errorMessages'

export function getErrorMessage(err: unknown): string {
  const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
  return ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong. Please try again.'
}
