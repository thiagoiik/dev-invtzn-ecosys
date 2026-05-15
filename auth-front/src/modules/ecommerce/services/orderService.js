import invtznClient from '@/core/api/invtznClient';

export const orderService = {
  createOrder(productId, totalAmount, userId = null) {
    const payload = {
      product: productId,
      total_amount: totalAmount,
      status: 'PENDING'
    };
    if (userId) payload.user = userId;
    
    return invtznClient.post('orders/', payload);
  }
};
