import { describe, it, expect, vi } from 'vitest';
import { catalogService } from '../catalogService';
import invtznClient from '@/core/api/invtznClient';

vi.mock('@/core/api/invtznClient', () => ({
  default: {
    get: vi.fn()
  }
}));

describe('catalogService', () => {
  it('fetchProducts hace un GET a products/', async () => {
    const mockProducts = [
      { id: 1, name: 'Prod A', is_active: true },
      { id: 2, name: 'Prod B', is_active: false }
    ];
    invtznClient.get.mockResolvedValue({ data: mockProducts });
    
    const response = await catalogService.fetchProducts();
    
    expect(invtznClient.get).toHaveBeenCalledWith('products/');
    expect(response.data).toEqual(mockProducts);
  });
});
