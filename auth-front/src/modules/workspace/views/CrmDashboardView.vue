<template>
  <div class="crm-dashboard">
    <div class="header">
      <h3>Directorio de Clientes</h3>
      <button @click="loadProfiles" class="btn btn-refresh">🔄 Actualizar</button>
    </div>

    <div v-if="loading" class="loading">Cargando datos del CRM...</div>
    
    <table v-else class="data-grid">
      <thead>
        <tr>
          <th>ID Usuario</th>
          <th>Rol</th>
          <th>Tipo</th>
          <th>Billetera</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="profile in profiles" :key="profile.remote_auth_id">
          <td>#{{ profile.remote_auth_id }}</td>
          <td>
            <span :class="['badge', profile.custom_role.toLowerCase()]">
              {{ profile.custom_role }}
            </span>
          </td>
          <td>{{ profile.customer_type }}</td>
          <td>${{ profile.current_balance }}</td>
          <td>
            <button @click="promoteToVendor(profile)" class="btn btn-sm" v-if="profile.custom_role === 'CLIENT'">
              Hacer Vendedor
            </button>
          </td>
        </tr>
      </tbody>
    </table>
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
    const res = await crmService.fetchAllProfiles();
    profiles.value = res.data;
  } catch (error) {
    toast.error('No tienes permisos para ver el CRM o hubo un error.');
  } finally {
    loading.value = false;
  }
};

const promoteToVendor = async (profile) => {
  try {
    await crmService.updateProfileRole(profile.remote_auth_id, 'VENDOR');
    toast.success(`Usuario #${profile.remote_auth_id} ascendido a VENDOR`);
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
.crm-dashboard {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}
.btn-refresh {
  background: #f1f5f9;
  color: #475569;
}
.btn-sm {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
}
.data-grid {
  width: 100%;
  border-collapse: collapse;
}
.data-grid th, .data-grid td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
.data-grid th {
  background: #f8fafc;
  color: #64748b;
  font-weight: 600;
}
.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
}
.badge.client { background: #e0f2fe; color: #0284c7; }
.badge.vendor { background: #dcfce7; color: #16a34a; }
.badge.admin { background: #fef08a; color: #854d0e; }
</style>
