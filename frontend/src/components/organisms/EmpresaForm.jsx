/**
 * EmpresaForm - Formulario para crear/editar empresas
 * Solo disponible para administradores
 */
import { useState, useEffect } from 'react'
import Input from '../atoms/Input'
import Button from '../atoms/Button'
import Spinner from '../atoms/Spinner'

// Iconos SVG inline
const BuildingIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
  </svg>
)

const IdIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
  </svg>
)

const MapPinIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
)

const PhoneIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
  </svg>
)

const initialFormData = {
  nit: '',
  nombre: '',
  direccion: '',
  telefono: '',
}

const EmpresaForm = ({
  empresa = null,
  onSubmit,
  onCancel,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState(initialFormData)
  const [errors, setErrors] = useState({})
  const isEditing = !!empresa

  useEffect(() => {
    if (empresa) {
      setFormData({
        nit: empresa.nit || '',
        nombre: empresa.nombre || '',
        direccion: empresa.direccion || '',
        telefono: empresa.telefono || '',
      })
    } else {
      setFormData(initialFormData)
    }
    setErrors({})
  }, [empresa])

  const validateForm = () => {
    const newErrors = {}

    if (!formData.nit.trim()) {
      newErrors.nit = 'El NIT es obligatorio'
    } else if (!/^[0-9-]+$/.test(formData.nit)) {
      newErrors.nit = 'El NIT solo debe contener números y guiones'
    }

    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es obligatorio'
    } else if (formData.nombre.length < 3) {
      newErrors.nombre = 'El nombre debe tener al menos 3 caracteres'
    }

    if (!formData.direccion.trim()) {
      newErrors.direccion = 'La dirección es obligatoria'
    }

    if (!formData.telefono.trim()) {
      newErrors.telefono = 'El teléfono es obligatorio'
    } else if (!/^[0-9+\-() ]+$/.test(formData.telefono)) {
      newErrors.telefono = 'El teléfono tiene un formato inválido'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Limpiar error del campo al escribir
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* NIT */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          NIT <span className="text-red-400">*</span>
        </label>
        <Input
          name="nit"
          value={formData.nit}
          onChange={handleChange}
          placeholder="Ej: 123456789-0"
          icon={IdIcon}
          error={!!errors.nit}
          disabled={isEditing || isLoading}
        />
        {errors.nit && (
          <p className="mt-1.5 text-sm text-red-400">{errors.nit}</p>
        )}
        {isEditing && (
          <p className="mt-1.5 text-xs text-white/50">
            El NIT no se puede modificar
          </p>
        )}
      </div>

      {/* Nombre */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Nombre de la Empresa <span className="text-red-400">*</span>
        </label>
        <Input
          name="nombre"
          value={formData.nombre}
          onChange={handleChange}
          placeholder="Nombre de la empresa"
          icon={BuildingIcon}
          error={!!errors.nombre}
          disabled={isLoading}
        />
        {errors.nombre && (
          <p className="mt-1.5 text-sm text-red-400">{errors.nombre}</p>
        )}
      </div>

      {/* Dirección */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Dirección <span className="text-red-400">*</span>
        </label>
        <Input
          name="direccion"
          value={formData.direccion}
          onChange={handleChange}
          placeholder="Dirección de la empresa"
          icon={MapPinIcon}
          error={!!errors.direccion}
          disabled={isLoading}
        />
        {errors.direccion && (
          <p className="mt-1.5 text-sm text-red-400">{errors.direccion}</p>
        )}
      </div>

      {/* Teléfono */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Teléfono <span className="text-red-400">*</span>
        </label>
        <Input
          name="telefono"
          value={formData.telefono}
          onChange={handleChange}
          placeholder="Ej: +57 300 123 4567"
          icon={PhoneIcon}
          error={!!errors.telefono}
          disabled={isLoading}
        />
        {errors.telefono && (
          <p className="mt-1.5 text-sm text-red-400">{errors.telefono}</p>
        )}
      </div>

      {/* Botones */}
      <div className="flex gap-3 pt-4">
        <Button
          type="button"
          variant="ghost"
          onClick={onCancel}
          disabled={isLoading}
          className="flex-1"
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="primary"
          disabled={isLoading}
          className="flex-1"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <Spinner size="sm" />
              {isEditing ? 'Actualizando...' : 'Creando...'}
            </span>
          ) : (
            isEditing ? 'Actualizar Empresa' : 'Crear Empresa'
          )}
        </Button>
      </div>
    </form>
  )
}

export default EmpresaForm
