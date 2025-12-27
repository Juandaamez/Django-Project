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
  async search(searchTerm) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { search: searchTerm }
    })
    return response.data
  }
}

export default inventarioService
