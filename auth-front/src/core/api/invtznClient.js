import axios from 'axios';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useToast } from "vue-toastification"; 

const invtznClient = axios.create({
  baseURL: 'http://api.invtzn.local/api/v1/', // Dominio del Ecosistema Core
  headers: { 'Content-Type': 'application/json' }
});

const toast = useToast(); 

// Interceptor de Petición: Inyección de JWT
invtznClient.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Interceptor de Respuesta: Manejo Global de errores y Renovación Silenciosa 
invtznClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const toast = useToast();
    
    if (!error.response) {
      toast.error('Error de red. Verifica tu conexión a internet.');
      return Promise.reject(error);
    }

    const originalRequest = error.config;
    const authStore = useAuthStore();
    const status = error.response.status;

    if (status >= 500) {
      toast.error('Error interno del servidor. Inténtalo más tarde.');
    } else if (status === 403) {
      toast.warning('No tienes permisos para realizar esta acción.');
    } else if (status === 404) {
      toast.info('El recurso que buscas no existe.');
    }

    // Renovación Silenciosa
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshResponse = await axios.post('http://api.auth.local/auth/token/refresh/', {
          refresh: authStore.refreshToken
        });

        const newAccess = refreshResponse.data.access;
        authStore.token = newAccess;

        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return invtznClient(originalRequest);
      } catch (refreshError) {
        toast.error('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
        authStore.logout();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default invtznClient;
