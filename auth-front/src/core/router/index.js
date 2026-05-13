import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/modules/auth/store/auth';
import { jwtDecode } from 'jwt-decode';

import authRoutes from '@/modules/auth/router/routes';
import dashboardRoutes from '@/modules/dashboard/router/routes';
import eventsRoutes from '@/modules/events/router/routes';
import ecommerceRoutes from '@/modules/ecommerce/router/routes';
import engineRoutes from '@/modules/engine/router/routes';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...authRoutes,
    ...dashboardRoutes,
    ...eventsRoutes,
    ...ecommerceRoutes,
    ...engineRoutes,
    // Ruta "Catch-All" para capturar URLs que no existen (404)
    { 
      path: '/:pathMatch(.*)*', 
      name: 'NotFound', 
      redirect: '/dashboard' 
    }
  ]
});

// Función auxiliar para validar el token
const isTokenValid = (token) => {
  if (!token) return false;
  try {
    const { exp } = jwtDecode(token);
    return Date.now() < exp * 1000;
  } catch { return false; }
};

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const token = authStore.token;
  
  const isAuthenticated = token && isTokenValid(token);

  // 2. Navigation Guards
  if (to.meta.requiresAuth) {
    if (isAuthenticated) {
      next(); 
    } else {
      authStore.logout(); 
      next({ name: 'login' }); 
    }
  } else if (to.meta.requiresGuest) {
    if (isAuthenticated) {
      next({ name: 'dashboard' }); 
    } else {
      next(); 
    }
  } else {
    next();
  }
});

export default router;
