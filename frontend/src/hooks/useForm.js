/**
 * useForm Hook - Hook personalizado para manejo de formularios
 * Incluye validación, estados touched y manejo de errores
 */
import { useState, useCallback, useMemo } from 'react'

const useForm = (initialValues = {}, validationRules = {}) => {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Validar un campo individual
  const validateField = useCallback(
    (name, value) => {
      const rules = validationRules[name]
      if (!rules) return ''

      for (const rule of rules) {
        const error = rule(value, values)
        if (error) return error
      }

      return ''
    },
    [validationRules, values]
  )

  // Validar todos los campos
  const validateAll = useCallback(() => {
    const newErrors = {}
    let isValid = true

    for (const [name, rules] of Object.entries(validationRules)) {
      const error = validateField(name, values[name])
      if (error) {
        newErrors[name] = error
        isValid = false
      }
    }

    setErrors(newErrors)
    return isValid
  }, [validationRules, values, validateField])

  // Manejar cambio de valor
  const handleChange = useCallback(
    (e) => {
      const { name, value, type, checked } = e.target
      const newValue = type === 'checkbox' ? checked : value

      setValues((prev) => ({ ...prev, [name]: newValue }))

      // Validar si ya fue tocado
      if (touched[name]) {
        setErrors((prev) => ({
          ...prev,
          [name]: validateField(name, newValue),
        }))
      }
    },
    [touched, validateField]
  )

  // Manejar blur
  const handleBlur = useCallback(
    (e) => {
      const { name, value } = e.target
      setTouched((prev) => ({ ...prev, [name]: true }))
      setErrors((prev) => ({
        ...prev,
        [name]: validateField(name, value),
      }))
    },
    [validateField]
  )

  // Establecer valor programáticamente
  const setValue = useCallback((name, value) => {
    setValues((prev) => ({ ...prev, [name]: value }))
  }, [])

  // Establecer error programáticamente
  const setError = useCallback((name, error) => {
    setErrors((prev) => ({ ...prev, [name]: error }))
  }, [])

  // Reset del formulario
  const reset = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
    setIsSubmitting(false)
  }, [initialValues])

  // Manejar submit
  const handleSubmit = useCallback(
    (onSubmit) => async (e) => {
      e.preventDefault()
      
      // Marcar todos como tocados
      const allTouched = Object.keys(validationRules).reduce(
        (acc, key) => ({ ...acc, [key]: true }),
        {}
      )
      setTouched(allTouched)

      const isValid = validateAll()
      if (!isValid) return

      setIsSubmitting(true)
      try {
        await onSubmit(values)
      } finally {
        setIsSubmitting(false)
      }
    },
    [values, validationRules, validateAll]
  )

  // Verificar si el formulario es válido
  const isValid = useMemo(() => {
    return Object.values(errors).every((error) => !error)
  }, [errors])

  // Verificar si hay cambios desde el estado inicial
  const isDirty = useMemo(() => {
    return JSON.stringify(values) !== JSON.stringify(initialValues)
  }, [values, initialValues])

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    isDirty,
    handleChange,
    handleBlur,
    handleSubmit,
    setValue,
    setError,
    reset,
    validateAll,
  }
}

// Validadores comunes
export const validators = {
  required: (message = 'Este campo es requerido') => (value) => {
    if (value === undefined || value === null || value === '') {
      return message
    }
    return ''
  },

  email: (message = 'Ingresa un correo válido') => (value) => {
    if (!value) return ''
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(value) ? '' : message
  },

  minLength: (min, message) => (value) => {
    if (!value) return ''
    return value.length >= min
      ? ''
      : message || `Mínimo ${min} caracteres`
  },

  maxLength: (max, message) => (value) => {
    if (!value) return ''
    return value.length <= max
      ? ''
      : message || `Máximo ${max} caracteres`
  },

  pattern: (regex, message = 'Formato inválido') => (value) => {
    if (!value) return ''
    return regex.test(value) ? '' : message
  },

  match: (fieldName, message) => (value, values) => {
    if (!value) return ''
    return value === values[fieldName]
      ? ''
      : message || `No coincide con ${fieldName}`
  },
}

export default useForm
