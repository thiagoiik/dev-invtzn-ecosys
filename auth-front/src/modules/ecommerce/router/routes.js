export default [
  { 
    path: '/catalog', 
    name: 'catalog', 
    component: () => import('@/modules/ecommerce/views/CatalogView.vue')
  },
  {
    path: '/catalog/:id',
    name: 'product-detail',
    component: () => import('@/modules/ecommerce/views/ProductDetailView.vue')
  },
  {
    path: '/checkout/:id',
    name: 'checkout',
    component: () => import('@/modules/ecommerce/views/CheckoutView.vue'),
    meta: { requiresAuth: true } // El checkout sí requiere estar logueado
  }
];
