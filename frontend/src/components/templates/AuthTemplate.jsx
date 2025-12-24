/**
 * AuthTemplate - Template para páginas de autenticación
 * Layout split-screen con hero decorativo y formulario
 */
import GlowOrb from '../atoms/GlowOrb'

const AuthTemplate = ({
  heroContent,
  children,
  className = '',
}) => {
  return (
    <div
      className={`
        min-h-screen flex
        bg-slate-950
        ${className}
      `}
    >
      {/* Hero Section (left side on desktop) */}
      {heroContent}

      {/* Form Section (right side on desktop) */}
      <div className="relative flex-1 flex flex-col justify-center px-6 py-12 lg:px-12 xl:px-20">
        {/* Mobile background orbs */}
        <div className="lg:hidden">
          <GlowOrb
            color="primary"
            size="md"
            position={{ top: '5%', right: '-20%' }}
            opacity={20}
          />
          <GlowOrb
            color="secondary"
            size="sm"
            position={{ bottom: '10%', left: '-10%' }}
            opacity={15}
          />
        </div>

        {/* Content */}
        <div className="relative z-10 w-full max-w-md mx-auto">
          {children}
        </div>

        {/* Footer */}
        <div className="relative z-10 mt-12 text-center">
          <p className="text-xs text-white/30">
            © 2025 LiteThinking. Todos los derechos reservados.
          </p>
          <div className="mt-2 flex items-center justify-center gap-4 text-xs text-white/30">
            <a href="/privacy" className="hover:text-white/50 transition-colors">
              Privacidad
            </a>
            <span>•</span>
            <a href="/terms" className="hover:text-white/50 transition-colors">
              Términos
            </a>
            <span>•</span>
            <a href="/support" className="hover:text-white/50 transition-colors">
              Soporte
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuthTemplate
