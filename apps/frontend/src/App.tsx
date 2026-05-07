import { Routes, Route } from 'react-router-dom'
import RegisterPage from '@/pages/RegisterPage'
import InviteUserPage from '@/pages/hr/InviteUserPage'
import LoginPage from '@/pages/LoginPage'
import HRDashboard from '@/pages/hr/HRDashboard'
import ManagerDashboard from '@/pages/manager/ManagerDashboard'
import EmployeeDashboard from '@/pages/employee/EmployeeDashboard'



export default function App() {
  return (
    <Routes>
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/hr/invite-user" element={<InviteUserPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/hr/dashboard" element={<HRDashboard />} />
      <Route path="/manager/dashboard" element={<ManagerDashboard />} />
      <Route path="/employee/dashboard" element={<EmployeeDashboard />} />


    </Routes>
  )
}
                                            