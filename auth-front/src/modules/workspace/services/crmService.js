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

  searchProfile(query) {
    return invtznClient.get('profiles/search/', { params: { query } });
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

  closeCashSession(sessionId, closingBalance) {
    return invtznClient.post(`cash-sessions/${sessionId}/close/`, {
      closing_balance: closingBalance
    });
  },

  // Finanzas y Conciliación
  fetchBankLogs() {
    return invtznClient.get('integrations/');
  },

  simulateBankWebhook(amount) {
    return invtznClient.post('integrations/simulate-webhook/', { amount });
  },

  syncOrderWithBank(bankLogId, orderId) {
    return invtznClient.post('integrations/sync/', { 
      bank_log_id: bankLogId, 
      order_id: orderId 
    });
  },

  fetchPendingOrders() {
    return invtznClient.get('orders/', { params: { status: 'PENDING' } });
  },

  createOrder(data) {
    return invtznClient.post('orders/', data);
  },

  // Stripe
  getStripeOnboardingLink(storeId, returnUrl) {
    return invtznClient.post(`stores/${storeId}/stripe-onboarding/`, { return_url: returnUrl });
  },

  verifyStripeOnboarding(storeId) {
    return invtznClient.get(`stores/${storeId}/stripe-verify/`);
  },

  debugStripe() {
    return invtznClient.get('integrations/debug-stripe/');
  },

  createStripeCheckout(orderId, successUrl, cancelUrl) {
    return invtznClient.post(`orders/${orderId}/pay-stripe/`, { 
      success_url: successUrl, 
      cancel_url: cancelUrl 
    });
  },

  // Diseños
  fetchAllDeployments() {
    return invtznClient.get('deployments/');
  },
  
  fetchDeploymentMetrics(id) {
    return invtznClient.get(`deployments/${id}/metrics/`);
  }
};
