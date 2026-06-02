<template>
  <div class="min-h-screen bg-slate-50 flex flex-col">
    <!-- Navbar -->
    <header class="navbar bg-white shadow-sm sticky top-0 z-50 px-4 sm:px-8 flex justify-between items-center h-20">
      <div class="flex items-center gap-2">
        <!-- Mobile Dropdown Menu -->
        <div class="dropdown md:hidden">
          <label tabindex="0" class="btn btn-ghost btn-circle text-slate-800">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </label>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[50] p-3 shadow-2xl bg-white rounded-2xl w-52 border border-slate-100 font-bold text-slate-700">
            <li><router-link to="/" class="py-3">Inicio</router-link></li>
            <li><router-link to="/catalog" class="py-3">Catálogo</router-link></li>
            <li v-if="authStore.isAuthenticated"><router-link to="/dashboard" class="py-3">Mis Diseños</router-link></li>
            <li v-if="authStore.isAuthenticated"><router-link to="/dashboard/orders" class="py-3">Mis Pedidos</router-link></li>
          </ul>
        </div>

        <router-link to="/" class="btn btn-ghost text-xl font-extrabold tracking-widest text-slate-800">
          INVITAZYON
        </router-link>
      </div>

      <!-- Center Desktop Navigation Links -->
      <div class="hidden md:flex gap-8 items-center">
        <router-link to="/" class="text-sm font-bold text-slate-500 hover:text-primary transition-colors">Inicio</router-link>
        <router-link to="/catalog" class="text-sm font-bold text-slate-500 hover:text-primary transition-colors">Catálogo</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="text-sm font-bold text-slate-500 hover:text-primary transition-colors">Mis Diseños</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/dashboard/orders" class="text-sm font-bold text-slate-500 hover:text-primary transition-colors">Mis Pedidos</router-link>
      </div>

      <!-- Right: User Avatar / Login Buttons -->
      <div class="flex items-center gap-2 sm:gap-4">
        <template v-if="authStore.isAuthenticated">
          <div class="dropdown dropdown-end">
            <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar border-2 border-slate-100">
              <div class="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-600 font-bold">
                {{ initial }}
              </div>
            </div>
            <ul tabindex="0" class="mt-3 z-[50] p-3 shadow-2xl menu menu-sm dropdown-content bg-white rounded-2xl w-60 border border-slate-100">
              <div class="px-4 py-3 border-b border-slate-50 mb-2">
                <p class="text-xs font-black text-slate-400 uppercase tracking-widest">Cuenta</p>
                <p class="text-sm font-bold text-slate-800 truncate">{{ authStore.user?.email }}</p>
              </div>
              <li><router-link to="/profile" class="py-3 rounded-xl">👤 Mi Perfil</router-link></li>
              <li><router-link to="/dashboard/orders" class="py-3 rounded-xl">📦 Mis Pedidos</router-link></li>
              <li v-if="['ADMIN', 'VENDOR'].includes(authStore.role)">
                <router-link to="/workspace" class="py-3 rounded-xl text-primary font-bold">🏢 Ir al Workspace POS</router-link>
              </li>
              <li><a @click="handleLogout" class="py-3 rounded-xl text-error hover:bg-error/10">🔌 Cerrar Sesión</a></li>
            </ul>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="btn btn-ghost btn-sm sm:btn-md text-slate-600 font-bold">Ingresar</router-link>
          <router-link to="/auth/registration/?redirect=create-basic" class="btn btn-primary btn-sm sm:btn-md rounded-xl shadow-lg shadow-primary/20">
            <span class="hidden sm:inline">Empezar Gratis</span>
            <span class="sm:hidden">Empezar</span>
          </router-link>
        </template>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-100 pt-20 pb-10 px-6 mt-20">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
        <div class="col-span-1 md:col-span-2 space-y-6">
          <router-link to="/" class="inline-block text-2xl font-black tracking-widest text-slate-900 hover:text-primary transition-colors">
            INVITAZYON
          </router-link>
          <p class="text-slate-400 max-w-sm leading-relaxed">
            Redefiniendo la forma en que el mundo celebra. Invitaciones digitales de lujo con tecnología interactiva para eventos inolvidables.
          </p>
        </div>
        <div>
          <h4 class="font-black text-slate-900 uppercase tracking-widest text-xs mb-6">Explorar</h4>
          <ul class="space-y-4 text-sm font-bold text-slate-400">
            <li><router-link to="/catalog" class="hover:text-primary transition-colors">Catálogo</router-link></li>
            <li><router-link to="/precios" class="hover:text-primary transition-colors">Precios</router-link></li>
            <li><a href="#" class="hover:text-primary transition-colors">Showcase</a></li>
          </ul>
        </div>
        <div>
          <h4 class="font-black text-slate-900 uppercase tracking-widest text-xs mb-6">Soporte</h4>
          <ul class="space-y-4 text-sm font-bold text-slate-400">
            <li><router-link to="/ayuda" class="hover:text-primary transition-colors">Ayuda</router-link></li>
            <li><router-link to="/terminos" class="hover:text-primary transition-colors">Términos</router-link></li>
            <li><router-link to="/privacidad" class="hover:text-primary transition-colors">Privacidad</router-link></li>
            <li><router-link to="/devoluciones" class="hover:text-primary transition-colors">Devoluciones</router-link></li>
          </ul>
        </div>
      </div>
      <div class="max-w-7xl mx-auto pt-10 border-t border-slate-50 flex flex-col md:row items-center justify-between gap-6 text-slate-300">
        <p class="text-[10px] font-black uppercase tracking-[0.2em]">© 2026 INVITAZYON DIGITAL LUXURY. TODOS LOS DERECHOS RESERVADOS.</p>
        <div class="flex gap-6">
          <!-- Social Placeholders -->
          <span class="w-5 h-5 bg-slate-100 rounded-full"></span>
          <span class="w-5 h-5 bg-slate-100 rounded-full"></span>
          <span class="w-5 h-5 bg-slate-100 rounded-full"></span>
        </div>
      </div>
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
