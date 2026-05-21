<template>
  <div class="flex h-screen bg-slate-100 overflow-hidden font-sans">
    
    <!-- Backdrop Overlay for Mobile Drawer -->
    <div 
      v-if="isMobile && mobileMenuOpen" 
      class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-30 transition-opacity duration-300"
      @click="mobileMenuOpen = false"
    ></div>

    <!-- Aside Sidebar (Adaptive) -->
    <aside 
      :class="[
        isMobile 
          ? 'fixed top-0 bottom-0 left-0 z-40 w-64 transform transition-transform duration-300 ease-in-out ' + (mobileMenuOpen ? 'translate-x-0' : '-translate-x-full')
          : isTablet 
            ? 'w-20' 
            : 'w-64',
        'bg-slate-900 text-white flex flex-col shadow-2xl transition-all duration-300'
      ]"
    >
      <!-- Brand Logo / Header -->
      <div class="p-6 border-b border-slate-800 text-center flex items-center justify-center">
        <h1 
          class="font-black tracking-widest text-slate-100 transition-all duration-300"
          :class="isTablet && !isMobile ? 'text-lg' : 'text-xl'"
        >
          {{ isTablet && !isMobile ? 'ECO' : 'ECOSYS B2B' }}
        </h1>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 py-6 flex flex-col gap-2 px-4 overflow-y-auto">
        <template v-if="userRole">
          
          <!-- Link: CRM & Clientes -->
          <template v-if="['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'].includes(userRole)">
            <router-link 
              to="/workspace/crm" 
              class="flex items-center rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link"
              :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
              :title="isTablet && !isMobile ? 'CRM & Clientes' : ''"
              @click="isMobile ? mobileMenuOpen = false : null"
            >
              <span>👥</span>
              <span v-if="!isTablet || isMobile" class="text-sm">CRM & Clientes</span>
            </router-link>
          </template>
          
          <!-- Link: Gestión de Diseños -->
          <template v-if="['ADMIN', 'FRANCHISEE', 'DESIGNER', 'VENDOR'].includes(userRole)">
            <router-link 
              to="/workspace/designs" 
              class="flex items-center rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link"
              :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
              :title="isTablet && !isMobile ? 'Gestión de Diseños' : ''"
              @click="isMobile ? mobileMenuOpen = false : null"
            >
              <span>🎨</span>
              <span v-if="!isTablet || isMobile" class="text-sm">Gestión de Diseños</span>
            </router-link>
          </template>

          <!-- Link: POS / Ventas -->
          <template v-if="['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'].includes(userRole)">
            <router-link 
              to="/workspace/pos" 
              class="flex items-center rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link"
              :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
              :title="isTablet && !isMobile ? 'POS / Ventas' : ''"
              @click="isMobile ? mobileMenuOpen = false : null"
            >
              <span>🛒</span>
              <span v-if="!isTablet || isMobile" class="text-sm">POS / Ventas</span>
            </router-link>
          </template>

          <!-- Link: Conciliación -->
          <template v-if="['ADMIN', 'FRANCHISEE', 'MANAGER'].includes(userRole)">
            <router-link 
              to="/workspace/finance" 
              class="flex items-center rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link"
              :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
              :title="isTablet && !isMobile ? 'Conciliación' : ''"
              @click="isMobile ? mobileMenuOpen = false : null"
            >
              <span>💰</span>
              <span v-if="!isTablet || isMobile" class="text-sm">Conciliación</span>
            </router-link>
          </template>
          
          <!-- Configuración Sección (ADMIN) -->
          <div v-if="userRole === 'ADMIN'" class="mt-4 pt-4 border-t border-slate-800 space-y-2">
            <p 
              v-if="!isTablet || isMobile" 
              class="px-4 text-[10px] font-black text-slate-500 uppercase tracking-widest text-left"
            >
              Configuración
            </p>
            <router-link 
              to="/workspace/stores" 
              class="flex items-center rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link"
              :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
              :title="isTablet && !isMobile ? 'Sucursales' : ''"
              @click="isMobile ? mobileMenuOpen = false : null"
            >
              <span>🏬</span>
              <span v-if="!isTablet || isMobile" class="text-sm">Sucursales</span>
            </router-link>
          </div>
        </template>
        
        <div v-else class="px-4 py-3 animate-pulse bg-slate-800/50 rounded-lg">
          <p v-if="!isTablet || isMobile" class="text-[10px] text-slate-500 font-black uppercase">Cargando Menú...</p>
        </div>

        <div class="mt-auto">
          <router-link 
            to="/dashboard" 
            class="flex items-center rounded-lg text-error hover:bg-error/10 font-medium transition-all"
            :class="isTablet && !isMobile ? 'justify-center p-3 text-xl' : 'px-4 py-3 gap-3'"
            :title="isTablet && !isMobile ? 'Volver a B2C' : ''"
          >
            <span>⬅️</span>
            <span v-if="!isTablet || isMobile" class="text-sm">Volver a B2C</span>
          </router-link>
        </div>
      </nav>
    </aside>

    <!-- Main Content Frame -->
    <main class="flex-grow flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="h-20 bg-white shadow-sm flex items-center justify-between px-6 z-10">
        <div class="flex items-center gap-4">
          <!-- Hamburger Button for Mobile -->
          <button 
            v-if="isMobile" 
            @click="mobileMenuOpen = true" 
            class="p-2 text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          
          <h2 
            class="font-bold text-slate-800 transition-all duration-300"
            :class="isMobile ? 'text-lg' : 'text-2xl'"
          >
            Panel de Administración
          </h2>
        </div>
        
        <!-- User Profile Dropdown -->
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3 cursor-pointer group" @click="toggleMenu">
            <div class="text-right hidden sm:block">
              <p class="font-bold text-slate-800 group-hover:text-primary transition-colors">{{ authStore.user?.username || 'Staff' }}</p>
              <p class="text-[10px] text-slate-400 font-black uppercase tracking-widest">{{ userRole }}</p>
            </div>
            
            <div class="dropdown dropdown-end">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar border-2 border-slate-100 hover:border-primary transition-all">
                <div class="w-10 h-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-black uppercase tracking-tighter">
                  {{ authStore.user?.username?.charAt(0) || 'S' }}
                </div>
              </label>
              <ul tabindex="0" class="mt-3 z-[50] p-2 shadow-2xl menu menu-sm dropdown-content bg-white rounded-xl w-52 border border-slate-100 animate-in fade-in slide-in-from-top-2">
                <li class="menu-title px-4 py-2 text-[10px] font-black uppercase text-slate-400 tracking-widest border-b border-slate-50 mb-1">Mi Cuenta</li>
                <li><router-link to="/profile" class="py-3 font-bold text-slate-700 hover:bg-slate-50">👤 Mi Perfil</router-link></li>
                <li><router-link to="/dashboard" class="py-3 font-bold text-slate-700 hover:bg-slate-50">🏠 Inicio B2C</router-link></li>
                <li class="mt-2 border-t border-slate-50 pt-2"><button @click="handleLogout" class="py-3 font-bold text-error hover:bg-error/5">🚪 Cerrar Sesión</button></li>
              </ul>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Content Area -->
      <div 
        :class="[
          isMobile ? 'pb-24 p-4' : 'p-8',
          'flex-grow overflow-y-auto bg-slate-50'
        ]"
      >
        <router-view></router-view>
      </div>

      <!-- Bottom Nav Bar for Mobile -->
      <nav 
        v-if="isMobile" 
        class="fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-slate-200 z-30 flex justify-around items-center shadow-lg"
      >
        <!-- POS link -->
        <router-link 
          v-if="userRole && ['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'].includes(userRole)"
          to="/workspace/pos" 
          class="flex flex-col items-center justify-center text-slate-400 transition-colors"
          active-class="text-primary"
        >
          <span class="text-xl">🛒</span>
          <span class="text-[10px] font-bold mt-0.5">POS</span>
        </router-link>

        <!-- CRM link -->
        <router-link 
          v-if="userRole && ['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'].includes(userRole)"
          to="/workspace/crm" 
          class="flex flex-col items-center justify-center text-slate-400 transition-colors"
          active-class="text-primary"
        >
          <span class="text-xl">👥</span>
          <span class="text-[10px] font-bold mt-0.5">CRM</span>
        </router-link>

        <!-- Designs link -->
        <router-link 
          v-if="userRole && ['ADMIN', 'FRANCHISEE', 'DESIGNER', 'VENDOR'].includes(userRole)"
          to="/workspace/designs" 
          class="flex flex-col items-center justify-center text-slate-400 transition-colors"
          active-class="text-primary"
        >
          <span class="text-xl">🎨</span>
          <span class="text-[10px] font-bold mt-0.5">Diseños</span>
        </router-link>

        <!-- Menu shortcut to open drawer -->
        <button 
          @click="mobileMenuOpen = true" 
          class="flex flex-col items-center justify-center text-slate-400 transition-colors"
        >
          <span class="text-xl">🍔</span>
          <span class="text-[10px] font-bold mt-0.5">Menú</span>
        </button>
      </nav>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useDevice } from '@/composables/useDevice';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const userRole = computed(() => authStore.role);
const menuOpen = ref(false);
const mobileMenuOpen = ref(false);

const { isMobile, isTablet, isDesktop } = useDevice();

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.ui-active-link.router-link-active {
  background-color: #1e293b; /* bg-slate-800 */
  color: white;
  border-left: 4px solid #3b82f6; /* blue-500 */
}
</style>
