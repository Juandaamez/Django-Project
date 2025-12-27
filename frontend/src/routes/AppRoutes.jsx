/**
 * AppRoutes - Configuración de rutas de la aplicación
 * Incluye rutas públicas y protegidas
 */
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// Pages
import LoginPage from '../pages/LoginPage'
import EmpresasPage from '../pages/EmpresasPage'
import InventarioPage from '../pages/InventarioPage'
import LandingTemplate from '../components/templates/LandingTemplate'

// Landing content (movido desde App.jsx)
const sections = [
  {
    tag: 'Empresas',
    title: 'Gestión centralizada de empresas',
    description:
      'Crea, edita y elimina compañías con metadatos clave (NIT, dirección, teléfono). Diseño pensado para administradores.',
    actions: [
      'Validación en vivo del NIT',
      'Asignación de responsables',
      'Visor público para usuarios externos',
    ],
  },
  {
    tag: 'Productos',
    title: 'Catálogo multi-moneda',
    description:
      'Define códigos únicos, características y precios dinamizados por divisa para cada empresa.',
    actions: [
      'Switch rápido COP / USD / EUR',
      'Relación directa con inventario',
      'Filtros por empresa, código y tags IA',
    ],
  },
  {
    tag: 'Inventario',
    title: 'Panel operativo y PDF',
    description:
      'Consulta niveles de stock, exporta reportes y programa envíos seguros vía servicios REST confiables.',
    actions: [
      'Generación de PDF con branding',
      'Webhook para correo y API REST',
      'Integración blockchain para sellado',
    ],
  },
  {
    tag: 'IA + Blockchain',
    title: 'Funcionalidad emergente',
    description:
      'Módulo para auditar trazabilidad y sugerir reposiciones inteligentes usando embeddings + NFTs ligeros.',
    actions: [
      'Alertas inteligentes por empresa',
      'Dashboard de riesgo / fraude',
      'Registro inmutable por transacción',
    ],
  },
]

const workflowSteps = [
  {
    badge: 'Auth',
    title: 'Secure login',
    copy: 'JWT (SimpleJWT) ready endpoints para validar credenciales cifradas.',
  },
  {
    badge: 'Empresas',
    title: 'Company registry',
    copy: 'CRUD con roles (admin vs externo) y búsquedas por NIT o nombre.',
  },
  {
    badge: 'Inventario',
    title: 'PDF + Blockchain',
    copy: 'Descarga y firma digital del inventario con envío automatizado vía API REST.',
  },
  {
    badge: 'IA',
    title: 'Predictive insights',
    copy: 'Sugerencias de stock y precios en múltiples monedas usando librerías de IA.',
  },
]

const getHeroContent = (isAuthenticated, user) => {
  if (isAuthenticated && user) {
    const displayName = user.first_name || user.username || 'Usuario'
    return {
      eyebrow: '✨ Bienvenido de nuevo',
      title: `Hola ${displayName}, listo para gestionar tu inventario?`,
      description:
        '🎯 Tienes acceso completo a todas las funcionalidades. Gestiona empresas, productos, inventario y activa las funciones de IA para optimizar tu operación.',
      buttons: [
        { label: '🏢 Ver Empresas', variant: 'primary', as: 'a', href: '/empresas' },
        { label: '📦 Inventario', variant: 'secondary', as: 'a', href: '/inventario' },
        { label: '🤖 Activar IA Beta', variant: 'ghost', as: 'a', href: '/ia-beta' },
      ],
      roadmap: {
        eyebrow: '🎯 Acciones Rápidas',
        title: 'Continúa donde lo dejaste',
        description:
          'Accede a todas las funcionalidades de la plataforma. Tu sesión está activa y segura con autenticación JWT.',
        bullets: [
          { text: '✅ Sesión activa y segura', variant: 'primary' },
          { text: '🚀 Todas las funciones desbloqueadas', variant: 'secondary' },
          { text: '⚡ IA y Blockchain disponibles', variant: 'accent' },
        ],
      },
    }
  }

  return {
    eyebrow: 'Frontend · Atomic Design',
    title: 'Panel operativo para empresas, productos e inventario con Tailwind + React 18.',
    description:
      'Esta maqueta define la capa visible que consumirá la API Django. Cada bloque corresponde a un template Atomic listo para hooks, contextos y servicios REST.',
    buttons: [
      { label: 'Iniciar Sesión', variant: 'primary', as: 'a', href: '/login' },
      { label: 'Ver Empresas', variant: 'secondary', as: 'a', href: '/empresas' },
      { label: 'Activar IA Beta', variant: 'ghost', as: 'a', href: '/ia-beta' },
    ],
    roadmap: {
      eyebrow: 'Roadmap',
      title: 'IA · Blockchain · PDF seguro',
      description:
        'El frontend consumirá endpoints JWT (/api/auth/login/) y servicios especializados para PDF/Correo. Reservamos hooks en src/hooks y contextos globales para el manejo de sesión.',
      bullets: [
        { text: 'Estados de carga y skeletons listos para datos reales.', variant: 'primary' },
        { text: 'Atomic templates para Empresa, Productos, Inventario.', variant: 'secondary' },
        { text: 'Integración de firmas blockchain y recomendaciones IA.', variant: 'accent' },
      ],
    },
  }
}

const workflowContent = {
  eyebrow: 'User journey',
  title: 'De sesión a PDF firmado',
  ctaLabel: 'Ver documentación →',
  ctaHref: '/docs',
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
            <PlaceholderPage title="IA + Blockchain Beta" />
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
