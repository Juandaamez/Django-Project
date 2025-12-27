/**
 * Badge Atom - Etiqueta de estado o categoría
 */

const variantClasses = {
  default: 'bg-white/10 text-white/80',
  primary: 'bg-brand-primary/20 text-brand-primary',
  secondary: 'bg-brand-secondary/20 text-brand-secondary',
  success: 'bg-green-500/20 text-green-400',
  warning: 'bg-amber-500/20 text-amber-400',
  danger: 'bg-red-500/20 text-red-400',
  info: 'bg-blue-500/20 text-blue-400',
}

const sizeClasses = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-xs',
  lg: 'px-3 py-1.5 text-sm',
}

const Badge = ({
  children,
  variant = 'default',
  size = 'md',
  className = '',
  icon,
}) => {
  return (
    <span
      className={`
        inline-flex items-center gap-1.5 rounded-full font-medium
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
    >
      {icon && <span className="flex-shrink-0">{icon}</span>}
      {children}
    </span>
  )
}

export default Badge
