<template>
  <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full">
    <div class="p-4 border-b border-slate-100 bg-slate-50">
      <h3 class="font-black text-slate-800 text-xs uppercase tracking-widest">⏳ Órdenes Pendientes</h3>
    </div>
    
    <div class="flex-1 overflow-y-auto">
      <div v-if="loading" class="p-8 text-center">
        <span class="loading loading-spinner text-primary"></span>
      </div>
      <div v-else-if="orders.length === 0" class="p-8 text-center text-slate-400 italic text-sm">
        No hay órdenes pendientes de pago.
      </div>
      <div v-else class="divide-y divide-slate-50">
        <div 
          v-for="order in orders" 
          :key="order.id" 
          class="p-4 hover:bg-slate-50 transition-colors cursor-pointer group"
          :class="{ 'border-l-4 border-primary bg-primary/5': isSelected(order) }"
          @click="$emit('select', order)"
        >
          <div class="flex justify-between items-start mb-1">
            <span class="font-black text-slate-900">#{{ order.id }} - ${{ order.total_amount }}</span>
            <span class="text-[10px] font-bold text-slate-400">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="text-xs font-bold text-slate-600 truncate">User ID: {{ order.user }}</div>
          <div class="flex gap-1 mt-2">
            <div class="badge badge-ghost badge-xs font-black">{{ order.origin }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['orders', 'loading', 'selectedId']);
defineEmits(['select']);

const isSelected = (order) => props.selectedId === order.id;

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>
