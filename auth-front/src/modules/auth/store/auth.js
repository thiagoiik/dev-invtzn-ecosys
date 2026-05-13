import { defineStore } from 'pinia';
import { authService } from '@/modules/auth/services/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    refreshToken: null,
  }),

  persist: true,

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      const response = await authService.login(credentials);
      this.token = response.data.access;
      this.refreshToken = response.data.refresh;
      await this.fetchUser();
    },

    async fetchUser() {
      const response = await authService.getUserDetails();
      this.user = response.data;
    },

    // CAMBIO 5: Se elimina la lógica de llamar a authService.tokenRefresh()
    // El interceptor se encarga del flujo de red. Si necesitas actualizar el token
    // manualmente, puedes dejar esta acción solo para asignar el valor.
    setNewToken(newToken) {
      this.token = newToken;
    },

    logout() {
      this.$reset();
    }
  }
});