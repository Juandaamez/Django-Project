const variantClasses = {
  primary: 'bg-brand-primary text-slate-950 shadow-glow hover:bg-brand-primary/90',
  secondary: 'border border-white/20 text-white hover:border-brand-primary/60',
  ghost: 'border border-white/10 text-white/70 hover:text-white',
}

const sizeClasses = {
  sm: 'px-4 py-2 text-xs',
  md: 'px-6 py-3 text-sm',
  lg: 'px-8 py-4 text-base',
}

function Button({
  as: Component = 'button',
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  ...rest
}) {
  const mergedClassName = [
    'rounded-full font-semibold transition-colors duration-150',
    variantClasses[variant] ?? variantClasses.primary,
    sizeClasses[size] ?? sizeClasses.md,
    className,
  ]
    .filter(Boolean)
    .join(' ')

  const componentProps = { ...rest }
  if (Component === 'button' && componentProps.type === undefined) {
    componentProps.type = 'button'
  }

  return (
    <Component className={mergedClassName} {...componentProps}>
      {children}
    </Component>
  )
}

export default Button
