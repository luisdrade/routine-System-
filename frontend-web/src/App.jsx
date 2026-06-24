import { Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Physique from './pages/Physique'
import Sidebar from './components/Sidebar'

function App() {
  return (
    <>
      <Sidebar />
      <main className="main-area">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/physique" element={<Physique />} />
          <Route path="/workouts" element={<div className="page-content"><h1 className="title">HISTÓRICO</h1><p className="subtitle">Em breve...</p></div>} />
          <Route path="/settings" element={<div className="page-content"><h1 className="title">PERFIL</h1><p className="subtitle">Em breve...</p></div>} />
        </Routes>
      </main>
    </>
  )
}

export default App
