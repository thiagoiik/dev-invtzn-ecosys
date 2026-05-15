export default [
  {
    path: '/workspace',
    component: () => import('@/layouts/WorkspaceLayout.vue'),
    meta: { requiresAuth: true }, // Más adelante podemos añadir requiresAdmin: true
    children: [
      {
        path: '',
        redirect: '/workspace/crm'
      },
      {
        path: 'crm',
        name: 'workspace-crm',
        component: () => import('@/modules/workspace/views/CrmDashboardView.vue')
      },
      {
        path: 'designs',
        name: 'workspace-designs',
        component: () => import('@/modules/workspace/views/DesignsManagerView.vue')
      },
      {
        path: 'pos',
        name: 'workspace-pos',
        component: () => import('@/modules/workspace/views/PosView.vue')
      }
    ]
  }
];
