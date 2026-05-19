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
        redirect: '/workspace/crm'
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
        meta: { requiresRole: ['ADMIN', 'MANAGER', 'VENDOR'] }
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
      }
    ]
  }
];
