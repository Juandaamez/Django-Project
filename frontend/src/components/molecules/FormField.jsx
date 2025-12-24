/**
 * FormField Molecule - Campo de formulario con label, input y mensaje de error
 */
import Input from '../atoms/Input'

const FormField = ({
  label,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  touched,
  icon,
  required = false,
  hint,
  className = '',
  ...inputProps
}) => {
  const showError = touched && error

  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-white/80"
        >
          {label}
          {required && <span className="text-brand-secondary ml-1">*</span>}
        </label>
      )}
      
      <Input
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        icon={icon}
        error={showError}
        aria-invalid={showError}
        aria-describedby={showError ? `${name}-error` : undefined}
        {...inputProps}
      />
      
      {/* Hint text */}
      {hint && !showError && (
        <p className="text-xs text-white/40">{hint}</p>
      )}
      
      {/* Error message with animation */}
      <div
        className={`overflow-hidden transition-all duration-300 ${
          showError ? 'max-h-10 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <p
          id={`${name}-error`}
          className="text-sm text-red-400 flex items-center gap-1.5"
          role="alert"
        >
          <svg className="w-4 h-4 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          {error}
        </p>
      </div>
    </div>
  )
}

export default FormField
