<template>
  <div class="space-y-6">
    <!-- Header Card -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Herramientas de Desarrollador</h2>
        <p class="text-slate-500 text-sm">Monitorea integraciones de pago, visualiza webhooks y realiza simulaciones en el sandbox.</p>
      </div>
      <div>
        <button @click="refreshCurrentLogs" class="btn btn-outline border-slate-300 text-slate-600 hover:bg-slate-50">
          🔄 Refrescar Logs
        </button>
      </div>
    </div>

    <!-- Tab Navigation (only visible to ADMIN/superuser) -->
    <div v-if="isAdmin" class="tabs tabs-boxed bg-white p-1 rounded-xl max-w-xs border border-slate-200 flex gap-1">
      <button 
        :class="['tab font-bold text-xs px-4 py-2 rounded-lg transition-all', activeTab === 'webhooks' ? 'tab-active bg-primary text-white' : 'text-slate-500 hover:bg-slate-100']"
        @click="activeTab = 'webhooks'"
      >
        📡 Webhooks (Stripe)
      </button>
      <button 
        :class="['tab font-bold text-xs px-4 py-2 rounded-lg transition-all', activeTab === 'system' ? 'tab-active bg-primary text-white' : 'text-slate-500 hover:bg-slate-100']"
        @click="activeTab = 'system'"
      >
        🖥️ Logs del Sistema
      </button>
    </div>

    <!-- Webhook Logs View -->
    <div v-if="activeTab === 'webhooks'" class="space-y-6 animate-in fade-in duration-200">
      <!-- Webhook Logs -->
      <div class="card bg-white border border-slate-200 shadow-sm rounded-2xl">
        <div class="card-body p-6">
          <h2 class="card-title text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <span>📡</span> Visor de Webhooks (Stripe)
          </h2>
          <div class="overflow-x-auto">
            <table class="table w-full">
              <thead>
                <tr class="text-slate-500 border-b border-slate-200">
                  <th class="font-bold text-slate-700">Fecha</th>
                  <th class="font-bold text-slate-700">Proveedor</th>
                  <th class="font-bold text-slate-700">Estado</th>
                  <th class="font-bold text-slate-700">Mensaje</th>
                  <th class="font-bold text-slate-700">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in webhookLogs" :key="log.id" class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                  <td class="text-slate-700 text-sm font-medium">{{ new Date(log.created_at).toLocaleString() }}</td>
                  <td><span class="badge badge-outline badge-primary font-semibold">{{ log.provider }}</span></td>
                  <td>
                    <span class="badge font-semibold" :class="{
                      'badge-success text-white': log.status === 'success',
                      'badge-error text-white': log.status === 'failed',
                      'badge-warning text-white': log.status === 'received'
                    }">{{ log.status }}</span>
                  </td>
                  <td class="text-slate-600 text-xs truncate max-w-xs font-mono">{{ log.message }}</td>
                  <td>
                    <button @click="viewPayload(log)" class="btn btn-sm btn-ghost text-xs text-primary hover:bg-primary/5">Ver Payload</button>
                  </td>
                </tr>
                <tr v-if="webhookLogs.length === 0">
                  <td colspan="5" class="text-center text-slate-400 py-12">
                    <div class="text-3xl mb-2">📡</div>
                    No se han recibido webhooks aún.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Simulador de Pagos -->
      <div class="card bg-white border border-slate-200 shadow-sm rounded-2xl">
        <div class="card-body p-6">
          <h2 class="card-title text-lg font-bold text-slate-800 mb-2 flex items-center gap-2">
            <span>⚡</span> Simular Activación de Orden
          </h2>
          <p class="text-slate-500 text-sm mb-4">Fuerza el pago y la activación de una orden que se quedó pendiente porque el webhook no llegó.</p>
          <div class="flex gap-4 items-center flex-wrap sm:flex-nowrap">
            <div class="form-control flex-1 max-w-xs">
              <input v-model="orderIdToForce" type="number" placeholder="ID de la Orden" class="input input-bordered bg-white border-slate-300 text-slate-800 w-full" />
            </div>
            <button @click="forceActivation" :disabled="!orderIdToForce || isLoading" class="btn btn-primary">
              <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
              Forzar Pago y Activación
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- System Logs View -->
    <div v-else-if="activeTab === 'system' && isAdmin" class="card bg-white border border-slate-200 shadow-sm rounded-2xl animate-in fade-in duration-200">
      <div class="card-body p-6">
        <h2 class="card-title text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
          <span>🖥️</span> Logs del Sistema
        </h2>
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr class="text-slate-500 border-b border-slate-200">
                <th class="font-bold text-slate-700">Fecha</th>
                <th class="font-bold text-slate-700">Tipo</th>
                <th class="font-bold text-slate-700">Mensaje</th>
                <th class="font-bold text-slate-700">Usuario</th>
                <th class="font-bold text-slate-700">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in systemLogs" :key="log.id" class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                <td class="text-slate-700 text-sm font-medium">{{ new Date(log.created_at).toLocaleString() }}</td>
                <td>
                  <span :class="[
                    'badge font-semibold text-xs',
                    log.log_type === 'USER_ACTION' ? 'badge-info' :
                    log.log_type === 'DEPLOYMENT_STATE' ? 'badge-primary' : 'badge-warning'
                  ]">{{ log.log_type }}</span>
                </td>
                <td class="text-slate-650 text-xs font-semibold max-w-sm truncate">{{ log.message }}</td>
                <td class="text-slate-600 text-xs font-mono">
                  {{ log.username || 'Sistema' }}
                  <span class="text-slate-400 block text-[10px]">ID: {{ log.user_id || 'N/A' }}</span>
                </td>
                <td>
                  <button @click="viewMetadata(log)" class="btn btn-sm btn-ghost text-xs text-primary hover:bg-primary/5">Ver Metadata</button>
                </td>
              </tr>
              <tr v-if="systemLogs.length === 0">
                <td colspan="5" class="text-center text-slate-400 py-12">
                  <div class="text-3xl mb-2">🖥️</div>
                  No hay logs de sistema registrados.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Payload -->
    <dialog id="payload_modal" class="modal">
      <div class="modal-box bg-white border border-slate-200 rounded-2xl w-11/12 max-w-5xl shadow-2xl">
        <h3 class="font-bold text-xl text-slate-800 mb-4 flex items-center gap-2">
          <span>📦</span> Payload del Webhook
        </h3>
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700 overflow-x-auto">
          <pre class="text-emerald-400 text-xs font-mono"><code>{{ selectedPayload }}</code></pre>
        </div>
        <div class="modal-action border-t border-slate-100 pt-4 mt-6">
          <form method="dialog">
            <button class="btn btn-outline border-slate-300 text-slate-600 hover:bg-slate-50">Cerrar</button>
          </form>
        </div>
      </div>
    </dialog>

    <!-- Modal Metadata -->
    <dialog id="metadata_modal" class="modal">
      <div class="modal-box bg-white border border-slate-200 rounded-2xl w-11/12 max-w-5xl shadow-2xl">
        <h3 class="font-bold text-xl text-slate-800 mb-4 flex items-center gap-2">
          <span>⚙️</span> Metadata del Log del Sistema
        </h3>
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700 overflow-x-auto">
          <pre class="text-emerald-400 text-xs font-mono"><code>{{ selectedMetadata }}</code></pre>
        </div>
        <div class="modal-action border-t border-slate-100 pt-4 mt-6">
          <form method="dialog">
            <button class="btn btn-outline border-slate-300 text-slate-600 hover:bg-slate-50">Cerrar</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import invtznClient from '@/core/api/invtznClient';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useToast } from 'vue-toastification';

