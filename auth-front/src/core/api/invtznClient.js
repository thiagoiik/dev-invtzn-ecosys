import axios from 'axios';

const invtznClient = axios.create({
  baseURL: 'http://api.invtzn.local/api/v1/',
  headers: { 'Content-Type': 'application/json' }
});

// Interceptor de Petición: Inyectamos el token dinámicamente
invtznClient.interceptors.request.use(async (config) => {
  try {
    // Si la URL es pública (ej. ver invitación por slug), NO enviamos el token
    // Esto evita errores de "Token Expirado" en vistas que no lo requieren
    const isPublic = config.url.includes('/slug/');
    
    if (!isPublic) {
      const { useAuthStore } = await import('@/modules/auth/store/auth');
      const authStore = useAuthStore();
      if (authStore.token) {
        config.headers.Authorization = `Bearer ${authStore.token}`;
      }
    }
  } catch (e) {
    console.warn("Auth store not ready or public route");
  }
  return config;
});

// Interceptor de Respuesta: Manejo de notificaciones y renovación de sesión
invtznClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Importamos useToast dinámicamente para evitar que rompa el arranque
    const { useToast } = await import("vue-toastification");
    const toast = useToast();

    if (!error.response) {
      toast.error('Error de red. Verifica tu conexión.');
      return Promise.reject(error);
    }

    const status = error.response.status;
    const originalRequest = error.config;

    // Manejo de notificaciones según el código de error
    if (status >= 500) {
      toast.error('Error en el servidor. Inténtalo más tarde.');
    } else if (status === 403) {
      toast.warning('No tienes permisos para esta acción.');
    } else if (status === 404) {
      toast.info('Recurso no encontrado.');
    }

    // Lógica de Renovación de Token (401 Unauthorized)
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const { useAuthStore } = await import('@/modules/auth/store/auth');
        const authStore = useAuthStore();

        // Intentamos refrescar el token en api-auth
        const refreshRes = await axios.post('http://api.auth.local/auth/token/refresh/', {
          refresh: authStore.refreshToken
        });

        const newAccess = refreshRes.data.access;
        authStore.token = newAccess;

        // Reintentamos la petición original con el nuevo token
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return invtznClient(originalRequest);
      } catch (refreshError) {
        // Si el refresh también falla, la sesión murió
        const { useAuthStore } = await import('@/modules/auth/store/auth');
        useAuthStore().logout();
        toast.error('Sesión expirada. Por favor, reingresa.');
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default invtznClient;
