import api from './api'

const ENDPOINT = '/inventarios'

const inventarioService = {
  async getAll(params = {}) {
    const response = await api.get(`${ENDPOINT}/`, { params })
    return response.data
  },

  async getByEmpresa(empresaNit) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { empresa: empresaNit }
    })
    return response.data
  },

  async getByProducto(productoCodigo) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { producto: productoCodigo }
    })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`${ENDPOINT}/${id}/`)
    return response.data
  },

  async create(inventarioData) {
    const response = await api.post(`${ENDPOINT}/`, inventarioData)
    return response.data
  },

  async update(id, inventarioData) {
    const response = await api.put(`${ENDPOINT}/${id}/`, inventarioData)
    return response.data
  },

  async patch(id, inventarioData) {
    const response = await api.patch(`${ENDPOINT}/${id}/`, inventarioData)
    return response.data
  },

  async delete(id) {
    await api.delete(`${ENDPOINT}/${id}/`)
  },

  async search(searchTerm) {
    const response = await api.get(`${ENDPOINT}/`, {
      params: { search: searchTerm }
    })
    return response.data
  },

  async descargarPDFServidor(empresaNit) {
    const response = await api.get(`${ENDPOINT}/pdf/${empresaNit}/`, {
      responseType: 'blob'
    })
    return response.data
  },

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

  async obtenerAnalisis(empresaNit) {
    const response = await api.get(`${ENDPOINT}/analisis/${empresaNit}/`)
    return response.data
  },

  async obtenerHistorialEnvios(empresaNit = null) {
    const params = empresaNit ? { empresa: empresaNit } : {}
    const response = await api.get('/historial-envios/', { params })
    return response.data
  }
}

export default inventarioService
