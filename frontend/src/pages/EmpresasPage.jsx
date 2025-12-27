/**
 * EmpresasPage - Página para gestión de empresas y sus productos
 * Pública para visualización, CRUD solo para administradores
 * Admin puede gestionar productos de cada empresa desde aquí
 */
import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import empresaService from '../services/empresa.service'
import productoService from '../services/producto.service'
import NavigationBar from '../components/organisms/NavigationBar'
import EmpresaForm from '../components/organisms/EmpresaForm'
import ProductoForm from '../components/organisms/ProductoForm'
import ConfirmDialog from '../components/molecules/ConfirmDialog'
import AlertMessage from '../components/molecules/AlertMessage'
import Modal from '../components/atoms/Modal'
import Button from '../components/atoms/Button'
import SearchBar from '../components/atoms/SearchBar'
import EmptyState from '../components/atoms/EmptyState'
import Badge from '../components/atoms/Badge'
import IconButton from '../components/atoms/IconButton'
import Spinner from '../components/atoms/Spinner'

// Iconos SVG inline
const PlusIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
  </svg>
)

const EditIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
  </svg>
)

const TrashIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
  </svg>
)

const BuildingIcon = () => (
  <svg className="w-10 h-10 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
  </svg>
)

const BoxIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
  </svg>
)

const ChevronDownIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
  </svg>
)

const ChevronUpIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
  </svg>
)

