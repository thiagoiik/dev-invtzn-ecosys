import invtznClient from '@/core/api/invtznClient';

export const orderService = {
  createOrder(productId, totalAmount) {
    // Crea una orden en estado PENDING
    return invtznClient.post('orders/', {
      product: productId,
      total_amount: totalAmount,
      status: 'PENDING'
    });
  }
};
