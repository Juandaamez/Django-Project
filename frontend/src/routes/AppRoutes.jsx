import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

import LoginPage from '../pages/LoginPage'
import EmpresasPage from '../pages/EmpresasPage'
import InventarioPage from '../pages/InventarioPage'
import IABetaPage from '../pages/IABetaPage'
import LandingTemplate from '../components/templates/LandingTemplate'

const API_DOCS_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8001/api'}/docs/`

// Landing content (movido desde App.jsx)
const sections = [
  {
    tag: 'Demo',
    title: 'Recorrido listo para evaluar',
    description:
      'Ingresa con los usuarios demo, explora empresas reales de prueba y revisa inventario con estados críticos, bajos y saludables.',
    actions: [
      'Admin: admin.demo@example.com / DemoAdmin2026!',
      'Lectura: demo@example.com / DemoUser2026!',
      'El login también trae botones para rellenar estos datos',
    ],
  },
  {
    tag: 'Operación',
    title: 'Empresas, productos e inventario',
    description:
      'CRUD administrativo con permisos por rol, búsqueda por NIT/nombre y catálogo multi-moneda conectado al stock.',
    actions: [
      'Permisos admin / lectura',
      'Productos por empresa',
      'Inventario por producto',
    ],
  },
  {
    tag: 'Reportes',
    title: 'PDF, correo e historial',
    description:
      'Genera reportes PDF, registra envíos y mantiene la demo funcional incluso sin llaves externas de Resend.',
    actions: [
      'PDF con ReportLab',
      'Modo demo para correo',
      'Historial auditable',
    ],
  },
  {
    tag: 'Analítica',
    title: 'IA por reglas y certificación',
    description:
      'Clasifica niveles de stock, propone acciones y certifica el contenido del reporte con hashes SHA-256.',
    actions: [
      'Alertas críticas',
      'Resumen ejecutivo',
      'Hash de documento y contenido',
    ],
  },
]

const workflowSteps = [
  {
    badge: 'Auth',
    title: 'Login JWT',
    copy: 'Autenticación con SimpleJWT, refresh token y roles para lectura o administración.',
  },
  {
    badge: 'Empresas',
    title: 'Datos demo',
    copy: 'Empresas, productos e inventario sembrados con casos diseñados para mostrar decisiones técnicas.',
  },
  {
    badge: 'Inventario',
    title: 'PDF + hash',
    copy: 'Descarga de reportes y generación de hashes para verificar integridad del documento.',
  },
  {
    badge: 'API',
    title: 'OpenAPI',
    copy: 'Documentación interactiva disponible para revisar contratos REST y probar endpoints.',
  },
]

const getHeroContent = (isAuthenticated, user) => {
  if (isAuthenticated && user) {
    const displayName = user.full_name || user.email || 'Usuario'
    return {
      eyebrow: 'Sesión activa',
      title: `Hola ${displayName}, el demo está listo para recorrer.`,
      description:
        'Gestiona empresas, productos e inventario; luego genera un PDF, revisa el análisis inteligente y valida los hashes del reporte.',
      buttons: [
        { label: 'Ver empresas', variant: 'primary', as: 'a', href: '/empresas' },
        { label: 'Abrir inventario', variant: 'secondary', as: 'a', href: '/inventario' },
        { label: 'Ver API docs', variant: 'ghost', as: 'a', href: API_DOCS_URL },
      ],
      roadmap: {
        eyebrow: 'Siguiente paso',
        title: 'Recorrido de evaluación',
        description:
          'Este recorrido está pensado para que alguien vea rápido frontend, backend, permisos, documentos y trazabilidad.',
        bullets: [
          { text: 'JWT activo y rol detectado', variant: 'primary' },
          { text: 'Datos demo listos para explorar', variant: 'secondary' },
          { text: 'PDF, análisis y hash disponibles', variant: 'accent' },
        ],
      },
    }
  }

  return {
    eyebrow: 'Proyecto demo fullstack',
    title: 'Inventario Pro muestra mi trabajo con React, Django REST y automatización de reportes.',
    description:
      'Una app de portafolio con flujo real: login JWT, empresas, productos, inventario, PDF, correo simulado en demo, análisis de stock y certificación por hash.',
    buttons: [
      { label: 'Probar demo', variant: 'primary', as: 'a', href: '/login' },
      { label: 'Ver empresas', variant: 'secondary', as: 'a', href: '/empresas' },
      { label: 'API docs', variant: 'ghost', as: 'a', href: API_DOCS_URL },
    ],
    roadmap: {
      eyebrow: 'Credenciales demo',
      title: 'Admin y lectura disponibles',
      description:
        'Admin: admin.demo@example.com / DemoAdmin2026!. Lectura: demo@example.com / DemoUser2026!.',
      bullets: [
        { text: 'Backend sembrado con seed_demo', variant: 'primary' },
        { text: 'Modo demo sin llaves externas', variant: 'secondary' },
        { text: 'Swagger disponible en la API', variant: 'accent' },
      ],
    },
  }
}

const workflowContent = {
  eyebrow: 'User journey',
  title: 'De sesión a reporte certificado',
  ctaLabel: 'Ver API docs →',
  ctaHref: API_DOCS_URL,
  steps: workflowSteps,
}

// Componente Landing Page
const LandingPage = () => {
  const { isAuthenticated, user } = useAuth()
  const heroContent = getHeroContent(isAuthenticated, user)
  
  return (
    <LandingTemplate hero={heroContent} sections={sections} workflow={workflowContent} />
  )
}

// Componente de ruta protegida
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-brand-primary border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

// Placeholder para páginas pendientes
const PlaceholderPage = ({ title }) => (
  <div className="min-h-screen bg-slate-950 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-3xl font-display font-bold text-white mb-4">{title}</h1>
      <p className="text-white/60">Esta página está en construcción</p>
      <a
        href="/"
        className="inline-block mt-6 px-6 py-3 rounded-full bg-brand-primary text-slate-950 font-semibold hover:bg-brand-primary/90 transition-colors"
      >
        Volver al inicio
      </a>
    </div>
  </div>
)

const AppRoutes = () => {
  return (
    <Routes>
      {/* Rutas públicas */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/empresas" element={<EmpresasPage />} />
      
      {/* Rutas protegidas */}
      <Route
        path="/inventario"
        element={
          <ProtectedRoute>
            <InventarioPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/ia-beta"
        element={
          <ProtectedRoute>
            <IABetaPage />
          </ProtectedRoute>
        }
      />

      {/* Ruta 404 */}
      <Route
        path="*"
        element={
          <div className="min-h-screen bg-slate-950 flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-6xl font-display font-bold text-brand-primary mb-4">
                404
              </h1>
              <p className="text-xl text-white mb-2">Página no encontrada</p>
              <p className="text-white/60 mb-8">
                La página que buscas no existe o fue movida.
              </p>
              <a
                href="/"
                className="inline-block px-6 py-3 rounded-full bg-brand-primary text-slate-950 font-semibold hover:bg-brand-primary/90 transition-colors"
              >
                Volver al inicio
              </a>
            </div>
          </div>
        }
      />
    </Routes>
  )
}

export default AppRoutes
