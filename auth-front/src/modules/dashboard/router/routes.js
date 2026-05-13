export default [
  { 
    path: '/dashboard', 
    name: 'dashboard', 
    component: () => import('@/modules/dashboard/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile', 
    name: 'profile', 
    component: () => import('@/modules/dashboard/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  }
];
