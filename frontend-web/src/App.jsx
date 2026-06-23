import { Routes, Route } from 'react-router-dom'
import Workout from './pages/Workout'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Physique from './pages/Physique'
import Navigation from './components/Navigation'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Workout />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/physique" element={<Physique />} />
      </Routes>
      <Navigation />
    </>
  )
}

export default App
