<template>
  <div class="@container py-10 sm:py-12 px-4 sm:px-6 max-w-6xl mx-auto space-y-6 sm:space-y-8 bg-white/40 backdrop-blur-md rounded-[2rem] sm:rounded-[2.5rem] border border-slate-100/50 shadow-xl my-4 sm:my-6 text-center">
    <div class="space-y-2">
      <div class="flex justify-center">
        <img v-if="config.icon && isUrl(config.icon)" :src="config.icon" class="w-10 h-10 sm:w-12 sm:h-12 object-contain" alt="icon" />
        <span v-else class="text-3xl sm:text-4xl block select-none">{{ config.icon || '📍' }}</span>
      </div>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-800 tracking-tight px-2">
        {{ config.title || 'Ubicaciones del Evento' }}
      </h2>
    </div>

    <!-- Si solo hay 1 ubicación, diseño centrado -->
    <div v-if="activeLocations.length === 1" class="mt-8 max-w-2xl mx-auto">
      <div v-for="loc in activeLocations" :key="loc.id || loc.type" class="bg-white/80 p-5 sm:p-8 rounded-[1.5rem] sm:rounded-[2rem] border border-slate-100 shadow-sm flex flex-col justify-between space-y-6">
        <div class="space-y-2 sm:space-y-3">
          <span class="text-[10px] sm:text-xs font-black uppercase tracking-widest text-indigo-500">{{ loc.title }}</span>
          <h3 v-if="loc.venueName" class="text-lg sm:text-xl font-black text-slate-800 leading-snug">{{ loc.venueName }}</h3>
          <p v-if="loc.address" class="text-xs sm:text-sm text-slate-500 leading-relaxed">{{ loc.address }}</p>
        </div>

        <div class="w-full">
          <div v-if="getEmbedUrl(loc)" class="relative w-full h-[220px] sm:h-[280px] rounded-xl sm:rounded-2xl overflow-hidden border border-slate-200/50 shadow-inner bg-slate-100">
            <iframe :src="getEmbedUrl(loc)" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
          <div v-else class="flex flex-col items-center justify-center p-6 bg-slate-50 rounded-2xl border border-dashed border-slate-300">
            <span class="text-2xl mb-1">🗺️</span>
            <p class="text-xs font-bold text-slate-500">Configura esta ubicación en el editor para mostrar el mapa.</p>
          </div>
        </div>

        <div v-if="loc.googleMapsUrl" class="pt-2">
          <a :href="loc.googleMapsUrl" target="_blank" class="btn btn-primary inline-flex items-center gap-2 px-6 py-3 sm:py-4 text-white font-extrabold rounded-xl shadow-sm hover:shadow-md transition-all text-[11px] sm:text-xs w-full justify-center">
            <span>🗺️</span> Cómo llegar
          </a>
        </div>
      </div>
    </div>

    <!-- Si hay múltiples, carrusel swipeable en móvil y grid en desktop -->
    <div v-else class="mt-8 flex @md:grid @md:grid-cols-2 gap-4 sm:gap-6 overflow-x-auto overflow-y-hidden snap-x snap-mandatory pb-6 pt-2 hide-scrollbar w-full" style="-ms-overflow-style: none; scrollbar-width: none; scroll-padding-left: 1rem;">
      <div v-for="loc in activeLocations" :key="loc.id || loc.type" class="shrink-0 w-[280px] sm:w-[320px] @md:w-full max-w-full snap-center @md:snap-align-none bg-white/80 p-5 sm:p-6 @md:p-8 rounded-[1.5rem] sm:rounded-[2rem] border border-slate-100 shadow-sm flex flex-col justify-between space-y-5">
        <div class="space-y-2 sm:space-y-3">
          <span class="text-[10px] sm:text-xs font-black uppercase tracking-widest text-indigo-500">{{ loc.title }}</span>
          <h3 v-if="loc.venueName" class="text-lg sm:text-xl font-black text-slate-800 leading-snug">{{ loc.venueName }}</h3>
          <p v-if="loc.address" class="text-xs sm:text-sm text-slate-500 leading-relaxed">{{ loc.address }}</p>
        </div>

        <div class="w-full mt-4 @md:mt-auto">
          <div v-if="getEmbedUrl(loc)" class="relative w-full h-[220px] sm:h-[260px] rounded-xl sm:rounded-2xl overflow-hidden border border-slate-200/50 shadow-inner bg-slate-100">
            <iframe :src="getEmbedUrl(loc)" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
          <div v-else class="flex flex-col items-center justify-center p-6 bg-slate-50 rounded-2xl border border-dashed border-slate-300">
            <span class="text-2xl mb-1">🗺️</span>
            <p class="text-[10px] sm:text-xs font-bold text-slate-500">Configura esta ubicación en el editor para mostrar el mapa.</p>
          </div>
        </div>

        <div v-if="loc.googleMapsUrl" class="pt-3">
          <a :href="loc.googleMapsUrl" target="_blank" class="btn btn-primary inline-flex items-center gap-2 px-6 py-3 sm:py-4 text-white font-extrabold rounded-xl shadow-sm hover:shadow-md transition-all text-[11px] sm:text-xs w-full justify-center">
            <span>🗺️</span> Cómo llegar
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      title: 'Ubicación del Evento',
      venueName: '',
      address: '',
      googleMapsUrl: '',
      zoom: 14,
      locations: null,
      locationsList: [],
      icon: ''
    })
  }
});

