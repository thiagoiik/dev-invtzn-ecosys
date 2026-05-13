export default [
  { path: '/login/', 
    name: 'login', 
    component: () => import('@/modules/auth/views/LoginView.vue'),
    meta: { requiresGuest: true }
  },
  { path: '/auth/registration/', 
    name: 'register', 
    component: () => import('@/modules/auth/views/RegisterView.vue'),
    meta: { requiresGuest: true }
  },
  { 
    path: '/password-reset', 
    name: 'password-reset', 
    component: () => import('@/modules/auth/views/PasswordResetView.vue'),
    meta: { requiresGuest: true }
  },
  { 
    path: '/password-reset/confirm/:uid/:token', 
    name: 'password-reset-confirm', 
    component: () => import('@/modules/auth/views/PasswordResetConfirmView.vue'),
    meta: { requiresGuest: true }
  },
  { 
    path: '/verify-email/:key?',
    name: 'verify-email', 
    component: () => import('@/modules/auth/views/VerifyEmailView.vue') 
  }
];
