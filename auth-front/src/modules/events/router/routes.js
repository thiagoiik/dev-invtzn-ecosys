export default [
  {
    path: '/',
    component: () => import('@/layouts/B2CLayout.vue'),
    children: [
      { 
        path: '/events', 
        name: 'my-events', 
        component: () => import('@/modules/events/views/MyEventsView.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
];
