import invtznClient from '@/core/api/invtznClient';

export const orderService = {
  createOrder(productIdOrPayload, totalAmount = null, userId = null, deploymentId = null) {
    if (typeof productIdOrPayload === 'object' && productIdOrPayload !== null) {
      return invtznClient.post('orders/', productIdOrPayload);
    }
    
    // Fallback compatibility
    const payload = {
      product: productIdOrPayload,
      total_amount: totalAmount,
      status: 'PENDING'
    };
    if (userId) payload.user = userId;
    if (deploymentId) payload.deployment = deploymentId;
    
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
