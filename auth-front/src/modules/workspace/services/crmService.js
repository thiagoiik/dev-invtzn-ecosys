import invtznClient from '@/core/api/invtznClient';

export const crmService = {
  // Perfiles y CRM
  fetchAllProfiles() {
    return invtznClient.get('profiles/');
  },
  
  updateProfileRole(profileId, newRole) {
    return invtznClient.patch(`profiles/${profileId}/change-role/`, { custom_role: newRole });
  },

  updateProfileStore(profileId, storeId, vendorMode) {
    return invtznClient.patch(`profiles/${profileId}/`, { 
      assigned_store: storeId,
      vendor_mode: vendorMode
    });
  },

  updateProfileGeneral(profileId, data) {
    return invtznClient.patch(`profiles/${profileId}/`, data);
  },

  searchProfile(remoteAuthId) {
    return invtznClient.get('profiles/search/', { params: { remote_auth_id: remoteAuthId } });
  },

  // Tiendas
  fetchAllStores() {
    return invtznClient.get('stores/');
  },

  createStore(data) {
    return invtznClient.post('stores/', data);
  },

  // Comisiones y Sesiones
  addWalletLog(profileId, amount, reason, notes = '') {
    return invtznClient.post('wallet-logs/', {
      user: profileId,
      amount,
      reason,
      notes
    });
  },

  fetchMyCommissions() {
    return invtznClient.get('commissions/');
  },

  openCashSession(openingBalance, storeId) {
    return invtznClient.post('cash-sessions/', {
      opening_balance: openingBalance,
      store: storeId
    });
  },

  fetchMySessions() {
    return invtznClient.get('cash-sessions/');
  },

  // Diseños
  fetchAllDeployments() {
    return invtznClient.get('deployments/');
  }
};
