/**
 * Servicio para gestionar inventarios
 * Endpoints: GET, POST, PUT, PATCH, DELETE /api/inventarios/
 */
import api from './api'

const ENDPOINT = '/inventarios'

const inventarioService = {
  /**
   * Obtener todos los inventarios
   * @param {Object} params - Parámetros de búsqueda, filtro y ordenamiento
   * @returns {Promise<Array>} Lista de inventarios
   */
  async getAll(params = {}) {
    const response = await api.get(`${ENDPOINT}/`, { params })
    return response.data
  },

  /**
   * Obtener inventarios por empresa
   * @param {string} empresaNit - NIT de la empresa
   * @returns {Promise<Array>} Lista de inventarios de la empresa
   */
  async getByEmpresa(empresaNit) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { empresa: empresaNit }
    })
    return response.data
  },

  /**
   * Obtener inventarios por producto
   * @param {string} productoCodigo - Código del producto
   * @returns {Promise<Array>} Lista de inventarios del producto
   */
  async getByProducto(productoCodigo) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { producto: productoCodigo }
    })
    return response.data
  },

  /**
   * Obtener un inventario por ID
   * @param {number} id - ID del inventario
   * @returns {Promise<Object>} Datos del inventario
   */
  async getById(id) {
    const response = await api.get(`${ENDPOINT}/${id}/`)
    return response.data
  },

  /**
   * Crear un nuevo registro de inventario (solo admin)
   * @param {Object} inventarioData - Datos del inventario
   * @returns {Promise<Object>} Inventario creado
   */
  async create(inventarioData) {
    const response = await api.post(`${ENDPOINT}/`, inventarioData)
    return response.data
  },

  /**
   * Actualizar un inventario existente (solo admin)
   * @param {number} id - ID del inventario
   * @param {Object} inventarioData - Datos actualizados
   * @returns {Promise<Object>} Inventario actualizado
   */
  async update(id, inventarioData) {
    const response = await api.put(`${ENDPOINT}/${id}/`, inventarioData)
    return response.data
  },

  /**
   * Actualizar parcialmente un inventario (solo admin)
   * @param {number} id - ID del inventario
   * @param {Object} inventarioData - Datos a actualizar
   * @returns {Promise<Object>} Inventario actualizado
   */
  async patch(id, inventarioData) {
    const response = await api.patch(`${ENDPOINT}/${id}/`, inventarioData)
    return response.data
  },

  /**
   * Eliminar un inventario (solo admin)
   * @param {number} id - ID del inventario
   * @returns {Promise<void>}
   */
  async delete(id) {
    await api.delete(`${ENDPOINT}/${id}/`)
  },

  /**
   * Buscar inventarios por término
   * @param {string} searchTerm - Término de búsqueda
   * @returns {Promise<Array>} Lista de inventarios filtrados
   */
  /**
   * Buscar inventarios por término
   * @param {string} searchTerm - Término de búsqueda
   * @returns {Promise<Array>} Lista de inventarios filtrados
   */
  async search(searchTerm) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { search: searchTerm }
    })
    return response.data
  },

  /**
   * Descargar PDF del inventario desde el servidor
   * @param {string} empresaNit - NIT de la empresa
   * @returns {Promise<Blob>} Blob del PDF
   */
  async descargarPDFServidor(empresaNit) {
    const response = await api.get(`${ENDPOINT}/pdf/${empresaNit}/`, {
      responseType: 'blob'
    })
    return response.data
  },

  /**
   * Enviar PDF del inventario por correo usando la API REST del servidor
   * Incluye opciones avanzadas de IA y Blockchain
   * 
   * @param {string} empresaNit - NIT de la empresa
   * @param {string} emailDestino - Correo de destino
   * @param {string} pdfBase64 - PDF en Base64 (opcional, generado en frontend)
   * @param {boolean} incluirAnalisisIA - Incluir análisis inteligente (default: true)
   * @param {boolean} incluirBlockchain - Incluir certificación blockchain (default: true)
   * @returns {Promise<Object>} Resultado del envío con hash y alertas
   */
  async enviarPorCorreo(empresaNit, emailDestino, pdfBase64 = null, incluirAnalisisIA = true, incluirBlockchain = true) {
    const response = await api.post(`${ENDPOINT}/enviar-correo/`, {
      empresa_nit: empresaNit,
      email_destino: emailDestino,
      pdf_base64: pdfBase64,
      incluir_analisis_ia: incluirAnalisisIA,
      incluir_blockchain: incluirBlockchain
    })
    return response.data
  },

  /**
   * Obtener análisis IA del inventario de una empresa
   * @param {string} empresaNit - NIT de la empresa
   * @returns {Promise<Object>} Análisis completo con alertas y recomendaciones
   */
  async obtenerAnalisis(empresaNit) {
    const response = await api.get(`${ENDPOINT}/analisis/${empresaNit}/`)
    return response.data
  },

  /**
   * Obtener historial de envíos de una empresa
   * @param {string} empresaNit - NIT de la empresa (opcional)
   * @returns {Promise<Array>} Lista de envíos realizados
   */
  async obtenerHistorialEnvios(empresaNit = null) {
    const params = empresaNit ? { empresa: empresaNit } : {}
    const response = await api.get('/historial-envios/', { params })
    return response.data
  }
}

export default inventarioService
