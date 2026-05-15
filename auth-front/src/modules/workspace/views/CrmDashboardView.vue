<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Directorio de Clientes y Staff</h2>
        <p class="text-slate-500">Gestiona roles, asigna sucursales y configura comisiones.</p>
      </div>
      <button @click="loadProfiles" class="btn btn-ghost">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
        Actualizar
      </button>
    </div>

    <div class="overflow-x-auto bg-white rounded-2xl shadow-sm border border-slate-200">
      <table class="table table-zebra w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-slate-500 uppercase text-[11px] font-black">Usuario</th>
            <th class="text-slate-500 uppercase text-[11px] font-black">Rol & Tipo</th>
            <th class="text-slate-500 uppercase text-[11px] font-black">Ubicación / Modo</th>
            <th class="text-slate-500 uppercase text-[11px] font-black text-right">Comisión</th>
            <th class="text-slate-500 uppercase text-[11px] font-black text-right">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="profile in profiles" :key="profile.remote_auth_id" class="hover">
            <td>
              <div class="flex items-center gap-3">
                <div class="avatar placeholder">
                  <div class="bg-slate-200 text-slate-500 rounded-full w-10">
                    <span class="text-xs font-bold">{{ profile.full_name?.charAt(0) || '?' }}</span>
                  </div>
                </div>
                <div>
                  <div class="font-bold text-slate-800">{{ profile.full_name || 'Sin nombre' }}</div>
                  <div class="text-xs text-slate-400 font-medium">ID #{{ profile.remote_auth_id }}</div>
                </div>
              </div>
            </td>
            <td>
              <div :class="['badge font-bold text-[10px]', getBadgeClass(profile.custom_role)]">
                {{ profile.custom_role }}
              </div>
              <div class="text-[11px] text-slate-400 mt-1 font-bold">{{ profile.customer_type }}</div>
            </td>
            <td>
              <div v-if="profile.custom_role !== 'CLIENT'">
                <div class="flex items-center gap-2">
                  <span class="text-xs font-bold text-slate-700">{{ profile.vendor_mode }}</span>
                  <div class="badge badge-outline badge-xs">{{ getStoreName(profile.assigned_store) }}</div>
                </div>
              </div>
              <span v-else class="text-slate-300 text-xs">-</span>
            </td>
            <td class="text-right">
              <span class="font-black text-slate-700">{{ profile.base_commission_rate }}%</span>
            </td>
            <td class="text-right">
              <div class="flex justify-end gap-2">
                <button v-if="profile.custom_role === 'CLIENT'" class="btn btn-xs btn-success text-white" @click="promoteToVendor(profile)">
                  Promover a Vendedor
                </button>
                <button class="btn btn-xs btn-outline" @click="openConfig(profile)">
                  Configurar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Configuración Staff -->
    <div :class="['modal', { 'modal-open': !!selectedProfile }]">
      <div class="modal-box max-w-sm">
        <h3 class="font-bold text-lg mb-4">Configurar Staff #{{ selectedProfile?.remote_auth_id }}</h3>
        <div class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-xs uppercase">Sucursal Asignada</span></label>
            <select v-model="configData.assigned_store" class="select select-bordered w-full">
              <option :value="null">Ninguna (Remoto)</option>
              <option v-for="store in stores" :key="store.id" :value="store.id">{{ store.name }}</option>
            </select>
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-xs uppercase">Modo de Venta</span></label>
            <select v-model="configData.vendor_mode" class="select select-bordered w-full">
              <option value="PHYSICAL">Físico (En Tienda)</option>
              <option value="REMOTE">Remoto (Distancia)</option>
            </select>
          </div>
        </div>
        <div class="modal-action">
          <button class="btn btn-ghost" @click="selectedProfile = null">Cancelar</button>
          <button class="btn btn-primary" @click="saveConfig" :disabled="saving">
            <span v-if="saving" class="loading loading-spinner"></span>
            Guardar Cambios
          </button>
        </div>
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
const stores = ref([]);
const loading = ref(true);
const saving = ref(false);

const selectedProfile = ref(null);
const configData = ref({
  assigned_store: null,
  vendor_mode: 'REMOTE'
});

const loadProfiles = async () => {
  loading.value = true;
  try {
    const res = await crmService.fetchAllProfiles();
    profiles.value = res.data;
  } catch (error) {
    toast.error('Error al cargar perfiles.');
  } finally {
    loading.value = false;
  }
};

const loadStores = async () => {
  try {
    const res = await crmService.fetchAllStores();
    stores.value = res.data;
  } catch (e) {}
};

const getStoreName = (storeId) => {
  if (!storeId) return 'Sin tienda';
  const s = stores.value.find(x => x.id === storeId);
  return s ? s.name : 'Desconocida';
};

const getBadgeClass = (role) => {
  switch(role) {
    case 'ADMIN': return 'badge-warning';
    case 'VENDOR': return 'badge-success text-white';
    default: return 'badge-ghost';
  }
};

const promoteToVendor = async (profile) => {
  try {
    await crmService.updateProfileRole(profile.remote_auth_id, 'VENDOR');
    toast.success('Promovido a Vendedor');
    loadProfiles();
  } catch (e) {
    toast.error('Error al promover');
  }
};

const openConfig = (profile) => {
  selectedProfile.value = profile;
  configData.value = {
    assigned_store: profile.assigned_store,
    vendor_mode: profile.vendor_mode
  };
};

const saveConfig = async () => {
  saving.value = true;
  try {
    await crmService.updateProfileStore(
      selectedProfile.value.remote_auth_id,
      configData.value.assigned_store,
      configData.value.vendor_mode
    );
    toast.success('Configuración actualizada');
    selectedProfile.value = null;
    loadProfiles();
  } catch (e) {
    toast.error('Error al guardar');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadProfiles();
  loadStores();
});
</script>
