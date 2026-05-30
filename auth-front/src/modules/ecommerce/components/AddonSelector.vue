<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h4 class="text-lg font-bold text-slate-900 flex items-center gap-2">
        <span>Personaliza con Add-ons</span>
        <span class="badge badge-sm badge-outline text-slate-400">Opcional</span>
      </h4>
    </div>

    <div class="grid grid-cols-1 gap-4">
      <div v-for="addon in addons" :key="addon.id" 
        class="group relative flex items-center gap-4 p-4 rounded-2xl border-2 transition-all cursor-pointer"
        :class="isSelected(addon.id) ? 'border-primary bg-primary/5' : 'border-slate-100 hover:border-slate-200 bg-white'"
        @click="toggleAddon(addon)"
      >
        <div class="flex-shrink-0 w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-700 group-hover:scale-110 transition-transform" v-html="getAddonIcon(addon.name)">
        </div>
        
        <div class="flex-1 min-w-0">
          <h5 class="font-bold text-slate-800 truncate text-sm">{{ addon.name }}</h5>
          <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed mt-0.5">{{ getAddonDescription(addon.name, addon.description) }}</p>
        </div>

        <div class="text-right flex-shrink-0 pl-2">
          <div class="font-black text-slate-900 text-sm">+${{ addon.base_price }}</div>
          <div class="text-[9px] text-slate-400 font-bold uppercase tracking-widest mt-0.5">MXN</div>
        </div>

        <!-- Checkmark Overlay -->
        <div v-if="isSelected(addon.id)" class="absolute -top-2 -right-2 bg-primary text-white rounded-full p-1 shadow-lg shadow-primary/45">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

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

const getAddonDescription = (name, dbDesc) => {
  if (dbDesc && dbDesc !== 'Mejora tu experiencia digital.') return dbDesc;
  const n = name.toLowerCase();
  if (n.includes('whatsapp')) return 'Notificaciones automáticas y recordatorios directos a tus invitados.';
  if (n.includes('galería') || n.includes('fotos')) return 'Comparte tus mejores fotografías previas al gran día.';
  if (n.includes('mapa') || n.includes('ubicación')) return 'Guía a tus invitados con mapas interactivos de Google Maps.';
  if (n.includes('música') || n.includes('audio')) return 'Sube tu banda sonora y ambienta tu invitación personalizada.';
  if (n.includes('regalo') || n.includes('sobres')) return 'Facilita la entrega de obsequios y transferencias bancarias.';
  return 'Personalización y características premium adicionales.';
};

const getAddonIcon = (name) => {
  const n = name.toLowerCase();
  if (n.includes('whatsapp')) {
    return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>`;
  }
  if (n.includes('galería') || n.includes('fotos')) {
    return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>`;
  }
  if (n.includes('mapa') || n.includes('ubicación')) {
    return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>`;
  }
  if (n.includes('música') || n.includes('audio')) {
    return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>`;
  }
  if (n.includes('regalo') || n.includes('sobres')) {
    return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>`;
  }
  return `<svg class="w-5 h-5 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path></svg>`;
};
</script>
