/**
 * NavigationBar - Organismo para la barra de navegación principal
 * Incluye logo, navegación y perfil de usuario (si está autenticado)
 */
import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import Button from '../atoms/Button'
import UserProfileDropdown from '../molecules/UserProfileDropdown'

function NavigationBar() {
  const { isAuthenticated, isLoading } = useAuth()

  const navigationLinks = [
    { label: 'Inicio', href: '/' },
    { label: 'Empresas', href: '/empresas', protected: false }, // Público para todos
    { label: 'Inventario', href: '/inventario', protected: true },
    { label: 'IA Beta', href: '/ia-beta', protected: true },
  ]

  // Filtrar links según autenticación
  const visibleLinks = navigationLinks.filter(
    link => !link.protected || isAuthenticated
  )

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 relative flex items-center justify-center rounded-xl bg-gradient-to-br from-brand-primary via-brand-secondary to-brand-accent p-[2px]">
              <div className="flex h-full w-full items-center justify-center rounded-xl bg-slate-950">
                <span className="text-lg font-bold font-display bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
                  IP
                </span>
              </div>
            </div>
            <span className="font-display font-bold text-lg text-white group-hover:text-brand-primary transition-colors">
              Inventario Pro
            </span>
          </Link>

          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex items-center gap-1">
            {visibleLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="px-4 py-2 rounded-lg text-sm font-medium text-white/80 hover:text-white hover:bg-white/5 transition-all duration-200"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right Side - Auth Actions */}
          <div className="flex items-center gap-3">
            {isLoading ? (
              <div className="w-8 h-8 rounded-full bg-white/10 animate-pulse" />
            ) : isAuthenticated ? (
              <>
                {/* Status Indicator */}
                <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 ring-1 ring-green-500/20">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-xs font-medium text-green-400">
                    Sesión activa
                  </span>
                </div>
                
                {/* User Profile Dropdown */}
                <UserProfileDropdown />
              </>
            ) : (
              <Link to="/login">
                <Button variant="primary" size="sm">
                  Iniciar Sesión
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Navigation - Slide from bottom when needed */}
      {isAuthenticated && (
        <div className="md:hidden border-t border-white/10 bg-slate-950/95 backdrop-blur-xl">
          <div className="px-4 py-2 flex gap-2 overflow-x-auto">
            {visibleLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="px-3 py-1.5 rounded-lg text-sm font-medium text-white/80 hover:text-white hover:bg-white/5 transition-all duration-200 whitespace-nowrap"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  )
}

export default NavigationBar
