export default [
  {
    path: '/',
    component: () => import('@/layouts/B2CLayout.vue'),
    children: [
      { 
        path: '/dashboard', 
        name: 'dashboard', 
        component: () => import('@/modules/dashboard/views/DashboardView.vue'),
        meta: { requiresAuth: true }
      },
      { 
        path: '/dashboard/orders', 
        name: 'orders-history', 
        component: () => import('@/modules/dashboard/views/OrdersHistoryView.vue'),
        meta: { requiresAuth: true }
      },
      { 
        path: '/profile', 
        name: 'profile', 
        component: () => import('@/modules/dashboard/views/ProfileView.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
];
