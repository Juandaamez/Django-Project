/**
 * InventarioForm - Formulario para crear/editar registros de inventario
 * Solo disponible para administradores
 */
import { useState, useEffect } from 'react'
import Input from '../atoms/Input'
import Button from '../atoms/Button'
import Spinner from '../atoms/Spinner'

// Iconos SVG inline
const BoxIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
  </svg>
)

const HashIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
  </svg>
)

const initialFormData = {
  producto: '',
  cantidad: '',
}

const InventarioForm = ({
  inventario = null,
  productos = [],
  selectedProductoId = '',
  onSubmit,
  onCancel,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState(initialFormData)
  const [errors, setErrors] = useState({})
  const isEditing = !!inventario

  useEffect(() => {
    if (inventario) {
      setFormData({
        producto: inventario.producto?.id?.toString() || inventario.producto?.toString() || '',
        cantidad: inventario.cantidad?.toString() || '',
      })
    } else {
      setFormData({
        ...initialFormData,
        producto: selectedProductoId?.toString() || '',
      })
    }
    setErrors({})
  }, [inventario, selectedProductoId])

  const validateForm = () => {
    const newErrors = {}

    if (!formData.producto) {
      newErrors.producto = 'Debe seleccionar un producto'
    }

    if (!formData.cantidad && formData.cantidad !== 0) {
      newErrors.cantidad = 'La cantidad es obligatoria'
    } else if (parseInt(formData.cantidad) < 0) {
      newErrors.cantidad = 'La cantidad no puede ser negativa'
    } else if (!Number.isInteger(parseFloat(formData.cantidad))) {
      newErrors.cantidad = 'La cantidad debe ser un número entero'
    }

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

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit({
        producto: parseInt(formData.producto),
        cantidad: parseInt(formData.cantidad),
      })
    }
  }

  // Obtener el producto seleccionado para mostrar información adicional
  const selectedProducto = productos.find(p => p.id?.toString() === formData.producto)

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Producto */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Producto <span className="text-red-400">*</span>
        </label>
        <select
          name="producto"
          value={formData.producto}
          onChange={handleChange}
          disabled={isLoading || isEditing}
          className={`
            w-full px-4 py-3.5 rounded-xl
            bg-white/5 backdrop-blur-sm
            border transition-all duration-300
            text-white
            focus:outline-none focus:ring-2
            disabled:opacity-50 disabled:cursor-not-allowed
            ${errors.producto 
              ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' 
              : 'border-white/10 hover:border-white/20 focus:border-brand-primary focus:ring-brand-primary/20'
            }
          `}
        >
          <option value="" className="bg-slate-900">Seleccionar producto...</option>
          {productos.map(prod => (
            <option key={prod.id} value={prod.id} className="bg-slate-900">
              {prod.codigo} - {prod.nombre} ({prod.empresa_nombre || prod.empresa})
            </option>
          ))}
        </select>
        {errors.producto && (
          <p className="mt-1.5 text-sm text-red-400">{errors.producto}</p>
        )}
        {isEditing && (
          <p className="mt-1.5 text-xs text-white/50">
            El producto no se puede modificar
          </p>
        )}
      </div>

      {/* Info del producto seleccionado */}
      {selectedProducto && (
        <div className="p-4 rounded-xl bg-brand-primary/10 border border-brand-primary/20">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-brand-primary/20">
              <BoxIcon className="w-5 h-5 text-brand-primary" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-white">{selectedProducto.nombre}</h4>
              <p className="text-sm text-white/60 mt-1">
                {selectedProducto.caracteristicas?.substring(0, 100)}
                {selectedProducto.caracteristicas?.length > 100 ? '...' : ''}
              </p>
              {selectedProducto.precios && (
                <div className="flex gap-2 mt-2">
                  {Object.entries(selectedProducto.precios).map(([currency, price]) => (
                    <span key={currency} className="px-2 py-1 rounded-lg bg-white/5 text-xs text-white/70">
                      {currency}: {price.toLocaleString()}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Cantidad */}
      <div>
        <label className="block text-sm font-medium text-white/80 mb-2">
          Cantidad en Stock <span className="text-red-400">*</span>
        </label>
        <Input
          type="number"
          name="cantidad"
          value={formData.cantidad}
          onChange={handleChange}
          placeholder="0"
          icon={HashIcon}
          error={!!errors.cantidad}
          disabled={isLoading}
          min="0"
          step="1"
        />
        {errors.cantidad && (
          <p className="mt-1.5 text-sm text-red-400">{errors.cantidad}</p>
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
            isEditing ? 'Actualizar Inventario' : 'Registrar en Inventario'
          )}
        </Button>
      </div>
    </form>
  )
}

export default InventarioForm
