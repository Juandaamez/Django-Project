/**
 * IconButton Atom - Botón con solo icono
 */

const variantClasses = {
  default: 'text-white/60 hover:text-white hover:bg-white/10',
  primary: 'text-brand-primary hover:bg-brand-primary/10',
  danger: 'text-red-400 hover:bg-red-500/10',
  success: 'text-green-400 hover:bg-green-500/10',
}

const sizeClasses = {
  sm: 'p-1.5',
  md: 'p-2',
  lg: 'p-3',
}

const IconButton = ({
  children,
  onClick,
  variant = 'default',
  size = 'md',
  disabled = false,
  className = '',
  title,
  'aria-label': ariaLabel,
  ...rest
}) => {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      title={title}
      aria-label={ariaLabel || title}
      className={`
        rounded-lg transition-colors duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
      {...rest}
    >
      {children}
    </button>
  )
}

export default IconButton
