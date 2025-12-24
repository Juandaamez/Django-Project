/**
 * LoginHero Organism - Panel decorativo con información de la plataforma
 * Incluye efectos visuales, características y branding
 */
import Logo from '../atoms/Logo'
import GlowOrb from '../atoms/GlowOrb'
import ParticleField from '../atoms/ParticleField'
import FeatureCard from '../molecules/FeatureCard'

// Íconos inline
const ShieldIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
  </svg>
)

const ChartIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="18" y1="20" x2="18" y2="10" />
    <line x1="12" y1="20" x2="12" y2="4" />
    <line x1="6" y1="20" x2="6" y2="14" />
  </svg>
)

const CubeIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
    <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
    <line x1="12" y1="22.08" x2="12" y2="12" />
  </svg>
)

const BrainIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-1.54" />
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-1.54" />
  </svg>
)

const features = [
  {
    icon: ShieldIcon,
    title: 'Autenticación JWT',
    description: 'Tokens seguros con refresh automático y roles de usuario',
  },
  {
    icon: ChartIcon,
    title: 'Gestión de Inventario',
    description: 'Control total de productos, stock y reportes PDF',
  },
  {
    icon: CubeIcon,
    title: 'Blockchain',
    description: 'Trazabilidad inmutable y sellado de transacciones',
  },
  {
    icon: BrainIcon,
    title: 'Inteligencia Artificial',
    description: 'Predicciones de stock y recomendaciones inteligentes',
  },
]

const LoginHero = ({ className = '' }) => {
  return (
    <div
      className={`
        relative hidden lg:flex flex-col justify-between
        bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900
        p-12 overflow-hidden
        ${className}
      `}
    >
      {/* Partículas animadas */}
      <ParticleField particleCount={40} />

      {/* Orbes decorativos */}
      <GlowOrb
        color="primary"
        size="lg"
        position={{ top: '-10%', right: '-10%' }}
        opacity={30}
      />
      <GlowOrb
        color="secondary"
        size="md"
        position={{ bottom: '10%', left: '-5%' }}
        opacity={25}
      />
      <GlowOrb
        color="accent"
        size="sm"
        position={{ top: '40%', right: '20%' }}
        opacity={20}
      />

      {/* Grid pattern background */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.1) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
        }}
      />

      {/* Contenido superior */}
      <div className="relative z-10">
        <Logo size="md" animated />
        
        <div className="mt-12 max-w-md">
          <h1 className="text-4xl font-display font-bold text-white leading-tight">
            Gestiona tu empresa con{' '}
            <span className="bg-gradient-to-r from-brand-primary via-brand-secondary to-brand-accent bg-clip-text text-transparent">
              tecnología de punta
            </span>
          </h1>
          <p className="mt-4 text-lg text-white/60 leading-relaxed">
            Plataforma integral para administrar empresas, productos e inventario 
            con inteligencia artificial y blockchain.
          </p>
        </div>
      </div>

      {/* Features grid */}
      <div className="relative z-10 grid grid-cols-2 gap-4 mt-8">
        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>

      {/* Footer con stats */}
      <div className="relative z-10 mt-8 pt-8 border-t border-white/10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div>
              <p className="text-2xl font-bold text-white">500+</p>
              <p className="text-xs text-white/50">Empresas activas</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">10K+</p>
              <p className="text-xs text-white/50">Productos gestionados</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">99.9%</p>
              <p className="text-xs text-white/50">Uptime</p>
            </div>
          </div>
        </div>
      </div>

      {/* Animated code snippets decoration */}
      <div className="absolute bottom-20 right-8 w-64 opacity-20 font-mono text-xs text-brand-primary">
        <pre className="animate-pulse">
{`{
  "auth": "JWT",
  "role": "admin",
  "blockchain": true,
  "ai_enabled": true
}`}
        </pre>
      </div>
    </div>
  )
}

export default LoginHero
