const SectionCard = ({ tag, title, description, actions }) => (
  <article className="glass-panel group transition-transform duration-200 hover:-translate-y-1">
    <span className="tag text-brand-primary/90">{tag}</span>
    <h3 className="mt-4 text-2xl font-display text-white">{title}</h3>
    <p className="mt-2 text-sm text-slate-300">{description}</p>
    <ul className="mt-5 space-y-2 text-sm text-slate-300">
      {actions.map((action) => (
        <li key={action} className="flex items-center gap-2">
          <span className="h-1.5 w-1.5 rounded-full bg-brand-primary" />
          {action}
        </li>
      ))}
    </ul>
  </article>
)

const workflow = [
  {
    badge: 'Auth',
    title: 'Secure login',
    copy: 'JWT (SimpleJWT) ready endpoints for administrar y validar credenciales cifradas.',
  },
  {
    badge: 'Empresas',
    title: 'Company registry',
    copy: 'CRUD completo con roles (admin vs externo) y búsquedas para NIT y razón social.',
  },
  {
    badge: 'Inventario',
    title: 'PDF + Blockchain',
    copy: 'Descarga y firma digital del inventario con envío automatizado vía API externa.',
  },
  {
    badge: 'IA',
    title: 'Predictive insights',
    copy: 'Sugerencias de stock y precios en múltiples monedas usando librerías de IA.',
  },
]

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
      'Consulta niveles de stock, exporta reportes y programa envíos seguros vía servicios externos.',
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

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="relative isolate overflow-hidden bg-grid px-6 pb-24 pt-16 sm:px-12">
        <div
          className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-gradient-to-br from-brand-primary/30 via-brand-secondary/20 to-slate-900 blur-3xl"
          aria-hidden="true"
        />

        <div className="mx-auto flex max-w-6xl flex-col gap-12">
          <header className="grid gap-8 lg:grid-cols-[3fr,2fr]">
            <div className="space-y-6">
              <span className="tag text-brand-secondary">Frontend · Atomic Design</span>
              <h1 className="text-4xl font-display leading-tight text-white sm:text-5xl">
                Panel operativo para empresas, productos e inventario con Tailwind + React 18.
              </h1>
              <p className="max-w-2xl text-base text-slate-300">
                Esta maqueta define la capa visible que consumirá la API Django. Cada bloque corresponde a un
                template Atomic listo para conectar con hooks, contextos y servicios (`src/services`).
              </p>
              <div className="flex flex-wrap gap-3">
                <button className="rounded-full bg-brand-primary px-6 py-3 text-sm font-semibold text-slate-950 shadow-glow">
                  Iniciar Sesión
                </button>
                <button className="rounded-full border border-white/20 px-6 py-3 text-sm font-semibold text-white">
                  Ver Empresas
                </button>
                <button className="rounded-full border border-white/10 px-6 py-3 text-sm font-semibold text-white/70">
                  Activar IA Beta
                </button>
              </div>
            </div>

            <div className="glass-panel">
              <p className="text-sm uppercase tracking-[0.3em] text-brand-primary">Roadmap</p>
              <h2 className="mt-3 text-2xl font-display text-white">IA · Blockchain · PDF seguro</h2>
              <p className="mt-3 text-sm text-slate-300">
                El frontend consumirá endpoints JWT (`/api/auth/login/`) y servicios especializados para PDF/Correo. Se reservan
                hooks específicos en `src/hooks` y contextos globales para sesionar al usuario.
              </p>
              <ul className="mt-4 space-y-3 text-sm text-slate-200">
                <li className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-brand-primary" /> Estados de carga y skeletons listos para datos reales.
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-brand-secondary" /> Atomic templates para Empresa, Productos, Inventario.
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-brand-accent" /> Integración de firmas blockchain y recomendaciones IA.
                </li>
              </ul>
            </div>
          </header>

          <section className="grid gap-6 md:grid-cols-2">
            {sections.map((section) => (
              <SectionCard key={section.tag} {...section} />
            ))}
          </section>

          <section className="glass-panel">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.4em] text-brand-secondary/80">User journey</p>
                <h3 className="mt-2 text-2xl font-display text-white">De sesión a PDF firmado</h3>
              </div>
              <a href="/docs" className="text-sm font-semibold text-brand-primary">
                Ver documentación →
              </a>
            </div>
            <ol className="mt-6 space-y-6">
              {workflow.map((step, index) => (
                <li key={step.title} className="flex items-start gap-4">
                  <span className="text-3xl font-display text-brand-primary/70">{String(index + 1).padStart(2, '0')}</span>
                  <div>
                    <span className="tag border-brand-secondary/40 text-brand-secondary">{step.badge}</span>
                    <h4 className="mt-2 text-xl font-semibold text-white">{step.title}</h4>
                    <p className="text-sm text-slate-300">{step.copy}</p>
                  </div>
                </li>
              ))}
            </ol>
          </section>
        </div>
      </div>
    </div>
  )
}

export default App