const isUrl = (val) => {
  if (!val) return false;
  return val.startsWith('http') || val.startsWith('/') || val.startsWith('.') || val.includes('/');
};

const activeLocations = computed(() => {
  if (props.config.locationsList && props.config.locationsList.length > 0) {
    return props.config.locationsList.filter(l => l.isActive);
  }

  // Fallback para invitaciones antiguas
  const list = [];
  const locs = props.config.locations;
  
  if (locs) {
    if (locs.ceremonyName || locs.ceremonyMapsUrl) {
      list.push({
        id: 'legacy_ceremony',
        isActive: true,
        title: '⛪ Ceremonia',
        venueName: locs.ceremonyName || 'Ceremonia',
        address: '',
        googleMapsUrl: locs.ceremonyMapsUrl || '',
        zoom: props.config.zoom || 14
      });
    }
    if (locs.receptionName || locs.receptionMapsUrl) {
      list.push({
        id: 'legacy_reception',
        isActive: true,
        title: '🥂 Recepción / Fiesta',
        venueName: locs.receptionName || 'Recepción / Fiesta',
        address: '',
        googleMapsUrl: locs.receptionMapsUrl || '',
        zoom: props.config.zoom || 14
      });
    }
  }
  
  // Fallback para ubicación general única si no hay ceremonia/recepción definidas
  if (list.length === 0 && (props.config.venueName || props.config.googleMapsUrl || props.config.address)) {
    list.push({
      id: 'legacy_general',
      isActive: true,
      title: '📍 Evento',
      venueName: props.config.venueName || '',
      address: props.config.address || '',
      googleMapsUrl: props.config.googleMapsUrl || '',
      zoom: props.config.zoom || 14
    });
  }
  
  return list;
});

const getEmbedUrl = (loc) => {
  // Mejoramos la geoposición separando el nombre y la dirección con coma para Google Maps
  let query = '';
  if (loc.venueName && loc.address) {
    query = `${loc.venueName}, ${loc.address}`;
  } else if (loc.address) {
    query = loc.address;
  } else if (loc.venueName) {
    query = loc.venueName;
  }

  query = query.trim();
  if (!query) return '';
  
  // Si accidentalmente pegaron un iframe en el nombre o dirección
  if (query.includes('google.com/maps/embed') || query.includes('<iframe')) {
    if (query.includes('<iframe')) {
      const match = query.match(/src="([^"]+)"/);
      return match ? match[1] : query;
    }
    return query;
  }
  
  const zoomVal = loc.zoom || 14;
  return `https://maps.google.com/maps?q=${encodeURIComponent(query)}&z=${zoomVal}&output=embed`;
};
</script>
