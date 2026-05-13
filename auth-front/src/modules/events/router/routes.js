export default [
  { 
    path: '/events', 
    name: 'my-events', 
    component: () => import('@/modules/events/views/MyEventsView.vue'),
    meta: { requiresAuth: true }
  }
];
