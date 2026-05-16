<template>
  <div class="flex h-screen bg-slate-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl z-20">
      <div class="p-6 border-b border-slate-800 text-center">
        <h1 class="text-xl font-black tracking-widest text-slate-100">ECOSYS B2B</h1>
      </div>
      <nav class="flex-1 py-6 flex flex-col gap-2 px-4">
        <!-- Links Dinámicos por Rol -->
        <template v-if="userRole">
          <template v-if="['ADMIN', 'FRANCHISEE', 'MANAGER', 'VENDOR'].includes(userRole)">
            <router-link to="/workspace/crm" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">👥 CRM & Clientes</router-link>
          </template>
          
          <template v-if="['ADMIN', 'FRANCHISEE', 'DESIGNER', 'VENDOR'].includes(userRole)">
            <router-link to="/workspace/designs" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🎨 Gestión de Diseños</router-link>
          </template>

          <template v-if="['ADMIN', 'MANAGER', 'VENDOR'].includes(userRole)">
            <router-link to="/workspace/pos" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🛒 POS / Ventas</router-link>
          </template>

          <template v-if="['ADMIN', 'FRANCHISEE', 'MANAGER'].includes(userRole)">
            <router-link to="/workspace/finance" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">💰 Conciliación</router-link>
          </template>
          
          <div v-if="userRole === 'ADMIN'" class="mt-4 pt-4 border-t border-slate-800 space-y-2">
            <p class="px-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Configuración</p>
            <router-link to="/workspace/stores" class="block px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🏬 Sucursales</router-link>
          </div>
        </template>
        <div v-else class="px-4 py-3 animate-pulse bg-slate-800/50 rounded-lg">
          <p class="text-[10px] text-slate-500 font-black uppercase">Cargando Menú...</p>
        </div>

        <div class="mt-auto">
          <router-link to="/dashboard" class="flex px-4 py-3 rounded-lg text-error hover:bg-error/10 font-medium transition-all">⬅️ Volver a B2C</router-link>
        </div>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <header class="h-20 bg-white shadow-sm flex items-center justify-between px-8 z-10">
        <h2 class="text-2xl font-bold text-slate-800">Panel de Administración</h2>
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3 cursor-pointer group" @click="toggleMenu">
            <div class="text-right">
              <p class="font-bold text-slate-800 group-hover:text-primary transition-colors">{{ authStore.user?.username || 'Staff' }}</p>
              <p class="text-[10px] text-slate-400 font-black uppercase tracking-widest">{{ userRole }}</p>
            </div>
            
            <div class="dropdown dropdown-end">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar border-2 border-slate-100 hover:border-primary transition-all">
                <div class="w-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-black uppercase tracking-tighter">
                  {{ authStore.user?.username?.charAt(0) || 'S' }}
                </div>
              </label>
              <ul tabindex="0" class="mt-3 z-[1] p-2 shadow-2xl menu menu-sm dropdown-content bg-white rounded-xl w-52 border border-slate-100 animate-in fade-in slide-in-from-top-2">
                <li class="menu-title px-4 py-2 text-[10px] font-black uppercase text-slate-400 tracking-widest border-b border-slate-50 mb-1">Mi Cuenta</li>
                <li><router-link to="/profile" class="py-3 font-bold text-slate-700 hover:bg-slate-50">👤 Mi Perfil</router-link></li>
                <li><router-link to="/dashboard" class="py-3 font-bold text-slate-700 hover:bg-slate-50">🏠 Inicio B2C</router-link></li>
                <li class="mt-2 border-t border-slate-50 pt-2"><button @click="authStore.logout()" class="py-3 font-bold text-error hover:bg-error/5">🚪 Cerrar Sesión</button></li>
              </ul>
            </div>
          </div>
        </div>
      </header>
      
      <div class="flex-1 p-8 overflow-y-auto bg-slate-50">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/modules/auth/store/auth';
import { profileService } from '@/modules/dashboard/services/profileService';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();
const userRole = ref(null);
const menuOpen = ref(false);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

onMounted(async () => {
  try {
    const res = await profileService.fetchMyProfile();
    userRole.value = res.data.custom_role;
    
    // Si el usuario es un CLIENTE normal, lo sacamos del Workspace
    if (userRole.value === 'CLIENT') {
      toast.error('Acceso denegado. Área exclusiva para personal B2B.');
      router.push('/dashboard');
    }
  } catch (error) {
    console.error("B2B Auth Error:", error);
    toast.error('Error al validar permisos B2B.');
    router.push('/dashboard');
  }
});
</script>

<style scoped>
.ui-active-link.router-link-active {
  background-color: #1e293b; /* bg-slate-800 */
  color: white;
  border-left: 4px solid #3b82f6; /* blue-500 */
}
</style>
