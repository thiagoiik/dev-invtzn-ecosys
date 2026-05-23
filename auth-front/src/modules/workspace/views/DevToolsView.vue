<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold text-white tracking-tight">Herramientas de Desarrollador</h1>
      <div class="flex gap-2">
        <button @click="fetchLogs" class="btn btn-outline border-slate-700 text-slate-300">
          <i class="fas fa-sync-alt mr-2"></i> Refrescar Logs
        </button>
      </div>
    </div>

    <!-- Webhook Logs -->
    <div class="card bg-slate-800/50 border border-slate-700">
      <div class="card-body">
        <h2 class="card-title text-xl text-white mb-4">
          <i class="fas fa-satellite-dish text-indigo-400 mr-2"></i> Visor de Webhooks (Stripe)
        </h2>
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr class="text-slate-400 border-b border-slate-700">
                <th>Fecha</th>
                <th>Proveedor</th>
                <th>Estado</th>
                <th>Mensaje</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in webhookLogs" :key="log.id" class="border-b border-slate-700 hover:bg-slate-800/80 transition-colors">
                <td class="text-slate-300">{{ new Date(log.created_at).toLocaleString() }}</td>
                <td><span class="badge badge-outline badge-primary">{{ log.provider }}</span></td>
                <td>
                  <span class="badge" :class="{
                    'badge-success': log.status === 'success',
                    'badge-error': log.status === 'failed',
                    'badge-warning': log.status === 'received'
                  }">{{ log.status }}</span>
                </td>
                <td class="text-slate-400 truncate max-w-xs">{{ log.message }}</td>
                <td>
                  <button @click="viewPayload(log)" class="btn btn-sm btn-ghost text-indigo-400">Ver Payload</button>
                </td>
              </tr>
              <tr v-if="webhookLogs.length === 0">
                <td colspan="5" class="text-center text-slate-500 py-8">No se han recibido webhooks aún.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Simulador de Pagos -->
    <div class="card bg-slate-800/50 border border-slate-700">
      <div class="card-body">
        <h2 class="card-title text-xl text-white mb-4">
          <i class="fas fa-magic text-fuchsia-400 mr-2"></i> Simular Activación de Orden
        </h2>
        <p class="text-slate-400 text-sm mb-4">Forza el pago y la activación de una orden que se quedó pendiente porque el webhook no llegó.</p>
        <div class="flex gap-4 items-center">
          <div class="form-control flex-1 max-w-xs">
            <input v-model="orderIdToForce" type="number" placeholder="ID de la Orden" class="input input-bordered bg-slate-900 border-slate-700 text-white w-full" />
          </div>
          <button @click="forceActivation" :disabled="!orderIdToForce || isLoading" class="btn btn-primary">
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            Forzar Pago y Activación
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Payload -->
    <dialog id="payload_modal" class="modal">
      <div class="modal-box bg-slate-800 border border-slate-700 w-11/12 max-w-5xl">
        <h3 class="font-bold text-lg text-white mb-4">Payload del Webhook</h3>
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-700 overflow-x-auto">
          <pre class="text-green-400 text-sm"><code>{{ selectedPayload }}</code></pre>
        </div>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn btn-outline text-slate-300 border-slate-600">Cerrar</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import invtznClient from '@/core/api/invtznClient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const webhookLogs = ref([]);
const orderIdToForce = ref('');
const isLoading = ref(false);
const selectedPayload = ref('');

const fetchLogs = async () => {
  try {
    const res = await invtznClient.get('integrations/webhook-logs/');
    webhookLogs.value = res.data.results || res.data;
  } catch (error) {
    console.error(error);
  }
};

const viewPayload = (log) => {
  selectedPayload.value = JSON.stringify(log.payload, null, 2);
  document.getElementById('payload_modal').showModal();
};

const forceActivation = async () => {
  isLoading.value = true;
  try {
    const res = await invtznClient.post(`sales/orders/${orderIdToForce.value}/force-activation/`);
    toast.success(res.data.message || 'Orden activada con éxito');
    orderIdToForce.value = '';
  } catch (error) {
    toast.error(error.response?.data?.error || 'Error al forzar activación');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchLogs();
});
</script>
