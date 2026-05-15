<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <div>
        <h3 class="text-2xl font-bold text-slate-800">Directorio de Clientes</h3>
        <p class="text-slate-500 text-sm mt-1">Gestión de usuarios y billeteras (CRM)</p>
      </div>
      <button @click="loadProfiles" class="btn btn-outline btn-primary">
        <span v-if="loading" class="loading loading-spinner loading-sm"></span>
        <span v-else>🔄</span> Actualizar
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
    
    <div v-else class="card bg-base-100 shadow-xl border border-slate-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <!-- head -->
          <thead class="bg-slate-50 text-slate-600 text-sm">
            <tr>
              <th>ID Usuario</th>
              <th>Rol</th>
              <th>Tipo Cliente</th>
              <th>Billetera</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="profile in profiles" :key="profile.remote_auth_id">
              <td class="font-medium text-slate-800">#{{ profile.remote_auth_id }}</td>
              <td>
                <div :class="[
                  'badge font-bold',
                  profile.custom_role === 'ADMIN' ? 'badge-error' : '',
                  profile.custom_role === 'VENDOR' ? 'badge-success text-white' : '',
                  profile.custom_role === 'CLIENT' ? 'badge-info text-white' : ''
                ]">
                  {{ profile.custom_role }}
                </div>
              </td>
              <td>{{ profile.customer_type }}</td>
              <td class="font-bold text-slate-700">${{ profile.current_balance }}</td>
              <td>
                <div class="flex gap-2">
                  <button @click="promoteToVendor(profile)" class="btn btn-xs btn-success text-white" v-if="profile.custom_role === 'CLIENT'">
                    ↑ Hacer Vendedor
                  </button>
                  <button @click="promoteToAdmin(profile)" class="btn btn-xs btn-error text-white" v-if="profile.custom_role === 'VENDOR'">
                    ↑ Hacer Admin
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="profiles.length === 0">
              <td colspan="5" class="text-center py-8 text-slate-500">No se encontraron usuarios en la base de datos.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { crmService } from '@/modules/workspace/services/crmService';

const toast = useToast();
const profiles = ref([]);
const loading = ref(true);

const loadProfiles = async () => {
  loading.value = true;
  try {
    const res = await crmService.fetchUsers();
    profiles.value = res.data;
  } catch (error) {
    toast.error('No tienes permisos para ver el CRM o hubo un error.');
  } finally {
    loading.value = false;
  }
};

const promoteToVendor = async (profile) => {
  if(!confirm(`¿Hacer a #${profile.remote_auth_id} Vendedor?`)) return;
  try {
    await crmService.updateUserRole(profile.id, 'VENDOR');
    toast.success(`Usuario #${profile.remote_auth_id} ascendido a VENDOR`);
    loadProfiles();
  } catch (error) {
    toast.error('Error al actualizar el rol');
  }
};

const promoteToAdmin = async (profile) => {
  if(!confirm(`¿Hacer a #${profile.remote_auth_id} Administrador?`)) return;
  try {
    await crmService.updateUserRole(profile.id, 'ADMIN');
    toast.success(`Usuario #${profile.remote_auth_id} ascendido a ADMIN`);
    loadProfiles();
  } catch (error) {
    toast.error('Error al actualizar el rol');
  }
};

onMounted(() => {
  loadProfiles();
});
</script>

<style scoped>
/* Tailwind maneja los estilos */
</style>
