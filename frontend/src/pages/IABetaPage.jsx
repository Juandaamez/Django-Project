import { useState } from 'react'
import { Link } from 'react-router-dom'
import NavigationBar from '../components/organisms/NavigationBar'

const BrainIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
  </svg>
)

const BlockchainIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
  </svg>
)

const ShieldIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
  </svg>
)

const ChartIcon = () => (
  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>
)

const AlertIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
)

const CheckIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
)

const HashIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
  </svg>
)

const IABetaPage = () => {
  const [activeTab, setActiveTab] = useState('ia')

  const iaFeatures = [
    {
      icon: <AlertIcon />,
      title: 'Alertas Inteligentes',
      description: 'Detecta automáticamente productos sin stock o con niveles críticos y genera alertas priorizadas.',
      color: 'from-red-500 to-orange-500'
    },
    {
      icon: <ChartIcon />,
      title: 'Análisis Predictivo',
      description: 'Analiza patrones de inventario para anticipar necesidades de reabastecimiento.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <BrainIcon />,
      title: 'Resumen Ejecutivo',
      description: 'Genera reportes automáticos con métricas clave y estado general del inventario.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: <CheckIcon />,
      title: 'Recomendaciones',
      description: 'Sugiere acciones específicas basadas en el análisis de datos históricos.',
      color: 'from-green-500 to-emerald-500'
    }
  ]

  const blockchainFeatures = [
    {
      icon: <HashIcon />,
      title: 'Hash SHA-256',
      description: 'Cada documento PDF genera un hash único e irrepetible que certifica su contenido.',
      color: 'from-amber-500 to-yellow-500'
    },
    {
      icon: <ShieldIcon />,
      title: 'Integridad Garantizada',
      description: 'Cualquier modificación al documento invalida el hash, detectando alteraciones.',
      color: 'from-indigo-500 to-blue-500'
    },
    {
      icon: <BlockchainIcon />,
      title: 'Certificación Digital',
      description: 'El hash actúa como firma digital inmutable del estado del inventario.',
      color: 'from-teal-500 to-cyan-500'
    }
  ]

  return (
    <div className="min-h-screen bg-slate-950">
      <NavigationBar />
      
      {/* Hero Section */}
      <div className="pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-brand-primary/20 to-brand-secondary/20 border border-brand-primary/30 mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-primary"></span>
            </span>
            <span className="text-sm font-medium text-brand-primary">Beta Experimental</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-white mb-6">
            <span className="bg-gradient-to-r from-brand-primary via-brand-secondary to-brand-accent bg-clip-text text-transparent">
              IA + Blockchain
            </span>
            <br />
            <span className="text-white/90">en tu Inventario</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-white/60 max-w-2xl mx-auto mb-8">
            Tecnologías emergentes integradas para análisis inteligente y certificación inmutable de tus reportes de inventario.
          </p>

          <Link
            to="/inventario"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-brand-primary to-brand-secondary text-white font-semibold hover:opacity-90 transition-opacity"
          >
            Probar en Inventario
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 mb-12">
        <div className="flex justify-center gap-4">
          <button
            onClick={() => setActiveTab('ia')}
            className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
              activeTab === 'ia'
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg shadow-purple-500/25'
                : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
            }`}
          >
            🤖 Inteligencia Artificial
          </button>
          <button
            onClick={() => setActiveTab('blockchain')}
            className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
              activeTab === 'blockchain'
                ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-500/25'
                : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
            }`}
          >
            🔗 Blockchain
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {activeTab === 'ia' ? (
          <div className="space-y-12">
            {/* IA Section */}
            <div className="grid md:grid-cols-2 gap-6">
              {iaFeatures.map((feature, index) => (
                <div
                  key={index}
                  className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} p-3 text-white mb-4 group-hover:scale-110 transition-transform`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-white/60">{feature.description}</p>
                </div>
              ))}
            </div>

            {/* How IA Works */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <BrainIcon />
                ¿Cómo funciona la IA?
              </h2>
              <div className="space-y-4 text-white/70">
                <p>
                  Nuestro motor de análisis inteligente procesa los datos de tu inventario en tiempo real usando algoritmos de clasificación y detección de patrones:
                </p>
                <ol className="list-decimal list-inside space-y-3 ml-4">
                  <li><strong className="text-white">Clasificación de Stock:</strong> Categoriza productos en niveles crítico (0), bajo (≤10), medio (≤50) y alto (&gt;50).</li>
                  <li><strong className="text-white">Generación de Alertas:</strong> Crea alertas priorizadas según la criticidad del stock detectado.</li>
                  <li><strong className="text-white">Análisis de Valor:</strong> Calcula el valor total del inventario y detecta concentraciones de riesgo.</li>
                  <li><strong className="text-white">Recomendaciones:</strong> Genera sugerencias accionables basadas en el estado actual.</li>
                </ol>
                <p className="mt-4 p-4 rounded-xl bg-white/5 border border-white/10">
                  💡 <strong className="text-white">Próximamente:</strong> Integración con OpenAI GPT y Anthropic Claude para análisis más sofisticados con lenguaje natural.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-12">
            {/* Blockchain Section */}
            <div className="grid md:grid-cols-3 gap-6">
              {blockchainFeatures.map((feature, index) => (
                <div
                  key={index}
                  className="p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                >
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} p-3 text-white mb-4 group-hover:scale-110 transition-transform`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-white/60">{feature.description}</p>
                </div>
              ))}
            </div>

            {/* How Blockchain Works */}
            <div className="p-8 rounded-2xl bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/20">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <BlockchainIcon />
                ¿Cómo funciona la Certificación Blockchain?
              </h2>
              <div className="space-y-4 text-white/70">
                <p>
                  Utilizamos criptografía SHA-256 para crear una "huella digital" única de cada documento, siguiendo los principios de blockchain:
                </p>
                
                {/* Visual Process */}
                <div className="grid md:grid-cols-3 gap-4 my-8">
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-3xl mb-2">📄</div>
                    <div className="text-sm font-medium text-white">1. Documento PDF</div>
                    <div className="text-xs text-white/50 mt-1">Se genera el reporte</div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-3xl mb-2">🔐</div>
                    <div className="text-sm font-medium text-white">2. Hash SHA-256</div>
                    <div className="text-xs text-white/50 mt-1">Se calcula el hash único</div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 text-center">
                    <div className="text-3xl mb-2">✅</div>
                    <div className="text-sm font-medium text-white">3. Certificación</div>
                    <div className="text-xs text-white/50 mt-1">Hash incluido en correo</div>
                  </div>
                </div>

                {/* Hash Example */}
                <div className="p-4 rounded-xl bg-slate-900 border border-white/10 font-mono text-sm">
                  <div className="text-white/50 mb-2">Ejemplo de Hash SHA-256:</div>
                  <div className="text-amber-400 break-all">
                    a7b9c3d8e2f1g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3...
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mt-6">
                  <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20">
                    <div className="flex items-center gap-2 text-green-400 font-medium mb-2">
                      <CheckIcon /> Documento Original
                    </div>
                    <p className="text-sm text-white/60">
                      Si el hash coincide, el documento no ha sido alterado desde su generación.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20">
                    <div className="flex items-center gap-2 text-red-400 font-medium mb-2">
                      <AlertIcon /> Documento Alterado
                    </div>
                    <p className="text-sm text-white/60">
                      Cualquier cambio, incluso un espacio, genera un hash completamente diferente.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* CTA */}
        <div className="mt-16 text-center">
          <div className="p-8 rounded-2xl bg-gradient-to-r from-brand-primary/10 to-brand-secondary/10 border border-brand-primary/20">
            <h3 className="text-2xl font-bold text-white mb-4">
              ¿Listo para probarlo?
            </h3>
            <p className="text-white/60 mb-6 max-w-lg mx-auto">
              Ve a la sección de Inventario, selecciona una empresa y envía un correo con las opciones de IA y Blockchain activadas.
            </p>
            <Link
              to="/inventario"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-brand-primary to-brand-secondary text-white font-semibold hover:opacity-90 transition-opacity text-lg"
            >
              Ir a Inventario
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default IABetaPage
