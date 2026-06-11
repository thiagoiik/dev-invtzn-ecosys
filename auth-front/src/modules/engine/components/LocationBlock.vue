<template>
  <div class="py-12 px-6 max-w-4xl mx-auto space-y-8 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6 text-center">
    <div class="space-y-2">
      <span class="text-4xl block">📍</span>
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">
        {{ config.title || 'Ubicación' }}
      </h2>
      <div v-if="config.venueName" class="text-lg font-extrabold text-slate-800/90 mt-4">
        {{ config.venueName }}
      </div>
      <p v-if="config.address" class="text-sm text-slate-500 max-w-md mx-auto leading-relaxed mt-1">
        {{ config.address }}
      </p>
    </div>

    <!-- Map Container -->
    <div class="w-full">
      <div v-if="embedUrl" class="relative w-full h-[280px] sm:h-[380px] rounded-3xl overflow-hidden border border-slate-200/50 shadow-md">
        <iframe
          :src="embedUrl"
          width="100%"
          height="100%"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>
      <div v-else class="flex flex-col items-center justify-center p-8 bg-slate-50 rounded-3xl border border-dashed border-slate-300">
        <span class="text-3xl mb-2">🗺️</span>
        <p class="text-sm font-bold text-slate-500">Configura el nombre del lugar y dirección en el editor para mostrar el mapa aquí.</p>
      </div>
    </div>

    <!-- Button to open in external maps -->
    <div v-if="config.googleMapsUrl" class="pt-2">
      <a 
        :href="config.googleMapsUrl" 
        target="_blank"
        class="btn btn-primary inline-flex items-center gap-2 px-8 py-3.5 text-white font-extrabold rounded-2xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all text-sm"
      >
        <span>🗺️</span> Ver en Google Maps / Cómo llegar
      </a>
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
      zoom: 14
    })
  }
});

const embedUrl = computed(() => {
  const venue = props.config.venueName || '';
  const addr = props.config.address || '';
  const query = `${venue} ${addr}`.trim();
  
  if (!query) return '';
  
  // If it's already an embed link (e.g. starts with iframe or maps embed)
  if (query.includes('google.com/maps/embed') || query.includes('<iframe')) {
    if (query.includes('<iframe')) {
      const match = query.match(/src="([^"]+)"/);
      return match ? match[1] : query;
    }
    return query;
  }
  
  const zoomVal = props.config.zoom || 14;
  return `https://maps.google.com/maps?q=${encodeURIComponent(query)}&z=${zoomVal}&output=embed`;
});
</script>
