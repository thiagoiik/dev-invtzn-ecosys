export default [
  { 
    path: '/catalog', 
    name: 'catalog', 
    component: () => import('@/modules/ecommerce/views/CatalogView.vue')
  }
];
