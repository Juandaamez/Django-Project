/**
 * GlowOrb Atom - Orbe decorativo con efecto de brillo animado
 */

const GlowOrb = ({
  color = 'primary',
  size = 'md',
  position = {},
  blur = 'xl',
  opacity = 40,
  animated = true,
  className = '',
}) => {
  const colorClasses = {
    primary: 'bg-brand-primary',
    secondary: 'bg-brand-secondary',
    accent: 'bg-brand-accent',
    mixed: 'bg-gradient-to-br from-brand-primary via-brand-secondary to-brand-accent',
  }

  const sizeClasses = {
    sm: 'w-32 h-32',
    md: 'w-64 h-64',
    lg: 'w-96 h-96',
    xl: 'w-[500px] h-[500px]',
  }

  const blurClasses = {
    md: 'blur-2xl',
    lg: 'blur-3xl',
    xl: 'blur-[100px]',
    '2xl': 'blur-[150px]',
  }

  const { top, right, bottom, left } = position

  return (
    <div
      className={`
        absolute rounded-full pointer-events-none
        ${colorClasses[color]}
        ${sizeClasses[size]}
        ${blurClasses[blur]}
        ${animated ? 'animate-pulse' : ''}
        ${className}
      `}
      style={{
        opacity: opacity / 100,
        top,
        right,
        bottom,
        left,
      }}
      aria-hidden="true"
    />
  )
}

export default GlowOrb