const EmpresasPage = () => {
  const { isAuthenticated, isAdmin } = useAuth()
  
  // Estados principales
  const [empresas, setEmpresas] = useState([])
  const [filteredEmpresas, setFilteredEmpresas] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)
  
  // Estados para expandir empresa y ver productos
  const [expandedEmpresa, setExpandedEmpresa] = useState(null)
  const [loadingProductos, setLoadingProductos] = useState(false)
  const [empresaProductos, setEmpresaProductos] = useState({})
  
  // Estados para modales
  const [isEmpresaModalOpen, setIsEmpresaModalOpen] = useState(false)
  const [isProductoModalOpen, setIsProductoModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [selectedEmpresa, setSelectedEmpresa] = useState(null)
  const [selectedProducto, setSelectedProducto] = useState(null)
  const [deleteType, setDeleteType] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Cargar empresas y sus productos
  const loadEmpresas = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await empresaService.getAll()
      setEmpresas(data)
      setFilteredEmpresas(data)
      
      // Cargar productos de todas las empresas para mostrar los contadores
      const productosPromises = data.map(empresa => 
        productoService.getByEmpresa(empresa.nit)
          .then(productos => ({ nit: empresa.nit, productos }))
          .catch(() => ({ nit: empresa.nit, productos: [] }))
      )
      
      const productosResults = await Promise.all(productosPromises)
      const productosMap = {}
      productosResults.forEach(({ nit, productos }) => {
        productosMap[nit] = productos
      })
      setEmpresaProductos(productosMap)
    } catch (err) {
      console.error('Error cargando empresas:', err)
      setError('No se pudieron cargar las empresas. Intenta de nuevo.')
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Cargar productos de una empresa
  const loadProductosEmpresa = useCallback(async (empresaNit) => {
    try {
      setLoadingProductos(true)
      const data = await productoService.getByEmpresa(empresaNit)
      setEmpresaProductos(prev => ({ ...prev, [empresaNit]: data }))
    } catch (err) {
      console.error('Error cargando productos:', err)
      setError('No se pudieron cargar los productos de esta empresa.')
    } finally {
      setLoadingProductos(false)
    }
  }, [])

  useEffect(() => {
    loadEmpresas()
  }, [loadEmpresas])

  // Filtrar empresas por búsqueda
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredEmpresas(empresas)
    } else {
      const term = searchTerm.toLowerCase()
      const filtered = empresas.filter(
        empresa =>
          empresa.nit.toLowerCase().includes(term) ||
          empresa.nombre.toLowerCase().includes(term) ||
          empresa.direccion.toLowerCase().includes(term)
      )
      setFilteredEmpresas(filtered)
    }
  }, [searchTerm, empresas])

  // Toggle expandir empresa
  const toggleExpandEmpresa = async (empresa) => {
    if (expandedEmpresa === empresa.nit) {
      setExpandedEmpresa(null)
    } else {
      setExpandedEmpresa(empresa.nit)
      // Solo cargar si no hay productos cargados aún
      if (!empresaProductos[empresa.nit] || empresaProductos[empresa.nit].length === 0) {
        await loadProductosEmpresa(empresa.nit)
      }
    }
  }

  // Handlers para Empresas
  const handleCreateEmpresa = () => {
    setSelectedEmpresa(null)
    setIsEmpresaModalOpen(true)
  }

  const handleEditEmpresa = (empresa) => {
    setSelectedEmpresa(empresa)
    setIsEmpresaModalOpen(true)
  }

  const handleDeleteEmpresa = (empresa) => {
    setSelectedEmpresa(empresa)
    setDeleteType('empresa')
    setIsDeleteModalOpen(true)
  }

  const handleEmpresaSubmit = async (formData) => {
    try {
      setIsSubmitting(true)
      setError(null)

      if (selectedEmpresa) {
        await empresaService.update(selectedEmpresa.nit, formData)
        setSuccessMessage('Empresa actualizada exitosamente')
      } else {
        await empresaService.create(formData)
        setSuccessMessage('Empresa creada exitosamente')
      }

      setIsEmpresaModalOpen(false)
      setSelectedEmpresa(null)
      await loadEmpresas()
    } catch (err) {
      console.error('Error guardando empresa:', err)
      const message = err.response?.data?.detail || 
                      err.response?.data?.nit?.[0] ||
                      'Error al guardar la empresa'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handlers para Productos
  const handleCreateProducto = (empresa) => {
    setSelectedEmpresa(empresa)
    setSelectedProducto(null)
    setIsProductoModalOpen(true)
  }

  const handleEditProducto = (producto, empresa) => {
    setSelectedEmpresa(empresa)
    setSelectedProducto(producto)
    setIsProductoModalOpen(true)
  }

  const handleDeleteProducto = (producto) => {
    setSelectedProducto(producto)
    setDeleteType('producto')
    setIsDeleteModalOpen(true)
  }

  const handleProductoSubmit = async (formData) => {
    try {
      setIsSubmitting(true)
      setError(null)

      if (selectedProducto) {
        await productoService.update(selectedProducto.id, formData)
        setSuccessMessage('Producto actualizado exitosamente')
      } else {
        await productoService.create(formData)
        setSuccessMessage('Producto creado exitosamente')
      }

      setIsProductoModalOpen(false)
      setSelectedProducto(null)
      if (selectedEmpresa) {
        await loadProductosEmpresa(selectedEmpresa.nit)
      }
    } catch (err) {
      console.error('Error guardando producto:', err)
      const message = err.response?.data?.detail || 
                      err.response?.data?.codigo?.[0] ||
                      'Error al guardar el producto'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Confirmar eliminación
  const handleConfirmDelete = async () => {
    try {
      setIsSubmitting(true)

      if (deleteType === 'empresa' && selectedEmpresa) {
        await empresaService.delete(selectedEmpresa.nit)
        setSuccessMessage(`Empresa "${selectedEmpresa.nombre}" eliminada exitosamente`)
        await loadEmpresas()
      } else if (deleteType === 'producto' && selectedProducto) {
        await productoService.delete(selectedProducto.id)
        setSuccessMessage(`Producto "${selectedProducto.nombre}" eliminado exitosamente`)
        if (selectedProducto.empresa) {
          await loadProductosEmpresa(selectedProducto.empresa)
        }
      }

      setIsDeleteModalOpen(false)
      setSelectedEmpresa(null)
      setSelectedProducto(null)
      setDeleteType(null)
    } catch (err) {
      console.error('Error eliminando:', err)
      if (deleteType === 'empresa') {
        setError('No se pudo eliminar la empresa. Puede tener productos asociados.')
      } else {
        setError('No se pudo eliminar el producto.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  // Limpiar mensajes automáticamente
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 4000)
      return () => clearTimeout(timer)
    }
  }, [successMessage])

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <NavigationBar />

      <div className="relative isolate overflow-hidden bg-grid px-6 pb-24 pt-24 sm:px-12">
        <div
          className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-gradient-to-br from-brand-primary/30 via-brand-secondary/20 to-slate-900 blur-3xl"
          aria-hidden="true"
        />

        <div className="mx-auto max-w-6xl">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-2 text-sm text-white/60 mb-2">
              <Link to="/" className="hover:text-white transition-colors">Inicio</Link>
              <span>/</span>
              <span className="text-brand-primary">Empresas</span>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-display font-bold text-white">
                  Gestión de Empresas
                </h1>
                <p className="text-white/60 mt-1">
                  {isAuthenticated 
                    ? isAdmin 
                      ? 'Administra empresas y sus productos' 
                      : 'Consulta las empresas registradas'
                    : 'Directorio de empresas'}
                </p>
              </div>

              {isAdmin && (
                <Button onClick={handleCreateEmpresa} className="flex items-center gap-2">
                  <PlusIcon />
                  Nueva Empresa
                </Button>
              )}
            </div>
          </div>

          {/* Mensajes */}
          {error && (
            <AlertMessage type="error" message={error} onDismiss={() => setError(null)} className="mb-6" />
          )}
          {successMessage && (
            <AlertMessage type="success" message={successMessage} onDismiss={() => setSuccessMessage(null)} className="mb-6" />
          )}

          {/* Info banner para usuarios no autenticados */}
          {!isAuthenticated && (
            <div className="mb-6 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-blue-500/20">
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-blue-400">Modo visitante</h3>
                  <p className="text-sm text-white/60 mt-1">
                    Estás viendo las empresas como visitante.{' '}
                    <Link to="/login" className="text-brand-primary hover:underline">Inicia sesión</Link>{' '}
                    como administrador para gestionar empresas y productos.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Barra de búsqueda */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <SearchBar
              value={searchTerm}
              onChange={setSearchTerm}
              placeholder="Buscar por NIT, nombre o dirección..."
              className="flex-1"
            />
            <div className="flex items-center gap-4">
              <div className="px-4 py-2 rounded-xl bg-white/5 border border-white/10">
                <span className="text-white/60 text-sm">Total:</span>
                <span className="ml-2 font-bold text-brand-primary">{filteredEmpresas.length}</span>
              </div>
            </div>
          </div>

          {/* Lista de empresas */}
          {isLoading ? (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <Spinner size="lg" className="text-brand-primary mx-auto mb-4" />
                <p className="text-white/60">Cargando empresas...</p>
              </div>
            </div>
          ) : filteredEmpresas.length === 0 ? (
            <EmptyState
              icon={<BuildingIcon />}
              title={searchTerm ? 'Sin resultados' : 'No hay empresas'}
              description={
                searchTerm
                  ? `No se encontraron empresas que coincidan con "${searchTerm}"`
                  : 'Aún no hay empresas registradas en el sistema'
              }
              action={
                isAdmin && !searchTerm && (
                  <Button onClick={handleCreateEmpresa} className="flex items-center gap-2">
                    <PlusIcon />
                    Crear primera empresa
                  </Button>
                )
              }
            />
          ) : (
            <div className="space-y-4">
              {filteredEmpresas.map((empresa) => (
                <div
                  key={empresa.nit}
                  className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm overflow-hidden"
                >
                  {/* Header de la empresa */}
                  <div className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-4">
                        <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-brand-primary/20 to-brand-secondary/20 flex items-center justify-center flex-shrink-0">
                          <span className="text-xl font-bold text-brand-primary">
                            {empresa.nombre.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h3 className="text-lg font-display font-bold text-white">{empresa.nombre}</h3>
                          <Badge variant="primary" size="sm" className="mt-1">NIT: {empresa.nit}</Badge>
                          <div className="mt-2 space-y-1 text-sm text-white/60">
                            <p className="flex items-center gap-2">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                              </svg>
                              {empresa.direccion}
                            </p>
                            <p className="flex items-center gap-2">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                              </svg>
                              {empresa.telefono}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Acciones */}
                      <div className="flex items-center gap-2">
                        {isAdmin && (
                          <>
                            <IconButton onClick={() => handleEditEmpresa(empresa)} variant="primary" title="Editar empresa">
                              <EditIcon />
                            </IconButton>
                            <IconButton onClick={() => handleDeleteEmpresa(empresa)} variant="danger" title="Eliminar empresa">
                              <TrashIcon />
                            </IconButton>
                          </>
                        )}
                        <button
                          onClick={() => toggleExpandEmpresa(empresa)}
                          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-white/70 hover:text-white hover:bg-white/10 transition-all"
                        >
                          <BoxIcon />
                          <span className="text-sm font-medium">
                            Productos ({empresaProductos[empresa.nit]?.length || 0})
                          </span>
                          {expandedEmpresa === empresa.nit ? <ChevronUpIcon /> : <ChevronDownIcon />}
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Productos expandibles */}
                  {expandedEmpresa === empresa.nit && (
                    <div className="border-t border-white/10 bg-slate-900/50">
                      <div className="p-6">
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="font-medium text-white flex items-center gap-2">
                            <BoxIcon />
                            Productos de {empresa.nombre}
                          </h4>
                          {isAdmin && (
                            <Button size="sm" onClick={() => handleCreateProducto(empresa)} className="flex items-center gap-2">
                              <PlusIcon />
                              Agregar Producto
                            </Button>
                          )}
                        </div>

                        {loadingProductos && !empresaProductos[empresa.nit] ? (
                          <div className="flex items-center justify-center py-8">
                            <Spinner size="md" className="text-brand-primary" />
                          </div>
                        ) : empresaProductos[empresa.nit]?.length > 0 ? (
                          <div className="overflow-x-auto">
                            <table className="w-full">
                              <thead>
                                <tr className="border-b border-white/10">
                                  <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Código</th>
                                  <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Nombre</th>
                                  <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Características</th>
                                  <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Precios</th>
                                  {isAdmin && (
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-white/70 uppercase tracking-wider">Acciones</th>
                                  )}
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-white/5">
                                {empresaProductos[empresa.nit].map((producto) => (
                                  <tr key={producto.id} className="hover:bg-white/5 transition-colors">
                                    <td className="px-4 py-3">
                                      <span className="font-mono text-brand-primary">{producto.codigo}</span>
                                    </td>
                                    <td className="px-4 py-3 font-medium text-white">{producto.nombre}</td>
                                    <td className="px-4 py-3 text-white/70 text-sm max-w-xs truncate">{producto.caracteristicas}</td>
                                    <td className="px-4 py-3">
                                      <div className="flex flex-wrap gap-1">
                                        {producto.precios && Object.entries(producto.precios).map(([currency, price]) => (
                                          <Badge key={currency} variant="default" size="sm">
                                            {currency}: {typeof price === 'number' ? price.toLocaleString() : price}
                                          </Badge>
                                        ))}
                                      </div>
                                    </td>
                                    {isAdmin && (
                                      <td className="px-4 py-3 text-right">
                                        <div className="flex items-center justify-end gap-1">
                                          <IconButton onClick={() => handleEditProducto(producto, empresa)} variant="primary" title="Editar">
                                            <EditIcon />
                                          </IconButton>
                                          <IconButton onClick={() => handleDeleteProducto(producto)} variant="danger" title="Eliminar">
                                            <TrashIcon />
                                          </IconButton>
                                        </div>
                                      </td>
                                    )}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        ) : (
                          <div className="text-center py-8">
                            <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto mb-4">
                              <BoxIcon />
                            </div>
                            <p className="text-white/60">Esta empresa no tiene productos registrados</p>
                            {isAdmin && (
                              <Button size="sm" onClick={() => handleCreateProducto(empresa)} className="mt-4 flex items-center gap-2 mx-auto">
                                <PlusIcon />
                                Agregar primer producto
                              </Button>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal de Empresa */}
      <Modal
        isOpen={isEmpresaModalOpen}
        onClose={() => !isSubmitting && setIsEmpresaModalOpen(false)}
        title={selectedEmpresa && !selectedProducto ? 'Editar Empresa' : 'Nueva Empresa'}
        size="md"
      >
        <EmpresaForm
          empresa={selectedEmpresa}
          onSubmit={handleEmpresaSubmit}
          onCancel={() => setIsEmpresaModalOpen(false)}
          isLoading={isSubmitting}
        />
      </Modal>

      {/* Modal de Producto */}
      <Modal
        isOpen={isProductoModalOpen}
        onClose={() => !isSubmitting && setIsProductoModalOpen(false)}
        title={selectedProducto ? 'Editar Producto' : `Nuevo Producto - ${selectedEmpresa?.nombre || ''}`}
        size="lg"
      >
        <ProductoForm
          producto={selectedProducto}
          empresas={empresas}
          selectedEmpresaNit={selectedEmpresa?.nit || ''}
          onSubmit={handleProductoSubmit}
          onCancel={() => setIsProductoModalOpen(false)}
          isLoading={isSubmitting}
        />
      </Modal>

      {/* Modal de confirmación */}
      <ConfirmDialog
        isOpen={isDeleteModalOpen}
        onClose={() => !isSubmitting && setIsDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
        title={deleteType === 'empresa' ? 'Eliminar Empresa' : 'Eliminar Producto'}
        message={
          deleteType === 'empresa'
            ? `¿Eliminar la empresa "${selectedEmpresa?.nombre}"? Se eliminarán todos sus productos.`
            : `¿Eliminar el producto "${selectedProducto?.nombre}"?`
        }
        confirmText="Eliminar"
        variant="danger"
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default EmpresasPage
