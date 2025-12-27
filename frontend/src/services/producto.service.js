/**
 * Servicio para gestionar productos
 * Endpoints: GET, POST, PUT, PATCH, DELETE /api/productos/
 */
import api from './api'

const ENDPOINT = '/productos'

const productoService = {
  /**
   * Obtener todos los productos
   * @param {Object} params - Parámetros de búsqueda, filtro y ordenamiento
   * @returns {Promise<Array>} Lista de productos
   */
  async getAll(params = {}) {
    const response = await api.get(`${ENDPOINT}/`, { params })
    return response.data
  },

  /**
   * Obtener productos por empresa
   * @param {string} empresaNit - NIT de la empresa
   * @returns {Promise<Array>} Lista de productos de la empresa
   */
  async getByEmpresa(empresaNit) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { empresa: empresaNit }
    })
    return response.data
  },

  /**
   * Obtener un producto por ID
   * @param {number} id - ID del producto
   * @returns {Promise<Object>} Datos del producto
   */
  async getById(id) {
    const response = await api.get(`${ENDPOINT}/${id}/`)
    return response.data
  },

  /**
   * Crear un nuevo producto (solo admin)
   * @param {Object} productoData - Datos del producto
   * @returns {Promise<Object>} Producto creado
   */
  async create(productoData) {
    const response = await api.post(`${ENDPOINT}/`, productoData)
    return response.data
  },

  /**
   * Actualizar un producto existente (solo admin)
   * @param {number} id - ID del producto
   * @param {Object} productoData - Datos actualizados
   * @returns {Promise<Object>} Producto actualizado
   */
  async update(id, productoData) {
    const response = await api.put(`${ENDPOINT}/${id}/`, productoData)
    return response.data
  },

  /**
   * Actualizar parcialmente un producto (solo admin)
   * @param {number} id - ID del producto
   * @param {Object} productoData - Datos a actualizar
   * @returns {Promise<Object>} Producto actualizado
   */
  async patch(id, productoData) {
    const response = await api.patch(`${ENDPOINT}/${id}/`, productoData)
    return response.data
  },

  /**
   * Eliminar un producto (solo admin)
   * @param {number} id - ID del producto
   * @returns {Promise<void>}
   */
  async delete(id) {
    await api.delete(`${ENDPOINT}/${id}/`)
  },

  /**
   * Buscar productos por término
   * @param {string} searchTerm - Término de búsqueda
   * @returns {Promise<Array>} Lista de productos filtrados
   */
  async search(searchTerm) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { search: searchTerm }
    })
    return response.data
  }
}

export default productoService
