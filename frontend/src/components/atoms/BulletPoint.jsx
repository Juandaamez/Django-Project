const bulletVariants = {
  primary: 'bg-brand-primary',
  secondary: 'bg-brand-secondary',
  accent: 'bg-brand-accent',
}

function BulletPoint({ children, variant = 'primary' }) {
  const bulletClass = bulletVariants[variant] ?? bulletVariants.primary

  return (
    <li className="flex items-center gap-2 text-sm text-slate-300">
      <span className={`h-1.5 w-1.5 rounded-full ${bulletClass}`} />
      {children}
    </li>
  )
}

export default BulletPoint
