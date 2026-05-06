import { setActivePinia, createPinia } from 'pinia';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from '../auth';
import { authService } from '@/services/authService';

// Mockeamos el servicio para no hacer peticiones reales a la API
vi.mock('@/services/authService', () => ({
  authService: {
    login: vi.fn(),
    getUserDetails: vi.fn(),
  }
}));

describe('Auth Store - Flujos de Autenticación', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('debería inicializar con el estado vacío (Estado Inicial)', () => {
    const store = useAuthStore();
    expect(store.token).toBe(null);
    expect(store.user).toBe(null);
    expect(store.isAuthenticated).toBe(false);
  });

  it('debería guardar tokens y datos de usuario tras un login exitoso (Acción Login)', async () => {
    const store = useAuthStore();
    const mockResponse = { data: { access: 'token-access', refresh: 'token-refresh' } };
    const mockUser = { data: { username: 'testuser', email: 'test@mail.com' } };

    authService.login.mockResolvedValue(mockResponse);
    authService.getUserDetails.mockResolvedValue(mockUser);

    await store.login({ username: 'testuser', password: 'password123' });

    expect(store.token).toBe('token-access');
    expect(store.refreshToken).toBe('token-refresh');
    expect(store.user).toEqual(mockUser.data);
    expect(store.isAuthenticated).toBe(true);
  });

  it('debería limpiar el estado completamente al hacer logout (Acción Logout)', () => {
    const store = useAuthStore();
    // Inyectamos datos falsos iniciales
    store.token = 'some-token';
    store.refreshToken = 'some-refresh-token';
    store.user = { name: 'Admin' };

    // Ejecutamos la acción
    store.logout();

    // Validamos la limpieza total
    expect(store.token).toBe(null);
    expect(store.refreshToken).toBe(null);
    expect(store.user).toBe(null);
    expect(store.isAuthenticated).toBe(false);
  });
});