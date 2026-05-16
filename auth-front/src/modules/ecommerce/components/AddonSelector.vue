<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h4 class="text-lg font-bold text-slate-900 flex items-center gap-2">
        <span>✨ Personaliza con Add-ons</span>
        <span class="badge badge-sm badge-outline text-slate-400">Opcional</span>
      </h4>
    </div>

    <div class="grid grid-cols-1 gap-4">
      <div v-for="addon in addons" :key="addon.id" 
        class="group relative flex items-center gap-4 p-4 rounded-2xl border-2 transition-all cursor-pointer"
        :class="isSelected(addon.id) ? 'border-primary bg-primary/5' : 'border-slate-100 hover:border-slate-200 bg-white'"
        @click="toggleAddon(addon)"
      >
        <div class="flex-shrink-0 w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
          {{ getAddonEmoji(addon.name) }}
        </div>
        
        <div class="flex-1 min-w-0">
          <h5 class="font-bold text-slate-800 truncate">{{ addon.name }}</h5>
          <p class="text-xs text-slate-500 line-clamp-1">{{ addon.description || 'Mejora tu experiencia digital.' }}</p>
        </div>

        <div class="text-right flex-shrink-0">
          <div class="font-black text-slate-900">+${{ addon.base_price }}</div>
          <div class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">MXN</div>
        </div>

        <!-- Checkmark Overlay -->
        <div v-if="isSelected(addon.id)" class="absolute -top-2 -right-2 bg-primary text-white rounded-full p-1 shadow-lg shadow-primary/40">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
  addons: { type: Array, default: () => [] },
  selectedIds: { type: Array, default: () => [] }
});

const emit = defineEmits(['update:selectedIds']);

const toggleAddon = (addon) => {
  const index = props.selectedIds.indexOf(addon.id);
  const newSelection = [...props.selectedIds];
  
  if (index === -1) {
    newSelection.push(addon.id);
  } else {
    newSelection.splice(index, 1);
  }
  
  emit('update:selectedIds', newSelection);
};

const isSelected = (id) => props.selectedIds.includes(id);

const getAddonEmoji = (name) => {
  const n = name.toLowerCase();
  if (n.includes('whatsapp')) return '💬';
  if (n.includes('galería')) return '📸';
  if (n.includes('mapa')) return '📍';
  if (n.includes('música')) return '🎵';
  if (n.includes('regalo')) return '🎁';
  return '➕';
};
</script>
