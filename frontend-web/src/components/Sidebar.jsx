import { NavLink } from 'react-router-dom'
import { LayoutDashboard, MessageSquareText, FileBarChart2, Camera, User } from 'lucide-react'

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">SAAS ROTINA</div>
      
      <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <LayoutDashboard size={20} />
        <span>Visão Geral</span>
      </NavLink>
      
      <NavLink to="/chat" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <MessageSquareText size={20} />
        <span>Assistente IA</span>
      </NavLink>
      
      <NavLink to="/workouts" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <FileBarChart2 size={20} />
        <span>Histórico de Treino</span>
      </NavLink>
      
      <NavLink to="/physique" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
        <Camera size={20} />
        <span>Análise Física</span>
      </NavLink>

      <div style={{ marginTop: 'auto' }}>
        <NavLink to="/settings" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <User size={20} />
          <span>Meu Perfil</span>
        </NavLink>
      </div>
    </aside>
  )
}
