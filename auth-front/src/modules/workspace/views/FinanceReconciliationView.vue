<template>
  <div class="space-y-6 flex flex-col h-[calc(100vh-12rem)]">
    <!-- Header -->
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Conciliación Bancaria</h2>
        <p class="text-slate-500">Cruce de depósitos bancarios con órdenes pendientes.</p>
      </div>
      <div class="stats bg-slate-50 border border-slate-100 shadow-none">
        <div class="stat py-1">
          <div class="stat-title text-[10px] font-black uppercase text-slate-400">Por Conciliar</div>
          <div class="stat-value text-xl text-primary">{{ pendingOrders.length }}</div>
        </div>
      </div>
    </div>

    <!-- Matcher Section (Magic Button) -->
    <ReconciliationMatcher 
      :selected-log="selectedLog" 
      :selected-order="selectedOrder" 
      :loading="syncing"
      @sync="handleSync"
    />

    <!-- Comparison Grid -->
    <div class="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-0">
      <BankSyncLogViewer 
        :logs="bankLogs" 
        :loading="loadingLogs" 
        :selected-id="selectedLog?.id"
        @select="selectedLog = $event"
        @simulate="simulateDeposit"
      />
      
      <PendingOrdersList 
        :orders="pendingOrders" 
        :loading="loadingOrders" 
        :selected-id="selectedOrder?.id"
        @select="selectedOrder = $event"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { crmService } from '@/modules/workspace/services/crmService';
import BankSyncLogViewer from '../components/BankSyncLogViewer.vue';
import PendingOrdersList from '../components/PendingOrdersList.vue';
import ReconciliationMatcher from '../components/ReconciliationMatcher.vue';

const toast = useToast();

const bankLogs = ref([]);
const pendingOrders = ref([]);

const loadingLogs = ref(true);
const loadingOrders = ref(true);
const syncing = ref(false);

const selectedLog = ref(null);
const selectedOrder = ref(null);

const fetchData = async () => {
  loadingLogs.value = true;
  loadingOrders.value = true;
  try {
    const [logsRes, ordersRes] = await Promise.all([
      crmService.fetchBankLogs(),
      crmService.fetchPendingOrders()
    ]);
    bankLogs.value = logsRes.data;
    pendingOrders.value = ordersRes.data;
  } catch (e) {
    toast.error('Error al cargar datos financieros');
  } finally {
    loadingLogs.value = false;
    loadingOrders.value = false;
  }
};

const simulateDeposit = async () => {
  try {
    const amount = prompt('Ingrese el monto a simular:', '100.00');
    if (!amount) return;
    await crmService.simulateBankWebhook(parseFloat(amount));
    toast.success('Simulación de depósito exitosa');
    fetchData();
  } catch (e) {
    toast.error('Error en simulación');
  }
};

const handleSync = async () => {
  if (!selectedLog.value || !selectedOrder.value) return;
  syncing.value = true;
  try {
    await crmService.syncOrderWithBank(selectedLog.value.id, selectedOrder.value.id);
    toast.success('¡Conciliación completada!');
    selectedLog.value = null;
    selectedOrder.value = null;
    fetchData();
  } catch (e) {
    const msg = e.response?.data?.error || 'Error en conciliación';
    toast.error(msg);
  } finally {
    syncing.value = false;
  }
};

onMounted(fetchData);
</script>
