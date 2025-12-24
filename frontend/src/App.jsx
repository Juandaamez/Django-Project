import LandingTemplate from './components/templates/LandingTemplate'

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

const heroContent = {
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

const workflowContent = {
  eyebrow: 'User journey',
  title: 'De sesión a PDF firmado',
  ctaLabel: 'Ver documentación →',
  ctaHref: '/docs',
  steps: workflowSteps,
}

function App() {
  return (
    <LandingTemplate hero={heroContent} sections={sections} workflow={workflowContent} />
  )
}

export default App
