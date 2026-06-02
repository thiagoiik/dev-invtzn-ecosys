import { useAuthStore } from '@/modules/auth/store/auth';

export default [
  {
    path: '/workspace',
    component: () => import('@/layouts/WorkspaceLayout.vue'),
    meta: { 
      requiresAuth: true,
      requiresRole: ['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR', 'DESIGNER']
    },
    children: [
      {
        path: '',
        redirect: () => {
          const authStore = useAuthStore();
          if (authStore.role === 'DESIGNER') {
            return '/workspace/designs';
          }
          return '/workspace/crm';
        }
      },
      {
        path: 'products',
        name: 'workspace-products',
        component: () => import('@/modules/workspace/views/ProductsManagerView.vue'),
        meta: { requiresRole: ['ADMIN'] }
      },
      {
        path: 'crm',
        name: 'workspace-crm',
        component: () => import('@/modules/workspace/views/CrmDashboardView.vue'),
        meta: { requiresRole: ['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'] }
      },
      {
        path: 'designs',
        name: 'workspace-designs',
        component: () => import('@/modules/workspace/views/DesignsManagerView.vue'),
        meta: { requiresRole: ['ADMIN', 'FRANCHISEE', 'DESIGNER', 'VENDOR'] }
      },
      {
        path: 'pos',
        name: 'workspace-pos',
        component: () => import('@/modules/workspace/views/PosView.vue'),
        meta: { requiresRole: ['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'] }
      },
      {
        path: 'stores',
        name: 'workspace-stores',
        component: () => import('@/modules/workspace/views/StoresManagerView.vue'),
        meta: { requiresRole: ['ADMIN'] }
      },
      {
        path: 'finance',
        name: 'workspace-finance',
        component: () => import('@/modules/workspace/views/FinanceReconciliationView.vue'),
        meta: { requiresRole: ['ADMIN', 'FRANCHISEE', 'MANAGER'] }
      },
      {
        path: 'tools',
        name: 'workspace-tools',
        component: () => import('../views/DevToolsView.vue'),
        meta: { 
          requiresAuth: true,
          roles: ['ADMIN', 'FRANCHISEE'],
          title: 'Herramientas Dev'
        }
      },
      {
        path: 'coupons',
        name: 'workspace-coupons',
        component: () => import('../views/CouponsView.vue'),
        meta: { 
          requiresAuth: true,
          roles: ['ADMIN', 'FRANCHISEE'],
          title: 'Gestión de Cupones'
        }
      },
      {
        path: 'reviews',
        name: 'workspace-reviews',
        component: () => import('@/modules/workspace/views/ReviewsManagerView.vue'),
        meta: { requiresRole: ['ADMIN', 'FRANCHISEE'] }
      }
    ]
  }
];
