import httpClient from '@/core/api/httpClient';

export const authService = {
  // --- Sesión ---
  login: (credentials) => httpClient.post('auth/login/', credentials),
  logout: () => httpClient.post('auth/logout/'),
  
  // --- Perfil ---
  getUserDetails: () => httpClient.get('auth/user/'),
  updateUserDetails: (data) => httpClient.patch('auth/user/', data),
  
  // --- Registro ---
  register: (userData) => httpClient.post('auth/registration/', userData),
  verifyEmail: (key) => httpClient.post('auth/registration/verify-email/', { key }),
  resendEmail: (email) => httpClient.post('auth/registration/resend-email/', { email }),
  
  // --- Contraseña ---
  passwordReset: (email) => httpClient.post('auth/password/reset/', { email }),
  passwordResetConfirm: (data) => httpClient.post('auth/password/reset/confirm/', data),
  passwordChange: (data) => httpClient.post('auth/password/change/', data),
  
  // --- Tokens ---
  tokenVerify: (token) => httpClient.post('auth/token/verify/', { token }),
  tokenRefresh: (refresh) => httpClient.post('auth/token/refresh/', { refresh })
};



