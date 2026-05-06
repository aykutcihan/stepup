export const API = {
  INVITATIONS: {
    VALIDATE: '/api/v1/invitations/validate',
    CREATE: '/api/v1/invitations',
    LIST: '/api/v1/invitations',
    RESEND: (id: string) => `/api/v1/invitations/${id}/resend`,
  },
  AUTH: {
    REGISTER: '/api/v1/auth/register',
  },
}
