<template>
  <div class="min-h-screen bg-slate-50 flex flex-col">
    <!-- Navbar -->
    <header class="navbar bg-white shadow-sm sticky top-0 z-50 px-4 sm:px-8">
      <div class="flex-1">
        <router-link to="/dashboard" class="btn btn-ghost text-xl font-extrabold tracking-widest text-slate-800">
          INVITAZYON
        </router-link>
      </div>
      <div class="flex-none gap-4">
        <router-link to="/catalog" class="btn btn-ghost">Catálogo</router-link>
        <router-link to="/dashboard" class="btn btn-ghost">Mis Diseños</router-link>
        
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
            <div class="w-10 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 font-bold">
              {{ initial }}
            </div>
          </div>
          <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-white rounded-box w-52 border border-slate-100">
            <li><router-link to="/profile">Mi Perfil</router-link></li>
            <li><a @click="handleLogout" class="text-error">Cerrar Sesión</a></li>
          </ul>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="footer footer-center p-4 bg-white text-slate-500 border-t border-slate-200 mt-auto">
      <aside>
        <p>Copyright © 2026 - Todos los derechos reservados por Invitazyon B2C</p>
      </aside>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const initial = computed(() => {
  return authStore.user?.email ? authStore.user.email.charAt(0).toUpperCase() : 'U';
});

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
</style>
