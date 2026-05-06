import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { jwtDecode } from 'jwt-decode'; // Importación nueva

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login/', 
      name: 'login', 
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true } // <-- Para proteger la ruta cuando esta logueado
    },
    { path: '/auth/registration/', 
      name: 'register', 
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresGuest: true } // <-- Para proteger la ruta cuando esta logueado
    },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    // Añadir estas rutas al array de routes en src/router/index.js
    { 
      path: '/password-reset', 
      name: 'password-reset', 
      component: () => import('@/views/PasswordResetView.vue'),
      meta: { requiresGuest: true } // <-- Para proteger la ruta cuando esta logueado
    },
    { 
      path: '/password-reset/confirm/:uid/:token', 
      name: 'password-reset-confirm', 
      component: () => import('@/views/PasswordResetConfirmView.vue'),
      meta: { requiresGuest: true } // <-- Para proteger la ruta cuando esta logueado
    },
    { 
      path: '/profile', 
      name: 'profile', 
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true } // Protegida por tu Navigation Guard
    },
    { 
      path: '/verify-email/:key?', // El parámetro key puede capturarse de params o dejarse como query string
      name: 'verify-email', 
      component: () => import('@/views/VerifyEmailView.vue') 
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
  
  // Guardamos en una variable si el usuario está realmente autenticado
  const isAuthenticated = token && isTokenValid(token);

  if (to.meta.requiresAuth) {
    // 1. Si la ruta es PRIVADA (Dashboard, Profile)
    if (isAuthenticated) {
      next(); 
    } else {
      authStore.logout(); 
      // meta: { requiresAuth: true } -> Expulsa al /login si no hay token
      next({ name: 'login' }); // Expulsado al login
    }
  } else if (to.meta.requiresGuest) {
    // 2. NUEVO: Si la ruta es SOLO PARA INVITADOS (Login, Register)
    if (isAuthenticated) {
      // meta: { requiresGuest: true } -> Expulsa al /dashboard si un usuario ya logueado intenta volver al /login o al /registro
      next({ name: 'dashboard' }); // Si ya tiene sesión, lo mandamos al dashboard
    } else {
      next(); // Si no tiene sesión, lo dejamos entrar a registrarse
    }
  } else {
    // 3. Rutas completamente públicas (Verify Email, Home, etc.)
    next();
  }
});

export default router;