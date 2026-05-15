import invtznClient from '@/core/api/invtznClient';

export const crmService = {
  /**
   * Obtiene la lista de perfiles (Usuarios) desde api-invtzn.
   * Solo disponible para ADMIN y VENDOR.
   */
  fetchUsers() {
    return invtznClient.get('/profiles/');
  },

  /**
   * Cambia el rol de un usuario.
   * Solo disponible para ADMIN.
   * @param {number} profileId - ID del perfil (UserProfile.id)
   * @param {string} newRole - Nuevo rol (ej. 'VENDOR', 'ADMIN', 'CLIENT')
   */
  updateUserRole(profileId, newRole) {
    return invtznClient.patch(`/profiles/${profileId}/change-role/`, {
      custom_role: newRole
    });
  },

  /**
   * Actualiza el saldo de un usuario (Simulado).
   * En el futuro puede llamar a un endpoint específico de recarga de wallet.
   */
  updateWallet(profileId, amount) {
    return invtznClient.patch(`/profiles/${profileId}/`, {
      current_balance: amount
    });
  }
};
