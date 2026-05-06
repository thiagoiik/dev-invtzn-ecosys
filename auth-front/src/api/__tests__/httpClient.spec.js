import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { setActivePinia, createPinia } from 'pinia';

// 1. Usamos vi.hoisted para elevar las variables antes de las importaciones
const { mockToastError, mockToastWarning, mockToastInfo } = vi.hoisted(() => ({
  mockToastError: vi.fn(),
  mockToastWarning: vi.fn(),
  mockToastInfo: vi.fn()
}));

// 2. Ahora el mock puede acceder a las variables sin fallar
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    error: mockToastError,
    warning: mockToastWarning,
    info: mockToastInfo
  })
}));

// IMPORTANTE: Importar el httpClient DESPUÉS de hacer el mock
import httpClient from '../httpClient';
import { useAuthStore } from '@/stores/auth';

describe('HTTP Client - Interceptores', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.restoreAllMocks();
  });

  it('debería inyectar el header Authorization si existe un token', () => {
    const store = useAuthStore();
    store.token = 'mi-token-secreto';

    const requestInterceptor = httpClient.interceptors.request.handlers.find(h => h.fulfilled);
    
    const config = { headers: {} };
    const result = requestInterceptor.fulfilled(config);

    expect(result.headers.Authorization).toBe('Bearer mi-token-secreto');
  });

  it('debería mostrar un toast de error ante un fallo global del servidor (Error 500)', async () => {
    const errorInterceptor = httpClient.interceptors.response.handlers.find(h => h.rejected);
    
    const error500 = {
      response: { status: 500 },
      config: {}
    };

    await expect(errorInterceptor.rejected(error500)).rejects.toEqual(error500);
    expect(mockToastError).toHaveBeenCalledWith('Error interno del servidor. Inténtalo más tarde.');
  });

  it('debería intentar refrescar el token y reintentar la petición ante un error 401', async () => {
    const store = useAuthStore();
    store.token = 'old-token';
    store.refreshToken = 'valid-refresh';

    vi.spyOn(axios, 'post').mockResolvedValue({ 
      data: { access: 'new-access-token' } 
    });

    const errorInterceptor = httpClient.interceptors.response.handlers.find(h => h.rejected);
    const mockAdapter = vi.fn().mockResolvedValue({ data: 'retry-success' });

    const error401 = {
      response: { status: 401 },
      config: { 
        _retry: false, 
        headers: {},
        adapter: mockAdapter 
      }
    };

    const result = await errorInterceptor.rejected(error401);

    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('auth/token/refresh/'), 
      { refresh: 'valid-refresh' }
    );
    expect(store.token).toBe('new-access-token');
    expect(result.data).toBe('retry-success');
    expect(mockAdapter).toHaveBeenCalled(); 
  });

  it('debería cerrar sesión y notificar si el refresh token también falla', async () => {
    const store = useAuthStore();
    store.token = 'old-token';
    store.refreshToken = 'expired-refresh';
    
    const logoutSpy = vi.spyOn(store, 'logout');

    const refreshError = new Error('Refresh failed');
    vi.spyOn(axios, 'post').mockRejectedValue(refreshError);

    const errorInterceptor = httpClient.interceptors.response.handlers.find(h => h.rejected);

    const error401 = {
      response: { status: 401 },
      config: { _retry: false, headers: {} }
    };

    await expect(errorInterceptor.rejected(error401)).rejects.toEqual(refreshError);
    
    expect(mockToastError).toHaveBeenCalledWith('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
    expect(logoutSpy).toHaveBeenCalled();
  });
});