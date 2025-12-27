const Input = ({
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  onFocus,
  name,
  id,
  disabled = false,
  error = false,
  icon: Icon,
  iconPosition = 'left',
  className = '',
  ...rest
}) => {
  const baseClasses = [
    'w-full px-4 py-3.5 rounded-xl',
    'bg-white/5',
    'border transition-all duration-300',
    'text-white placeholder-white/40',
    'focus:outline-none focus:ring-2',
    'disabled:opacity-50 disabled:cursor-not-allowed',
  ]

  const stateClasses = error
    ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20'
    : 'border-white/10 hover:border-white/20 focus:border-brand-primary focus:ring-brand-primary/20'

  const paddingClasses = Icon
    ? iconPosition === 'left'
      ? 'pl-12'
      : 'pr-12'
    : ''

  return (
    <div className="relative">
      {Icon && (
        <div
          className={`absolute top-1/2 -translate-y-1/2 text-white/40 transition-colors duration-300 ${
            iconPosition === 'left' ? 'left-4' : 'right-4'
          }`}
        >
          <Icon className="w-5 h-5" />
        </div>
      )}
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        onFocus={onFocus}
        name={name}
        id={id || name}
        disabled={disabled}
        className={[...baseClasses, stateClasses, paddingClasses, className]
          .filter(Boolean)
          .join(' ')}
        {...rest}
      />
    </div>
  )
}

export default Input
