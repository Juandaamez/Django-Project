/**
 * WelcomeBanner - Molécula para mostrar un banner de bienvenida animado
 * Se muestra solo cuando el usuario inicia sesión por primera vez
 */
import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'

function WelcomeBanner() {
  const { user, isAuthenticated } = useAuth()
  const [isVisible, setIsVisible] = useState(false)
  const [shouldRender, setShouldRender] = useState(false)

  useEffect(() => {
    // Mostrar banner solo si está autenticado y no se ha mostrado antes en esta sesión
    const bannerShown = sessionStorage.getItem('welcomeBannerShown')
    
    if (isAuthenticated && !bannerShown) {
      setShouldRender(true)
      // Pequeño delay para la animación
      setTimeout(() => setIsVisible(true), 300)
      
      // Auto-ocultar después de 5 segundos
      const timer = setTimeout(() => {
        handleClose()
      }, 5000)

      return () => clearTimeout(timer)
    }
  }, [isAuthenticated])

  const handleClose = () => {
    setIsVisible(false)
    sessionStorage.setItem('welcomeBannerShown', 'true')
    setTimeout(() => setShouldRender(false), 300)
  }

  if (!shouldRender || !user) return null

  const displayName = user.first_name || user.username || 'Usuario'
  const isAdmin = user.is_staff || user.role === 'admin'

  return (
    <div
      className={`
        fixed top-20 right-4 z-40 max-w-md
        transition-all duration-300 ease-out
        ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
      `}
    >
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-brand-primary/90 to-brand-secondary/90 backdrop-blur-xl shadow-2xl shadow-brand-primary/20 ring-1 ring-white/10">
        {/* Animated background effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-shimmer" />
        
        <div className="relative px-5 py-4">
          {/* Header */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-2xl">👋</span>
              <div>
                <h3 className="font-display font-bold text-white">
                  ¡Bienvenido, {displayName}!
                </h3>
                {isAdmin && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-white/20 text-xs font-semibold text-white mt-1">
                    🛡️ Administrador
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={handleClose}
              className="text-white/80 hover:text-white transition-colors"
              aria-label="Cerrar"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <p className="text-sm text-white/90 mb-3">
            Tu sesión está activa. Explora todas las funcionalidades de la plataforma.
          </p>

          {/* Quick Stats */}
          <div className="flex gap-2">
            <div className="flex-1 px-3 py-2 rounded-lg bg-white/10 backdrop-blur-sm">
              <div className="text-xs text-white/70">Estado</div>
              <div className="flex items-center gap-1 text-sm font-semibold text-white">
                <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                Online
              </div>
            </div>
            <div className="flex-1 px-3 py-2 rounded-lg bg-white/10 backdrop-blur-sm">
              <div className="text-xs text-white/70">Acceso</div>
              <div className="text-sm font-semibold text-white">
                {isAdmin ? 'Total' : 'Usuario'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WelcomeBanner
