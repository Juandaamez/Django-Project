const variantClasses = {
  primary: 'bg-brand-primary text-slate-950 shadow-glow hover:bg-brand-primary/90',
  secondary: 'border border-white/20 text-white hover:border-brand-primary/60',
  ghost: 'border border-white/10 text-white/70 hover:text-white',
}

function Button({
  as: Component = 'button',
  children,
  variant = 'primary',
  className = '',
  ...rest
}) {
  const mergedClassName = [
    'rounded-full px-6 py-3 text-sm font-semibold transition-colors duration-150',
    variantClasses[variant] ?? variantClasses.primary,
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
