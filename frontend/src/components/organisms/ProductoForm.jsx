/**
 * ProductoForm - Formulario para crear/editar productos
 * Solo disponible para administradores
 */
import { useState, useEffect } from 'react'
import Input from '../atoms/Input'
import Button from '../atoms/Button'
import Spinner from '../atoms/Spinner'

// Iconos SVG inline
const CodeIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
  </svg>
)

const ProductIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
  </svg>
)

const CurrencyIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
)

const initialFormData = {
  codigo: '',
  nombre: '',
  caracteristicas: '',
  precios: {
    COP: '',
    USD: '',
    EUR: '',
  },
  empresa: '',
}

const currencySymbols = {
  COP: '$',
  USD: 'US$',
  EUR: '€',
}

const ProductoForm = ({
  producto = null,
  empresas = [],
  selectedEmpresaNit = '',
  onSubmit,
  onCancel,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState(initialFormData)
  const [errors, setErrors] = useState({})
  const isEditing = !!producto

  useEffect(() => {
    if (producto) {
      setFormData({
        codigo: producto.codigo || '',
        nombre: producto.nombre || '',
        caracteristicas: producto.caracteristicas || '',
        precios: {
          COP: producto.precios?.COP?.toString() || '',
          USD: producto.precios?.USD?.toString() || '',
          EUR: producto.precios?.EUR?.toString() || '',
        },
        empresa: producto.empresa || '',
      })
    } else {
      setFormData({
        ...initialFormData,
        empresa: selectedEmpresaNit,
      })
    }
    setErrors({})
  }, [producto, selectedEmpresaNit])

  const validateForm = () => {
    const newErrors = {}

    if (!formData.codigo.trim()) {
      newErrors.codigo = 'El código es obligatorio'
    }

    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es obligatorio'
    }

    if (!formData.caracteristicas.trim()) {
      newErrors.caracteristicas = 'Las características son obligatorias'
    }

    if (!formData.empresa) {
      newErrors.empresa = 'Debe seleccionar una empresa'
    }

    // Validar al menos un precio
    const hasPrice = Object.values(formData.precios).some(p => p && parseFloat(p) > 0)
    if (!hasPrice) {
      newErrors.precios = 'Debe ingresar al menos un precio'
    }

    // Validar que los precios sean números válidos
    Object.entries(formData.precios).forEach(([currency, value]) => {
      if (value && (isNaN(parseFloat(value)) || parseFloat(value) < 0)) {
        newErrors[`precio_${currency}`] = `El precio en ${currency} no es válido`
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const handlePriceChange = (currency, value) => {
    setFormData(prev => ({
      ...prev,
      precios: { ...prev.precios, [currency]: value }
    }))
    if (errors.precios || errors[`precio_${currency}`]) {
      setErrors(prev => ({ 
        ...prev, 
        precios: '', 
        [`precio_${currency}`]: '' 
      }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      // Convertir precios a números, eliminando los vacíos
      const cleanPrecios = {}
      Object.entries(formData.precios).forEach(([currency, value]) => {
        if (value && parseFloat(value) > 0) {
          cleanPrecios[currency] = parseFloat(value)
        }
      })

      onSubmit({
        ...formData,
        precios: cleanPrecios,
      })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Código */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Código <span className="text-red-400">*</span>
        </label>
        <Input
          name="codigo"
          value={formData.codigo}
          onChange={handleChange}
          placeholder="Ej: PROD-001"
          icon={CodeIcon}
          error={!!errors.codigo}
          disabled={isLoading}
        />
        {errors.codigo && (
          <p className="mt-1.5 text-sm text-red-400">{errors.codigo}</p>
        )}
      </div>

      {/* Nombre */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Nombre del Producto <span className="text-red-400">*</span>
        </label>
        <Input
          name="nombre"
          value={formData.nombre}
          onChange={handleChange}
          placeholder="Nombre del producto"
          icon={ProductIcon}
          error={!!errors.nombre}
          disabled={isLoading}
        />
        {errors.nombre && (
          <p className="mt-1.5 text-sm text-red-400">{errors.nombre}</p>
        )}
      </div>

      {/* Empresa */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Empresa <span className="text-red-400">*</span>
        </label>
        <select
          name="empresa"
          value={formData.empresa}
          onChange={handleChange}
          disabled={isLoading || isEditing}
          className={`
            w-full px-4 py-3.5 rounded-xl
            bg-white/5 backdrop-blur-sm
            border transition-all duration-300
            text-white
            focus:outline-none focus:ring-2
            disabled:opacity-50 disabled:cursor-not-allowed
            ${errors.empresa 
              ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' 
              : 'border-white/10 hover:border-white/20 focus:border-brand-primary focus:ring-brand-primary/20'
            }
          `}
        >
          <option value="" className="bg-slate-900">Seleccionar empresa...</option>
          {empresas.map(emp => (
            <option key={emp.nit} value={emp.nit} className="bg-slate-900">
              {emp.nombre} ({emp.nit})
            </option>
          ))}
        </select>
        {errors.empresa && (
          <p className="mt-1.5 text-sm text-red-400">{errors.empresa}</p>
        )}
      </div>

      {/* Características */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Características <span className="text-red-400">*</span>
        </label>
        <textarea
          name="caracteristicas"
          value={formData.caracteristicas}
          onChange={handleChange}
          placeholder="Descripción y características del producto..."
          rows={3}
          disabled={isLoading}
          className={`
            w-full px-4 py-3.5 rounded-xl
            bg-white/5 backdrop-blur-sm
            border transition-all duration-300
            text-white placeholder-white/40
            focus:outline-none focus:ring-2
            disabled:opacity-50 disabled:cursor-not-allowed
            resize-none
            ${errors.caracteristicas 
              ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' 
              : 'border-white/10 hover:border-white/20 focus:border-brand-primary focus:ring-brand-primary/20'
            }
          `}
        />
        {errors.caracteristicas && (
          <p className="mt-1.5 text-sm text-red-400">{errors.caracteristicas}</p>
        )}
      </div>

      {/* Precios Multi-moneda */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Precios <span className="text-red-400">*</span>
          <span className="text-white/50 font-normal ml-2">(al menos uno)</span>
        </label>
        <div className="grid grid-cols-3 gap-3">
          {Object.keys(formData.precios).map(currency => (
            <div key={currency}>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/50 text-sm">
                  {currencySymbols[currency]}
                </span>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.precios[currency]}
                  onChange={(e) => handlePriceChange(currency, e.target.value)}
                  placeholder="0.00"
                  disabled={isLoading}
                  className={`
                    w-full pl-12 pr-4 py-3 rounded-xl
                    bg-white/5 backdrop-blur-sm
                    border transition-all duration-300
                    text-white placeholder-white/40
                    focus:outline-none focus:ring-2
                    disabled:opacity-50 disabled:cursor-not-allowed
                    ${errors[`precio_${currency}`]
                      ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20'
                      : 'border-white/10 hover:border-white/20 focus:border-brand-primary focus:ring-brand-primary/20'
                    }
                  `}
                />
              </div>
              <p className="mt-1 text-xs text-white/50 text-center">{currency}</p>
              {errors[`precio_${currency}`] && (
                <p className="mt-1 text-xs text-red-400">{errors[`precio_${currency}`]}</p>
              )}
            </div>
          ))}
        </div>
        {errors.precios && (
          <p className="mt-2 text-sm text-red-400">{errors.precios}</p>
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
            isEditing ? 'Actualizar Producto' : 'Crear Producto'
          )}
        </Button>
      </div>
    </form>
  )
}

export default ProductoForm
