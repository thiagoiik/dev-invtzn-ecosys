import invtznClient from '@/core/api/invtznClient';

export const catalogService = {
  // Obtener el catálogo público de productos
  fetchProducts() {
    return invtznClient.get('products/');
  }
};
