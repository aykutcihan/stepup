import { Routes, Route } from 'react-router-dom'
import RegisterPage from '@/pages/RegisterPage'
import InviteUserPage from '@/pages/hr/InviteUserPage'
import LoginPage from '@/pages/LoginPage'


export default function App() {
  return (
    <Routes>
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/hr/invite-user" element={<InviteUserPage />} />
      <Route path="/login" element={<LoginPage />} />

    </Routes>
  )
}
                                            