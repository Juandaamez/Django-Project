/**
 * Checkbox Atom - Checkbox estilizado con animación
 */

const Checkbox = ({
  checked = false,
  onChange,
  label,
  name,
  id,
  disabled = false,
  className = '',
}) => {
  return (
    <label
      className={`group flex items-center gap-3 cursor-pointer select-none ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      } ${className}`}
    >
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          name={name}
          id={id || name}
          disabled={disabled}
          className="peer sr-only"
        />
        <div
          className={`w-5 h-5 rounded-md border-2 transition-all duration-200
            ${
              checked
                ? 'bg-brand-primary border-brand-primary'
                : 'bg-transparent border-white/30 group-hover:border-white/50'
            }
          `}
        >
          {/* Checkmark */}
          <svg
            className={`w-full h-full p-0.5 text-slate-950 transition-transform duration-200 ${
              checked ? 'scale-100' : 'scale-0'
            }`}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </div>
        {/* Glow on check */}
        {checked && (
          <div className="absolute inset-0 rounded-md bg-brand-primary opacity-30 blur-md -z-10" />
        )}
      </div>
      {label && (
        <span className="text-sm text-white/70 group-hover:text-white/90 transition-colors">
          {label}
        </span>
      )}
    </label>
  )
}

export default Checkbox
