/**
 * LoginPage - Página de inicio de sesión
 * Integra el template de autenticación con el formulario de login
 */
import { useCallback, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import AuthTemplate from '../components/templates/AuthTemplate'
import LoginForm from '../components/organisms/LoginForm'
import LoginHero from '../components/organisms/LoginHero'
import Logo from '../components/atoms/Logo'

const LoginPage = () => {
  const navigate = useNavigate()
  const { login, isLoading, error, clearError, isAuthenticated } = useAuth()

  // Redirigir si ya está autenticado
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/empresas', { replace: true })
    }
  }, [isAuthenticated, navigate])

  const handleLogin = useCallback(
    async ({ email, password, rememberMe }) => {
      const result = await login(email, password)
      
      if (result.success) {
        // Si rememberMe está activo, el token ya está en localStorage
        // Si no, podríamos usar sessionStorage (simplificado aquí)
        navigate('/empresas', { replace: true })
      }
    },
    [login, navigate]
  )

  return (
    <AuthTemplate heroContent={<LoginHero className="w-1/2 xl:w-3/5" />}>
      {/* Header móvil */}
      <div className="lg:hidden mb-10 text-center">
        <div className="flex justify-center mb-6">
          <Logo size="lg" />
        </div>
        <h1 className="text-2xl font-display font-bold text-white">
          Bienvenido de vuelta
        </h1>
        <p className="mt-2 text-white/60">
          Ingresa tus credenciales para continuar
        </p>
      </div>

      {/* Header desktop */}
      <div className="hidden lg:block mb-10">
        <h1 className="text-3xl font-display font-bold text-white">
          Iniciar Sesión
        </h1>
        <p className="mt-2 text-white/60">
          Ingresa tus credenciales para acceder al panel
        </p>
      </div>

      {/* Formulario de login */}
      <LoginForm
        onSubmit={handleLogin}
        isLoading={isLoading}
        error={error}
        onClearError={clearError}
      />

      {/* Decoración adicional */}
      <div className="mt-8 p-4 rounded-xl bg-gradient-to-r from-brand-primary/10 via-brand-secondary/10 to-brand-accent/10 border border-white/5">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-brand-secondary/20 flex items-center justify-center">
            <svg
              className="w-5 h-5 text-brand-secondary"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              <path d="M9 12l2 2 4-4" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-white">
              Conexión segura
            </p>
            <p className="text-xs text-white/50 mt-0.5">
              Tus datos están protegidos con encriptación de extremo a extremo
              y autenticación JWT.
            </p>
          </div>
        </div>
      </div>
    </AuthTemplate>
  )
}

export default LoginPage
