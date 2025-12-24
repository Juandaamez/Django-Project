/**
 * PasswordField Molecule - Campo de contraseña con toggle de visibilidad
 */
import { useState } from 'react'
import FormField from './FormField'

// Iconos inline para no depender de librerías externas
const EyeIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
)

const EyeOffIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
    <line x1="1" y1="1" x2="23" y2="23" />
  </svg>
)

const LockIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
  </svg>
)

const PasswordField = ({
  label = 'Contraseña',
  name = 'password',
  placeholder = '••••••••',
  value,
  onChange,
  onBlur,
  error,
  touched,
  required = true,
  showStrength = false,
  className = '',
  ...rest
}) => {
  const [showPassword, setShowPassword] = useState(false)

  // Calcular fortaleza de la contraseña
  const getPasswordStrength = (password) => {
    if (!password) return { score: 0, label: '', color: '' }
    
    let score = 0
    if (password.length >= 8) score++
    if (password.length >= 12) score++
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++
    if (/\d/.test(password)) score++
    if (/[^a-zA-Z0-9]/.test(password)) score++

    const levels = [
      { label: 'Muy débil', color: 'bg-red-500' },
      { label: 'Débil', color: 'bg-orange-500' },
      { label: 'Regular', color: 'bg-yellow-500' },
      { label: 'Fuerte', color: 'bg-green-400' },
      { label: 'Muy fuerte', color: 'bg-brand-primary' },
    ]

    return { score, ...levels[Math.min(score, 4)] }
  }

  const strength = getPasswordStrength(value)

  return (
    <div className={`space-y-2 ${className}`}>
      {/* Campo de contraseña */}
      <div className="relative">
        <FormField
          type={showPassword ? 'text' : 'password'}
          label={label}
          name={name}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          error={error}
          touched={touched}
          icon={LockIcon}
          required={required}
          {...rest}
        />
        
        {/* Toggle visibility button */}
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-4 top-[42px] text-white/40 hover:text-white/70 transition-colors"
          aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
        >
          {showPassword ? (
            <EyeOffIcon className="w-5 h-5" />
          ) : (
            <EyeIcon className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Indicador de fortaleza */}
      {showStrength && value && (
        <div className="space-y-1.5 animate-in fade-in duration-300">
          <div className="flex gap-1">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                  i < strength.score ? strength.color : 'bg-white/10'
                }`}
              />
            ))}
          </div>
          <p className="text-xs text-white/50">
            Fortaleza: <span className="text-white/70">{strength.label}</span>
          </p>
        </div>
      )}
    </div>
  )
}

export default PasswordField
