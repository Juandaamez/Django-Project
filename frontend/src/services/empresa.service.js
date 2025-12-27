/**
 * Servicio para gestionar empresas
 * Endpoints: GET, POST, PUT, PATCH, DELETE /api/empresas/
 */
import api from './api'

const ENDPOINT = '/empresas'

const empresaService = {
  /**
   * Obtener todas las empresas (público)
   * @param {Object} params - Parámetros de búsqueda y ordenamiento
   * @returns {Promise<Array>} Lista de empresas
   */
  async getAll(params = {}) {
    const response = await api.get(`${ENDPOINT}/`, { params })
    return response.data
  },

  /**
   * Obtener una empresa por NIT
   * @param {string} nit - NIT de la empresa
   * @returns {Promise<Object>} Datos de la empresa
   */
  async getByNit(nit) {
    const response = await api.get(`${ENDPOINT}/${nit}/`)
    return response.data
  },

  /**
   * Crear una nueva empresa (solo admin)
   * @param {Object} empresaData - Datos de la empresa
   * @returns {Promise<Object>} Empresa creada
   */
  async create(empresaData) {
    const response = await api.post(`${ENDPOINT}/`, empresaData)
    return response.data
  },

  /**
   * Actualizar una empresa existente (solo admin)
   * @param {string} nit - NIT de la empresa
   * @param {Object} empresaData - Datos actualizados
   * @returns {Promise<Object>} Empresa actualizada
   */
  async update(nit, empresaData) {
    const response = await api.put(`${ENDPOINT}/${nit}/`, empresaData)
    return response.data
  },

  /**
   * Actualizar parcialmente una empresa (solo admin)
   * @param {string} nit - NIT de la empresa
   * @param {Object} empresaData - Datos a actualizar
   * @returns {Promise<Object>} Empresa actualizada
   */
  async patch(nit, empresaData) {
    const response = await api.patch(`${ENDPOINT}/${nit}/`, empresaData)
    return response.data
  },

  /**
   * Eliminar una empresa (solo admin)
   * @param {string} nit - NIT de la empresa
   * @returns {Promise<void>}
   */
  async delete(nit) {
    await api.delete(`${ENDPOINT}/${nit}/`)
  },

  /**
   * Buscar empresas por término
   * @param {string} searchTerm - Término de búsqueda
   * @returns {Promise<Array>} Lista de empresas filtradas
   */
  async search(searchTerm) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { search: searchTerm }
    })
    return response.data
  }
}

export default empresaService
