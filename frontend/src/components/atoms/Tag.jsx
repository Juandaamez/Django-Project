const variantClasses = {
  default: 'text-brand-primary/90',
  secondary: 'text-brand-secondary',
  outline: 'border border-white/20 text-white',
  subtle: 'text-slate-400',
}

function Tag({ children, variant = 'default', className = '' }) {
  const variantClass = variantClasses[variant] ?? variantClasses.default
  const mergedClassName = ['tag', variantClass, className].filter(Boolean).join(' ')

  return <span className={mergedClassName}>{children}</span>
}

export default Tag
