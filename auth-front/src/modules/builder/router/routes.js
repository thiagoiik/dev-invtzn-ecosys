export default [
  {
    path: '/builder/:id',
    name: 'builder-studio',
    component: () => import('@/modules/builder/views/StudioView.vue'),
    meta: { requiresAuth: true }
  }
];
