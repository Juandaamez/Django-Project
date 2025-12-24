/**
 * Logo Atom - Logo de la aplicación con variantes
 */

const Logo = ({ size = 'md', animated = false, className = '' }) => {
  const sizeConfig = {
    sm: { container: 'w-8 h-8', text: 'text-lg' },
    md: { container: 'w-12 h-12', text: 'text-2xl' },
    lg: { container: 'w-16 h-16', text: 'text-3xl' },
    xl: { container: 'w-24 h-24', text: 'text-5xl' },
  }

  const { container, text } = sizeConfig[size]

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div
        className={`${container} relative flex items-center justify-center rounded-2xl bg-gradient-to-br from-brand-primary via-brand-secondary to-brand-accent p-[2px] ${
          animated ? 'animate-pulse' : ''
        }`}
      >
        <div className="flex h-full w-full items-center justify-center rounded-2xl bg-slate-950">
          <span className={`${text} font-bold font-display bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent`}>
            LT
          </span>
        </div>
        {/* Glow effect */}
        <div className="absolute inset-0 -z-10 rounded-2xl bg-gradient-to-br from-brand-primary via-brand-secondary to-brand-accent opacity-50 blur-xl" />
      </div>
      <div className="flex flex-col">
        <span className="font-display font-bold text-white tracking-tight">
          LiteThinking
        </span>
        <span className="text-xs text-white/50">Enterprise Platform</span>
      </div>
    </div>
  )
}

export default Logo
