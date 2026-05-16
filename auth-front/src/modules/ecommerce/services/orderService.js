import invtznClient from '@/core/api/invtznClient';

export const orderService = {
  createOrder(productId, totalAmount, userId = null) {
    // Crea una orden en estado PENDING. Si userId viene, se asigna a ese cliente.
    const payload = {
      product: productId,
      total_amount: totalAmount,
      status: 'PENDING'
    };
    if (userId) payload.user = userId;
    
    return invtznClient.post('orders/', payload);
  },

  createStripeCheckout(orderId, successUrl, cancelUrl) {
    return invtznClient.post(`orders/${orderId}/pay-stripe/`, { 
      success_url: successUrl, 
      cancel_url: cancelUrl 
    });
  }
};
