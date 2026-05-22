import invtznClient from '@/core/api/invtznClient';

export const orderService = {
  createOrder(items, totalAmount, userId = null, deploymentId = null) {
    // Si se pasa un objeto de payload completo, enviarlo directamente
    if (items && typeof items === 'object' && !Array.isArray(items)) {
      return invtznClient.post('orders/', items);
    }

    const payload = {
      total_amount: totalAmount,
      status: 'PENDING'
    };
    if (userId) payload.user = userId;
    if (deploymentId) payload.deployment = deploymentId;

    if (Array.isArray(items)) {
      payload.items = items;
    } else {
      // Legacy compatibility: si se pasa un ID único de producto, usar la llave 'product'
      payload.product = items;
    }
    
    return invtznClient.post('orders/', payload);
  },

  createStripeCheckout(orderId, successUrl, cancelUrl) {
    return invtznClient.post(`orders/${orderId}/pay-stripe/`, { 
      success_url: successUrl, 
      cancel_url: cancelUrl 
    });
  },

  completePosOrder(orderId, paymentMethod, customerEmail = null) {
    const payload = { payment_method: paymentMethod };
    if (customerEmail) payload.customer_email = customerEmail;
    return invtznClient.post(`orders/${orderId}/complete-pos/`, payload);
  },

  sendReceiptEmail(orderId, email) {
    return invtznClient.post(`orders/${orderId}/send-email/`, { email });
  },

  issueCFDI(orderId, billingData) {
    return invtznClient.post(`orders/${orderId}/issue-cfdi/`, billingData);
  }
};
