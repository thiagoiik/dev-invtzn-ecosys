<template>
  <div v-if="authStore.user">
    <h1>Dashboard</h1>
    <p>Bienvenido, {{ authStore.user.username }}</p> <!-- Datos del fetchUser -->
    <button @click="onLogout">Cerrar Sesión</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const onLogout = () => {
  authStore.logout();
  router.push({ name: 'login' }); // Redirección tras cerrar sesión
};
</script>