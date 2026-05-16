<template>
  <div class="bg-slate-900 rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden">
    <!-- Background Decor -->
    <div class="absolute -top-24 -right-24 w-64 h-64 bg-primary/20 rounded-full blur-3xl"></div>
    <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl"></div>

    <div class="relative z-10 flex flex-col md:flex-row gap-8 items-center justify-between">
      <div class="flex-1 space-y-4">
        <h3 class="text-2xl font-black uppercase tracking-tighter">Match de Conciliación</h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Banco -->
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <p class="text-[10px] font-black text-primary uppercase tracking-widest mb-1">Movimiento Banco</p>
            <div v-if="selectedLog" class="animate-in fade-in slide-in-from-left-2">
              <p class="text-xl font-black">${{ selectedLog.amount }}</p>
              <p class="text-xs text-slate-400 font-medium truncate">{{ selectedLog.sender_name }}</p>
            </div>
            <p v-else class="text-sm text-slate-500 italic">Selecciona un depósito...</p>
          </div>

          <!-- Orden -->
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            <p class="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">Orden Pendiente</p>
            <div v-if="selectedOrder" class="animate-in fade-in slide-in-from-right-2">
              <p class="text-xl font-black">${{ selectedOrder.total_amount }}</p>
              <p class="text-xs text-slate-400 font-medium">Orden #{{ selectedOrder.id }}</p>
            </div>
            <p v-else class="text-sm text-slate-500 italic">Selecciona una orden...</p>
          </div>
        </div>

        <!-- Alerta de coincidencia -->
        <div v-if="matchAlert" :class="['p-3 rounded-xl text-center font-bold text-xs animate-bounce', matchAlert.class]">
          {{ matchAlert.text }}
        </div>
      </div>

      <div class="w-full md:w-auto">
        <button 
          class="btn btn-primary btn-lg w-full md:w-48 h-20 text-lg font-black uppercase tracking-widest shadow-xl shadow-primary/20"
          :disabled="!canSync || loading"
          @click="$emit('sync')"
        >
          <span v-if="loading" class="loading loading-spinner"></span>
          Cruzar Pago
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps(['selectedLog', 'selectedOrder', 'loading']);
defineEmits(['sync']);

const canSync = computed(() => {
  return props.selectedLog && props.selectedOrder;
});

const matchAlert = computed(() => {
  if (!props.selectedLog || !props.selectedOrder) return null;
  
  const logAmount = parseFloat(props.selectedLog.amount);
  const orderAmount = parseFloat(props.selectedOrder.total_amount);

  if (logAmount === orderAmount) {
    return { text: '¡Coincidencia Exacta!', class: 'bg-green-500/20 text-green-400' };
  } else if (logAmount > orderAmount) {
    return { text: 'Monto superior al de la orden', class: 'bg-yellow-500/20 text-yellow-400' };
  } else {
    return { text: 'El depósito es menor a la orden (No permitido)', class: 'bg-error/20 text-error' };
  }
});
</script>
