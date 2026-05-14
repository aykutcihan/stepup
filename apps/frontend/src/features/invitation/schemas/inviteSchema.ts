import { z } from 'zod'
import { USER_ROLE_VALUES } from '@/constants/userRoles'

export const inviteSchema = z.object({
  email: z.string().email('Invalid email address'),
  role: z.enum(USER_ROLE_VALUES),
  department_id: z.string().optional(),
})

export type InviteFormData = z.infer<typeof inviteSchema>
