import api from './api'

const AUTH_ENDPOINTS = {
  login: '/auth/login/',
  refresh: '/auth/token/refresh/',
}

export const authService = {
  /**
   * Iniciar sesión con email y contraseña
   * @param {string} email 
   * @param {string} password 
   * @returns {Promise<{access: string, refresh: string, user: object}>}
   */
  async login(email, password) {
    const response = await api.post(AUTH_ENDPOINTS.login, { email, password })
    const { access, refresh, user } = response.data

    // Guardar tokens y usuario en localStorage
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user', JSON.stringify(user))

    return response.data
  },

  /**
   * Cerrar sesión - limpiar tokens
   */
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },

  /**
   * Obtener usuario actual del localStorage
   * @returns {object|null}
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  /**
   * Verificar si hay sesión activa
   * @returns {boolean}
   */
  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },

  /**
   * Obtener el token de acceso actual
   * @returns {string|null}
   */
  getAccessToken() {
    return localStorage.getItem('access_token')
  },

  /**
   * Verificar si el usuario es administrador
   * @returns {boolean}
   */
  isAdmin() {
    const user = this.getCurrentUser()
    return user?.is_staff || user?.role === 'admin'
  },
}

export default authService
