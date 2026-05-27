export default [
  {
    path: '/builder/:id',
    name: 'builder-studio',
    component: () => import('@/modules/builder/views/StudioView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/builder/:id/form',
    name: 'builder-form',
    component: () => import('@/modules/builder/views/CatalogFormView.vue'),
    meta: { requiresAuth: true }
  }
];
