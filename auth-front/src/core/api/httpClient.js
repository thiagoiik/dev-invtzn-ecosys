import axios from 'axios';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useToast } from "vue-toastification"; 

const httpClient = axios.create({
  baseURL: 'http://api.auth.local/', // Dominio
  headers: { 'Content-Type': 'application/json' }
});


// const toast = useToast(); // Eliminado de aquí, se usa dentro del interceptor


// Interceptor de Petición: Inyección de JWT
httpClient.interceptors.request.use((config) => {
  // Solución clave: La importación de Pinia se hace por dentro de la función para evitar el error de "Dependencia Circular" al cargar Vue
  const authStore = useAuthStore();
  if (authStore.token) {
    // Obtiene el access_token desde Pinia y lo inyecta en los headers para peticiones seguras (Authorization: Bearer)
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Interceptor de Respuesta: Manejo Global de errores y Renovación Silenciosa 
httpClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const toast = useToast();
    // Manejo de Errores de Red (El servidor no responde)
    if (!error.response) {
      toast.error('Error de red. Verifica tu conexión a internet.');
      return Promise.reject(error);
    }

    const originalRequest = error.config;
    const authStore = useAuthStore();
    const status = error.response.status;

    // Manejo Global de Errores: Errores de red o de servidor (Error 500) disparan notificaciones globales sin necesidad de programarlos en cada vista
    if (status >= 500) {
      toast.error('Error interno del servidor. Inténtalo más tarde.');
    } else if (status === 403) {
      toast.warning('No tienes permisos para realizar esta acción.');
    } else if (status === 404) {
      toast.info('El recurso que buscas no existe.');
    }

    // Renovación Silenciosa: Si el backend arroja un error 401 Unauthorized (Token expirado), el cliente pausa la petición original
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Envía el refresh_token a /auth/token/refresh/ para obtener un nuevo JWT de forma transparente
        const refreshResponse = await axios.post('http://api.auth.local/auth/token/refresh/', {
          refresh: authStore.refreshToken
        });

        const newAccess = refreshResponse.data.access;
        authStore.token = newAccess;

        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        // Reintenta la petición original; el usuario nunca nota la interrupción
        return httpClient(originalRequest);
      } catch (refreshError) {
        // Si falla el refresh token, notificamos y cerramos sesión
        toast.error('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
        authStore.logout();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default httpClient;