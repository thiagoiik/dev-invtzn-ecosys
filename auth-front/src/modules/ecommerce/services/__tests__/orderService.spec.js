import { describe, it, expect, vi } from 'vitest';
import { orderService } from '../orderService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient', () => ({
  default: {
    post: vi.fn()
  }
}));

describe('orderService', () => {
  it('createOrder hace un POST a orders/ con el payload correcto', async () => {
    const mockOrder = { id: 10, product: 1, total_amount: 150.00, status: 'PENDING' };
    invtznClient.post.mockResolvedValue({ data: mockOrder });

    const response = await orderService.createOrder(1, 150.00, 14, 5);

    expect(invtznClient.post).toHaveBeenCalledWith('orders/', {
      product: 1,
      total_amount: 150.00,
      status: 'PENDING',
      user: 14,
      deployment: 5
    });
    expect(response.data).toEqual(mockOrder);
  });

  it('createStripeCheckout hace un POST a orders/:id/pay-stripe/ con urls de retorno', async () => {
    const mockStripeResponse = { url: 'https://stripe.com/checkout' };
    invtznClient.post.mockResolvedValue({ data: mockStripeResponse });

    const response = await orderService.createStripeCheckout(10, 'http://success', 'http://cancel');

    expect(invtznClient.post).toHaveBeenCalledWith('orders/10/pay-stripe/', {
      success_url: 'http://success',
      cancel_url: 'http://cancel'
    });
    expect(response.data).toEqual(mockStripeResponse);
  });

  it('completePosOrder hace un POST a orders/:id/complete-pos/ con el metodo de pago', async () => {
    const mockPosResponse = { success: true };
    invtznClient.post.mockResolvedValue({ data: mockPosResponse });

    const response = await orderService.completePosOrder(10, 'CASH');

    expect(invtznClient.post).toHaveBeenCalledWith('orders/10/complete-pos/', {
      payment_method: 'CASH'
    });
    expect(response.data).toEqual(mockPosResponse);
  });
});
