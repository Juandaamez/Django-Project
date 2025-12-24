/**
 * UserProfileDropdown - Molécula para el menú de perfil de usuario
 * Dropdown con información del usuario y acciones (perfil, configuración, logout)
 */
import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import UserBadge from '../atoms/UserBadge'
import { useAuth } from '../../context/AuthContext'

function UserProfileDropdown() {
  const { user, logout } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)
  const navigate = useNavigate()

  // Cerrar dropdown al hacer click fuera
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLogout = () => {
    logout()
    setIsOpen(false)
    navigate('/')
  }

  if (!user) return null

  const displayName = user.first_name || user.username || user.email?.split('@')[0] || 'Usuario'
  const userEmail = user.email || 'Sin correo'
  const isAdmin = user.is_staff || user.role === 'admin'

  const menuItems = [
    {
      icon: '👤',
      label: 'Mi Perfil',
      action: () => {
        navigate('/perfil')
        setIsOpen(false)
      },
    },
    {
      icon: '⚙️',
      label: 'Configuración',
      action: () => {
        navigate('/configuracion')
        setIsOpen(false)
      },
    },
    ...(isAdmin ? [{
      icon: '🛡️',
      label: 'Panel Admin',
      action: () => {
        navigate('/admin')
        setIsOpen(false)
      },
      highlight: true,
    }] : []),
    {
      icon: '🚪',
      label: 'Cerrar Sesión',
      action: handleLogout,
      danger: true,
    },
  ]

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 px-3 py-2 rounded-full hover:bg-white/5 transition-all duration-200 group"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <UserBadge user={user} size="md" showStatus={true} />
        <div className="hidden md:flex flex-col items-start">
          <span className="text-sm font-medium text-white group-hover:text-brand-primary transition-colors">
            {displayName}
          </span>
          {isAdmin && (
            <span className="text-xs text-brand-primary font-semibold">
              Admin
            </span>
          )}
        </div>
        <svg
          className={`w-4 h-4 text-white/60 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className="absolute right-0 mt-2 w-64 rounded-2xl bg-slate-900/95 backdrop-blur-xl shadow-xl shadow-black/50 ring-1 ring-white/10 overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200"
        >
          {/* User Info Header */}
          <div className="px-4 py-3 border-b border-white/10 bg-gradient-to-br from-brand-primary/10 to-brand-secondary/10">
            <div className="flex items-center gap-3">
              <UserBadge user={user} size="lg" showStatus={false} />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-white truncate">
                  {displayName}
                </p>
                <p className="text-xs text-white/60 truncate">
                  {userEmail}
                </p>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-2">
            {menuItems.map((item, index) => (
              <button
                key={index}
                onClick={item.action}
                className={`
                  w-full px-4 py-2.5 flex items-center gap-3
                  transition-colors duration-150
                  ${item.danger 
                    ? 'hover:bg-red-500/10 text-red-400 hover:text-red-300' 
                    : item.highlight
                    ? 'hover:bg-brand-primary/10 text-brand-primary'
                    : 'hover:bg-white/5 text-white/90 hover:text-white'
                  }
                `}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="text-sm font-medium">{item.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default UserProfileDropdown
