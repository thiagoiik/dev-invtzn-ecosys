export default [
  {
    path: '/',
    name: 'home',
    component: () => import('@/modules/ecommerce/views/HomeView.vue')
  },
  {
    path: '/',
    component: () => import('@/layouts/B2CLayout.vue'),
    children: [
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
        component: () => import('@/modules/ecommerce/views/CheckoutView.vue')
      }
    ]
  }
];
