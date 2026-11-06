import axios from 'axios'

// Grabs the URL from the environment file, defaults to localhost if not found
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  register(userData) {
    return apiClient.post('/auth/register', userData)
  },
  login(credentials) {
    return apiClient.post('/auth/login', credentials)
  },

  getGoogleAuthUrl() {
    return apiClient.get('/auth/google')
  },
 
}