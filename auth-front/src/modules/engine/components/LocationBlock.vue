<template>
  <div class="py-12 px-6 max-w-6xl mx-auto space-y-8 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6 text-center">
    <div class="space-y-2">
      <span class="text-4xl block">📍</span>
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">
        {{ config.title || 'Ubicaciones del Evento' }}
      </h2>
    </div>

    <div :class="[
      'grid gap-8 mt-8',
      activeLocations.length > 1 ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1 max-w-2xl mx-auto'
    ]">
      <div v-for="loc in activeLocations" :key="loc.type" class="bg-white/80 p-6 sm:p-8 rounded-[2rem] border border-slate-100 shadow-sm flex flex-col justify-between space-y-6">
        <div class="space-y-3">
          <span class="text-xs font-black uppercase tracking-widest text-indigo-500">{{ loc.title }}</span>
          <h3 v-if="loc.venueName" class="text-xl font-black text-slate-800 leading-snug">{{ loc.venueName }}</h3>
          <p v-if="loc.address" class="text-sm text-slate-500 leading-relaxed">{{ loc.address }}</p>
        </div>

        <!-- Map Container -->
        <div class="w-full">
          <div v-if="getEmbedUrl(loc)" class="relative w-full h-[240px] sm:h-[280px] rounded-2xl overflow-hidden border border-slate-200/50 shadow-inner">
            <iframe
              :src="getEmbedUrl(loc)"
              width="100%"
              height="100%"
              style="border:0;"
              allowfullscreen=""
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
          <div v-else class="flex flex-col items-center justify-center p-6 bg-slate-50 rounded-2xl border border-dashed border-slate-300">
            <span class="text-2xl mb-1">🗺️</span>
            <p class="text-xs font-bold text-slate-500">Configura esta ubicación en el editor para mostrar el mapa.</p>
          </div>
        </div>

        <!-- Link Button -->
        <div v-if="loc.googleMapsUrl" class="pt-2">
          <a 
            :href="loc.googleMapsUrl" 
            target="_blank"
            class="btn btn-primary inline-flex items-center gap-2 px-6 py-3 text-white font-extrabold rounded-xl shadow-sm hover:shadow-md transition-all text-xs w-full justify-center"
          >
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
      locations: null
    })
  }
});

const activeLocations = computed(() => {
  const list = [];
  const locs = props.config.locations;
  
  if (locs) {
    if (locs.ceremonyName || locs.ceremonyMapsUrl) {
      list.push({
        type: 'ceremony',
        title: '⛪ Ceremonia',
        venueName: locs.ceremonyName || 'Ceremonia',
        address: '',
        googleMapsUrl: locs.ceremonyMapsUrl || '',
        zoom: props.config.zoom || 14
      });
    }
    if (locs.receptionName || locs.receptionMapsUrl) {
      list.push({
        type: 'reception',
        title: '🥂 Recepción / Fiesta',
        venueName: locs.receptionName || 'Recepción / Fiesta',
        address: '',
        googleMapsUrl: locs.receptionMapsUrl || '',
        zoom: props.config.zoom || 14
      });
    }
  }
  
  // Fallback to legacy single general location if no ceremony/reception defined
  if (list.length === 0 && (props.config.venueName || props.config.googleMapsUrl || props.config.address)) {
    list.push({
      type: 'general',
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
  let query = loc.venueName || '';
  if (loc.address) {
    query += ' ' + loc.address;
  }
  query = query.trim();
  if (!query) return '';
  
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
