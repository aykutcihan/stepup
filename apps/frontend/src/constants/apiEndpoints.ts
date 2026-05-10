export const API = {
  INVITATIONS: {
    VALIDATE: '/api/v1/invitations/validate',
    CREATE: '/api/v1/invitations',
    LIST: '/api/v1/invitations',
    RESEND: (id: string) => `/api/v1/invitations/${id}/resend`,
  },
  AUTH: {
    REGISTER: '/api/v1/auth/register',
    LOGIN: '/api/v1/auth/login',
    ME: '/api/v1/auth/me',
    REFRESH: '/api/v1/auth/refresh',
    LOGOUT: '/api/v1/auth/logout',
  },
  USERS: {
    LIST: '/api/v1/users/',
    DEACTIVATE: (id: string) => `/api/v1/users/${id}/deactivate`,
  },
  DEPARTMENTS: {
    LIST: '/api/v1/departments/',
    CREATE: '/api/v1/departments/',
    UPDATE: (id: string) => `/api/v1/departments/${id}`,
    DEACTIVATE: (id: string) => `/api/v1/departments/${id}/deactivate`,
    REACTIVATE: (id: string) => `/api/v1/departments/${id}/reactivate`,
},

}
