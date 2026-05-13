export default [
  { 
    path: '/i/:slug', 
    name: 'render-engine', 
    component: () => import('@/modules/engine/views/RenderEngineView.vue')
    // No requiere meta: { requiresAuth } porque es una URL pública para invitados
  }
];