const toast = useToast();
const authStore = useAuthStore();

const activeTab = ref('webhooks');
const webhookLogs = ref([]);
const systemLogs = ref([]);
const orderIdToForce = ref('');
const isLoading = ref(false);
const selectedPayload = ref('');
const selectedMetadata = ref('');

const isAdmin = computed(() => {
  return authStore.role === 'ADMIN' || authStore.user?.is_superuser === true;
});

const fetchLogs = async () => {
  try {
    const res = await invtznClient.get('webhook-logs/');
    webhookLogs.value = res.data.results || res.data;
  } catch (error) {
    console.error(error);
  }
};

const fetchSystemLogs = async () => {
  if (!isAdmin.value) return;
  try {
    const res = await invtznClient.get('system-logs/');
    systemLogs.value = res.data.results || res.data;
  } catch (error) {
    console.error('Error fetching system logs', error);
  }
};

const refreshCurrentLogs = () => {
  if (activeTab.value === 'webhooks') {
    fetchLogs();
  } else if (activeTab.value === 'system') {
    fetchSystemLogs();
  }
};

const viewPayload = (log) => {
  selectedPayload.value = JSON.stringify(log.payload, null, 2);
  document.getElementById('payload_modal').showModal();
};

const viewMetadata = (log) => {
  selectedMetadata.value = JSON.stringify(log.metadata, null, 2);
  document.getElementById('metadata_modal').showModal();
};

const forceActivation = async () => {
  isLoading.value = true;
  try {
    const res = await invtznClient.post(`orders/${orderIdToForce.value}/force-activation/`);
    toast.success(res.data.message || 'Orden activada con éxito');
    orderIdToForce.value = '';
  } catch (error) {
    toast.error(error.response?.data?.error || 'Error al forzar activación');
  } finally {
    isLoading.value = false;
  }
};

watch(activeTab, (newTab) => {
  if (newTab === 'system') {
    fetchSystemLogs();
  } else {
    fetchLogs();
  }
});

onMounted(() => {
  fetchLogs();
  if (isAdmin.value && activeTab.value === 'system') {
    fetchSystemLogs();
  }
});
</script>
