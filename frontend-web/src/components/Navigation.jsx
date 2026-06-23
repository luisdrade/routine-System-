import { NavLink } from 'react-router-dom'
import { Dumbbell, LayoutDashboard, MessageSquareText, Camera } from 'lucide-react'

export default function Navigation() {
  return (
    <nav className="bottom-nav">
      <NavLink to="/" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <Dumbbell size={24} />
        <span>Treino</span>
      </NavLink>
      <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <LayoutDashboard size={24} />
        <span>Visão</span>
      </NavLink>
      <NavLink to="/chat" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <MessageSquareText size={24} />
        <span>IA</span>
      </NavLink>
      <NavLink to="/physique" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <Camera size={24} />
        <span>Físico</span>
      </NavLink>
    </nav>
  )
}
