export default [
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
      },
      {
        path: '/terminos',
        name: 'terms',
        component: () => import('@/modules/ecommerce/views/TermsView.vue')
      },
      {
        path: '/privacidad',
        name: 'privacy',
        component: () => import('@/modules/ecommerce/views/PrivacyView.vue')
      },
      {
        path: '/devoluciones',
        name: 'refunds',
        component: () => import('@/modules/ecommerce/views/RefundsView.vue')
      },
      {
        path: '/precios',
        name: 'pricing',
        component: () => import('@/modules/ecommerce/views/PricingView.vue')
      },
      {
        path: '/ayuda',
        name: 'help',
        component: () => import('@/modules/ecommerce/views/HelpView.vue')
      }
    ]
  }
];
