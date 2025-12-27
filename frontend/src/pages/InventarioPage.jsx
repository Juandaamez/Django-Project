/**
 * InventarioPage - Vista de inventario por empresa
 * Muestra empresas con sus productos (inventario) y opciones de exportar PDF/enviar correo
 */
import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import empresaService from '../services/empresa.service'
import inventarioService from '../services/inventario.service'
import { descargarPDFInventario, obtenerPDFBase64 } from '../services/pdfGenerator'
import NavigationBar from '../components/organisms/NavigationBar'
import InventarioForm from '../components/organisms/InventarioForm'
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
const DownloadIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
)

const MailIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
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

const PlusIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
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

const InventarioPage = () => {
  const { isAdmin } = useAuth()
  
  // Estados principales
  const [empresas, setEmpresas] = useState([])
  const [filteredEmpresas, setFilteredEmpresas] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)
  
  // Estados para expandir empresa y ver inventario
  const [expandedEmpresa, setExpandedEmpresa] = useState(null)
  const [loadingInventario, setLoadingInventario] = useState(false)
  const [empresaInventarios, setEmpresaInventarios] = useState({})
  const [empresaProductos, setEmpresaProductos] = useState({})
  
  // Estados para modales
  const [isInventarioModalOpen, setIsInventarioModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [selectedEmpresa, setSelectedEmpresa] = useState(null)
  const [selectedInventario, setSelectedInventario] = useState(null)
  const [emailDestino, setEmailDestino] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isPDFGenerating, setIsPDFGenerating] = useState(false)
  const [isSendingEmail, setIsSendingEmail] = useState(false)
  
  // Estados para opciones avanzadas de email
  const [incluirAnalisisIA, setIncluirAnalisisIA] = useState(true)
  const [incluirBlockchain, setIncluirBlockchain] = useState(true)
  const [emailResponse, setEmailResponse] = useState(null)

  // Cargar empresas
  const loadEmpresas = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await empresaService.getAll()
      setEmpresas(data)
      setFilteredEmpresas(data)
    } catch (err) {
      console.error('Error cargando empresas:', err)
      setError('No se pudieron cargar las empresas. Intenta de nuevo.')
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Cargar inventario de una empresa
  const loadInventarioEmpresa = useCallback(async (empresaNit) => {
    try {
      setLoadingInventario(true)
      const data = await inventarioService.getByEmpresa(empresaNit)
      setEmpresaInventarios(prev => ({ ...prev, [empresaNit]: data }))
    } catch (err) {
      console.error('Error cargando inventario:', err)
      setError('No se pudo cargar el inventario de esta empresa.')
    } finally {
      setLoadingInventario(false)
    }
  }, [])

  // Cargar productos de una empresa para el formulario
  const loadProductosEmpresa = useCallback(async (empresaNit) => {
    try {
      const { default: productoService } = await import('../services/producto.service')
      const data = await productoService.getByEmpresa(empresaNit)
      setEmpresaProductos(prev => ({ ...prev, [empresaNit]: data }))
    } catch (err) {
      console.error('Error cargando productos:', err)
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
          empresa.nombre.toLowerCase().includes(term)
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
      if (!empresaInventarios[empresa.nit]) {
        await loadInventarioEmpresa(empresa.nit)
      }
      if (!empresaProductos[empresa.nit]) {
        await loadProductosEmpresa(empresa.nit)
      }
    }
  }

  // Handlers para Inventario
  const handleAddInventario = (empresa) => {
    setSelectedEmpresa(empresa)
    setSelectedInventario(null)
    setIsInventarioModalOpen(true)
  }

  const handleEditInventario = (inventario, empresa) => {
    setSelectedEmpresa(empresa)
    setSelectedInventario(inventario)
    setIsInventarioModalOpen(true)
  }

  const handleDeleteInventario = (inventario) => {
    setSelectedInventario(inventario)
    setIsDeleteModalOpen(true)
  }

  const handleInventarioSubmit = async (formData) => {
    try {
      setIsSubmitting(true)
      setError(null)

      if (selectedInventario) {
        await inventarioService.update(selectedInventario.id, formData)
        setSuccessMessage('Stock actualizado exitosamente')
      } else {
        await inventarioService.create(formData)
        setSuccessMessage('Producto agregado al inventario exitosamente')
      }

      setIsInventarioModalOpen(false)
      setSelectedInventario(null)
      if (selectedEmpresa) {
        await loadInventarioEmpresa(selectedEmpresa.nit)
      }
    } catch (err) {
      console.error('Error guardando inventario:', err)
      const message = err.response?.data?.detail || 'Error al guardar el inventario'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleConfirmDelete = async () => {
    try {
      setIsSubmitting(true)
      await inventarioService.delete(selectedInventario.id)
      setSuccessMessage('Registro eliminado del inventario')
      setIsDeleteModalOpen(false)
      setSelectedInventario(null)
      if (expandedEmpresa) {
        await loadInventarioEmpresa(expandedEmpresa)
      }
    } catch (err) {
      console.error('Error eliminando inventario:', err)
      setError('No se pudo eliminar el registro.')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handlers para PDF y Email
  const handleDownloadPDF = async (empresa) => {
    try {
      setIsPDFGenerating(true)
      setError(null)
      
      // Obtener inventarios de la empresa si no los tenemos
      let inventarios = empresaInventarios[empresa.nit]
      if (!inventarios) {
        inventarios = await inventarioService.getByEmpresa(empresa.nit)
        setEmpresaInventarios(prev => ({ ...prev, [empresa.nit]: inventarios }))
      }
      
      // Generar PDF en el frontend con diseño profesional
      const fileName = descargarPDFInventario(empresa, inventarios)
      setSuccessMessage(`📄 PDF generado exitosamente: ${fileName}`)
    } catch (err) {
      console.error('Error generando PDF:', err)
      setError('No se pudo generar el PDF. Intenta de nuevo.')
    } finally {
      setIsPDFGenerating(false)
    }
  }

  const handleOpenEmailModal = (empresa) => {
    setSelectedEmpresa(empresa)
    setEmailDestino('')
    setEmailResponse(null)
    setIncluirAnalisisIA(true)
    setIncluirBlockchain(true)
    setIsEmailModalOpen(true)
  }

  const handleSendEmail = async () => {
    if (!emailDestino || !emailDestino.includes('@')) {
      setError('Por favor ingresa un correo válido')
      return
    }
    
    try {
      setIsSendingEmail(true)
      setError(null)
      setEmailResponse(null)
      
      // Obtener inventarios de la empresa si no los tenemos
      let inventarios = empresaInventarios[selectedEmpresa.nit]
      if (!inventarios) {
        inventarios = await inventarioService.getByEmpresa(selectedEmpresa.nit)
        setEmpresaInventarios(prev => ({ ...prev, [selectedEmpresa.nit]: inventarios }))
      }
      
      // Generar PDF en Base64 para enviar al servidor
      const pdfBase64 = obtenerPDFBase64(selectedEmpresa, inventarios)
      
      // Enviar correo via API REST del servidor con opciones avanzadas
      const resultado = await inventarioService.enviarPorCorreo(
        selectedEmpresa.nit,
        emailDestino,
        pdfBase64,
        incluirAnalisisIA,
        incluirBlockchain
      )
      
      if (resultado.success) {
        setEmailResponse(resultado)
        setSuccessMessage(`📧 Correo enviado exitosamente a ${emailDestino}${resultado.hash_documento ? ' (Certificado Blockchain)' : ''}${resultado.alertas_count > 0 ? ` - ${resultado.alertas_count} alertas IA` : ''}`)
        setIsEmailModalOpen(false)
        setEmailDestino('')
      } else {
        throw new Error(resultado.error || 'Error al enviar el correo')
      }
    } catch (err) {
      console.error('Error enviando correo:', err)
      const errorMsg = err.response?.data?.error || err.response?.data?.suggestion || err.message || 'Error al enviar el correo'
      setError(`${errorMsg}. Puedes descargar el PDF y enviarlo manualmente.`)
    } finally {
      setIsSendingEmail(false)
    }
  }

  // Limpiar mensajes
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 4000)
      return () => clearTimeout(timer)
    }
  }, [successMessage])

  // Calcular total de items en inventario
  const getTotalItems = (inventarios) => {
    if (!inventarios) return 0
    return inventarios.reduce((sum, inv) => sum + (inv.cantidad || 0), 0)
  }

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
              <span className="text-brand-primary">Inventario</span>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-display font-bold text-white">
                  📦 Inventario por Empresa
                </h1>
                <p className="text-white/60 mt-1">
                  Consulta el inventario de cada empresa, descarga PDF o envía por correo
                </p>
              </div>
            </div>
          </div>

          {/* Mensajes */}
          {error && (
            <AlertMessage type="error" message={error} onDismiss={() => setError(null)} className="mb-6" />
          )}
          {successMessage && (
            <AlertMessage type="success" message={successMessage} onDismiss={() => setSuccessMessage(null)} className="mb-6" />
          )}

          {/* Barra de búsqueda */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <SearchBar
              value={searchTerm}
              onChange={setSearchTerm}
              placeholder="Buscar empresa por NIT o nombre..."
              className="flex-1"
            />
            <div className="flex items-center gap-4">
              <div className="px-4 py-2 rounded-xl bg-white/5 border border-white/10">
                <span className="text-white/60 text-sm">Empresas:</span>
                <span className="ml-2 font-bold text-brand-primary">{filteredEmpresas.length}</span>
              </div>
            </div>
          </div>

          {/* Lista de empresas con inventario */}
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
                  : 'No hay empresas registradas para mostrar inventario'
              }
            />
          ) : (
            <div className="space-y-4">
              {filteredEmpresas.map((empresa) => {
                const inventarios = empresaInventarios[empresa.nit]
                const totalItems = getTotalItems(inventarios)
                
                return (
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
                            <p className="mt-2 text-sm text-white/60">{empresa.direccion}</p>
                          </div>
                        </div>

                        {/* Acciones principales */}
                        <div className="flex items-center gap-2">
                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => handleDownloadPDF(empresa)}
                            className="flex items-center gap-2"
                            title="Descargar PDF"
                            disabled={isPDFGenerating}
                          >
                            {isPDFGenerating ? (
                              <Spinner size="sm" className="text-brand-primary" />
                            ) : (
                              <DownloadIcon />
                            )}
                            <span className="hidden sm:inline">PDF</span>
                          </Button>
                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => handleOpenEmailModal(empresa)}
                            className="flex items-center gap-2"
                            title="Enviar por correo"
                          >
                            <MailIcon />
                            <span className="hidden sm:inline">Enviar</span>
                          </Button>
                          <button
                            onClick={() => toggleExpandEmpresa(empresa)}
                            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-primary/10 border border-brand-primary/20 text-brand-primary hover:bg-brand-primary/20 transition-all"
                          >
                            <BoxIcon />
                            <span className="text-sm font-medium">
                              Ver Inventario
                            </span>
                            {expandedEmpresa === empresa.nit ? <ChevronUpIcon /> : <ChevronDownIcon />}
                          </button>
                        </div>
                      </div>

                      {/* Stats resumidas */}
                      {inventarios && (
                        <div className="mt-4 flex gap-4">
                          <div className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                            <span className="text-xs text-white/50">Productos:</span>
                            <span className="ml-2 text-sm font-medium text-white">{inventarios.length}</span>
                          </div>
                          <div className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                            <span className="text-xs text-white/50">Total items:</span>
                            <span className="ml-2 text-sm font-medium text-white">{totalItems.toLocaleString()}</span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Inventario expandible */}
                    {expandedEmpresa === empresa.nit && (
                      <div className="border-t border-white/10 bg-slate-900/50">
                        <div className="p-6">
                          <div className="flex items-center justify-between mb-4">
                            <h4 className="font-medium text-white flex items-center gap-2">
                              <BoxIcon />
                              Inventario de {empresa.nombre}
                            </h4>
                            {isAdmin && (
                              <Button size="sm" onClick={() => handleAddInventario(empresa)} className="flex items-center gap-2">
                                <PlusIcon />
                                Agregar al Inventario
                              </Button>
                            )}
                          </div>

                          {loadingInventario && !inventarios ? (
                            <div className="flex items-center justify-center py-8">
                              <Spinner size="md" className="text-brand-primary" />
                            </div>
                          ) : inventarios?.length > 0 ? (
                            <div className="overflow-x-auto">
                              <table className="w-full">
                                <thead>
                                  <tr className="border-b border-white/10">
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Código</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Producto</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Cantidad</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-white/70 uppercase tracking-wider">Última Actualización</th>
                                    {isAdmin && (
                                      <th className="px-4 py-3 text-right text-xs font-semibold text-white/70 uppercase tracking-wider">Acciones</th>
                                    )}
                                  </tr>
                                </thead>
                                <tbody className="divide-y divide-white/5">
                                  {inventarios.map((inv) => (
                                    <tr key={inv.id} className="hover:bg-white/5 transition-colors">
                                      <td className="px-4 py-3">
                                        <span className="font-mono text-brand-primary">{inv.producto_codigo}</span>
                                      </td>
                                      <td className="px-4 py-3 font-medium text-white">{inv.producto_nombre}</td>
                                      <td className="px-4 py-3">
                                        <Badge 
                                          variant={inv.cantidad > 10 ? 'success' : inv.cantidad > 0 ? 'warning' : 'danger'}
                                          size="md"
                                        >
                                          {inv.cantidad} unidades
                                        </Badge>
                                      </td>
                                      <td className="px-4 py-3 text-white/60 text-sm">
                                        {inv.fecha_actualizacion 
                                          ? new Date(inv.fecha_actualizacion).toLocaleDateString('es-CO', {
                                              day: '2-digit',
                                              month: 'short',
                                              year: 'numeric',
                                            })
                                          : '-'}
                                      </td>
                                      {isAdmin && (
                                        <td className="px-4 py-3 text-right">
                                          <div className="flex items-center justify-end gap-1">
                                            <IconButton onClick={() => handleEditInventario(inv, empresa)} variant="primary" title="Editar">
                                              <EditIcon />
                                            </IconButton>
                                            <IconButton onClick={() => handleDeleteInventario(inv)} variant="danger" title="Eliminar">
                                              <TrashIcon />
                                            </IconButton>
                                          </div>
                                        </td>
                                      )}
                                    </tr>
                                  ))}
                                </tbody>
                                <tfoot>
                                  <tr className="border-t border-white/10 bg-white/5">
                                    <td colSpan={2} className="px-4 py-3 font-medium text-white">Total</td>
                                    <td className="px-4 py-3">
                                      <Badge variant="info" size="md">
                                        {totalItems.toLocaleString()} unidades
                                      </Badge>
                                    </td>
                                    <td colSpan={isAdmin ? 2 : 1}></td>
                                  </tr>
                                </tfoot>
                              </table>
                            </div>
                          ) : (
                            <div className="text-center py-8">
                              <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto mb-4">
                                <BoxIcon />
                              </div>
                              <p className="text-white/60">Esta empresa no tiene inventario registrado</p>
                              {isAdmin && (
                                <Button size="sm" onClick={() => handleAddInventario(empresa)} className="mt-4 flex items-center gap-2 mx-auto">
                                  <PlusIcon />
                                  Agregar primer producto al inventario
                                </Button>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>

      {/* Modal de Inventario */}
      <Modal
        isOpen={isInventarioModalOpen}
        onClose={() => !isSubmitting && setIsInventarioModalOpen(false)}
        title={selectedInventario ? 'Editar Stock' : `Agregar al Inventario - ${selectedEmpresa?.nombre || ''}`}
        size="md"
      >
        <InventarioForm
          inventario={selectedInventario}
          productos={empresaProductos[selectedEmpresa?.nit] || []}
          selectedProductoId={selectedInventario?.producto}
          onSubmit={handleInventarioSubmit}
          onCancel={() => setIsInventarioModalOpen(false)}
          isLoading={isSubmitting}
        />
      </Modal>

      {/* Modal de Email */}
      <Modal
        isOpen={isEmailModalOpen}
        onClose={() => !isSendingEmail && setIsEmailModalOpen(false)}
        title={`📧 Enviar Inventario - ${selectedEmpresa?.nombre || ''}`}
        size="md"
      >
        <div className="space-y-5">
          <p className="text-white/70">
            El inventario de <strong className="text-white">{selectedEmpresa?.nombre}</strong> se generará en PDF y se enviará al correo indicado.
          </p>
          
          {/* Correo de destino */}
          <div>
            <label className="block text-sm font-medium text-white/80 mb-2">
              Correo de destino
            </label>
            <input
              type="email"
              value={emailDestino}
              onChange={(e) => setEmailDestino(e.target.value)}
              placeholder="correo@ejemplo.com"
              disabled={isSendingEmail}
              className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/40 focus:outline-none focus:border-brand-primary focus:ring-2 focus:ring-brand-primary/20 disabled:opacity-50"
            />
          </div>
          
          {/* Opciones avanzadas */}
          <div className="p-4 rounded-xl bg-slate-800/50 border border-white/10">
            <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
              <span>⚙️</span> Opciones Avanzadas
            </h4>
            <div className="space-y-3">
              {/* Análisis IA */}
              <label className="flex items-center gap-3 cursor-pointer group">
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={incluirAnalisisIA}
                    onChange={(e) => setIncluirAnalisisIA(e.target.checked)}
                    disabled={isSendingEmail}
                    className="sr-only peer"
                  />
                  <div className="w-10 h-5 bg-white/10 rounded-full peer-checked:bg-emerald-500/50 transition-colors"></div>
                  <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white/40 rounded-full peer-checked:translate-x-5 peer-checked:bg-emerald-400 transition-all"></div>
                </div>
                <div className="flex-1">
                  <span className="text-sm font-medium text-white/90 group-hover:text-white">🤖 Análisis Inteligente (IA)</span>
                  <p className="text-xs text-white/50">Incluir alertas y recomendaciones automáticas</p>
                </div>
              </label>
              
              {/* Certificación Blockchain */}
              <label className="flex items-center gap-3 cursor-pointer group">
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={incluirBlockchain}
                    onChange={(e) => setIncluirBlockchain(e.target.checked)}
                    disabled={isSendingEmail}
                    className="sr-only peer"
                  />
                  <div className="w-10 h-5 bg-white/10 rounded-full peer-checked:bg-indigo-500/50 transition-colors"></div>
                  <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white/40 rounded-full peer-checked:translate-x-5 peer-checked:bg-indigo-400 transition-all"></div>
                </div>
                <div className="flex-1">
                  <span className="text-sm font-medium text-white/90 group-hover:text-white">⛓️ Certificación Blockchain</span>
                  <p className="text-xs text-white/50">Hash SHA-256 para verificación de autenticidad</p>
                </div>
              </label>
            </div>
          </div>
          
          {/* Preview de características */}
          {(incluirAnalisisIA || incluirBlockchain) && (
            <div className="flex flex-wrap gap-2">
              {incluirAnalisisIA && (
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-xs text-emerald-400">
                  🤖 IA Activa
                </span>
              )}
              {incluirBlockchain && (
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs text-indigo-400">
                  ⛓️ Blockchain
                </span>
              )}
            </div>
          )}
          
          <div className="flex gap-3 pt-2">
            <Button 
              variant="ghost" 
              onClick={() => setIsEmailModalOpen(false)} 
              className="flex-1"
              disabled={isSendingEmail}
            >
              Cancelar
            </Button>
            <Button 
              onClick={handleSendEmail} 
              className="flex-1 flex items-center justify-center gap-2"
              disabled={isSendingEmail || !emailDestino}
            >
              {isSendingEmail ? (
                <>
                  <Spinner size="sm" />
                  Enviando...
                </>
              ) : (
                <>
                  <MailIcon />
                  Enviar Reporte
                </>
              )}
            </Button>
          </div>
        </div>
      </Modal>

      {/* Modal de confirmación */}
      <ConfirmDialog
        isOpen={isDeleteModalOpen}
        onClose={() => !isSubmitting && setIsDeleteModalOpen(false)}
        onConfirm={handleConfirmDelete}
        title="Eliminar del Inventario"
        message={`¿Eliminar "${selectedInventario?.producto_nombre}" del inventario?`}
        confirmText="Eliminar"
        variant="danger"
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default InventarioPage
