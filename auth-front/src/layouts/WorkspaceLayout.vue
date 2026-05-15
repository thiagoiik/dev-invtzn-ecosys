<template>
  <div class="flex h-screen bg-slate-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl z-20">
      <div class="p-6 border-b border-slate-800 text-center">
        <h1 class="text-xl font-black tracking-widest text-slate-100">ECOSYS B2B</h1>
      </div>
      <nav class="flex-1 py-6 flex flex-col gap-2 px-4">
        <!-- Links comunes -->
        <router-link to="/workspace/crm" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">👥 CRM & Clientes</router-link>
        <router-link to="/workspace/designs" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🎨 Gestión de Diseños</router-link>
        <router-link to="/workspace/pos" class="px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🛒 POS / Ventas</router-link>
        
        <!-- Links exclusivos de Admin -->
        <div v-if="userRole === 'ADMIN'" class="mt-4 pt-4 border-t border-slate-800 space-y-2">
          <p class="px-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Configuración</p>
          <router-link to="/workspace/stores" class="block px-4 py-3 rounded-lg text-slate-400 font-medium transition-all hover:bg-slate-800 hover:text-white ui-active-link">🏬 Sucursales</router-link>
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
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="font-bold text-slate-800">{{ authStore.user?.username || 'Staff' }}</p>
            <p class="text-xs text-slate-500 font-bold uppercase tracking-wider">{{ userRole }}</p>
          </div>
          <div class="avatar placeholder">
            <div class="bg-primary text-primary-content rounded-full w-10">
              <span class="text-xs">B2B</span>
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
    // Si hay error de red o no existe el perfil aún, por seguridad lo sacamos
    toast.error('Error de autenticación B2B.');
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
