<template>
  <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full">
    <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
      <h3 class="font-black text-slate-800 text-xs uppercase tracking-widest">🏦 Movimientos Bancarios</h3>
      <button class="btn btn-ghost btn-xs text-primary" @click="$emit('simulate')" :disabled="loading">
        Simular Depósito
      </button>
    </div>
    
    <div class="flex-1 overflow-y-auto">
      <div v-if="loading" class="p-8 text-center">
        <span class="loading loading-spinner text-primary"></span>
      </div>
      <div v-else-if="logs.length === 0" class="p-8 text-center text-slate-400 italic text-sm">
        No hay movimientos bancarios registrados.
      </div>
      <div v-else class="divide-y divide-slate-50">
        <div 
          v-for="log in logs" 
          :key="log.id" 
          class="p-4 hover:bg-slate-50 transition-colors cursor-pointer group"
          :class="{ 'opacity-50 grayscale bg-slate-100': log.is_reconciled, 'border-l-4 border-primary': !log.is_reconciled && isSelected(log) }"
          @click="!log.is_reconciled && $emit('select', log)"
        >
          <div class="flex justify-between items-start mb-1">
            <span class="font-black text-slate-900">${{ log.amount }}</span>
            <span v-if="log.is_reconciled" class="badge badge-success badge-xs text-white font-bold">Conciliado</span>
            <span v-else class="text-[10px] font-bold text-slate-400">{{ formatDate(log.timestamp) }}</span>
          </div>
          <div class="text-xs font-bold text-slate-600 truncate">{{ log.sender_name }}</div>
          <div class="text-[10px] text-slate-400 mt-1 uppercase tracking-wider font-medium">Ref: {{ log.external_id }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['logs', 'loading', 'selectedId']);
defineEmits(['select', 'simulate']);

const isSelected = (log) => props.selectedId === log.id;

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>
