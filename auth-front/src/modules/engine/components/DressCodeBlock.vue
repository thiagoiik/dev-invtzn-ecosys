<template>
  <div 
    v-if="config && config.type"
    class="py-12 px-6 max-w-4xl mx-auto space-y-6 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6 text-center"
  >
    <div class="space-y-4">
      <span class="text-4xl block">👗👔</span>
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">
        Código de Vestimenta
      </h2>
      <div class="inline-block bg-primary/10 text-primary font-black px-6 py-2 rounded-full uppercase tracking-wider text-sm">
        {{ dressCodeLabel }}
      </div>
      <p v-if="config.details" class="text-sm text-slate-500 max-w-md mx-auto leading-relaxed mt-2 whitespace-pre-line">
        {{ config.details }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      type: 'FORMAL',
      details: ''
    })
  }
});

const dressCodeLabel = computed(() => {
  const types = {
    'FORMAL': 'Formal',
    'ETIQUETA': 'Etiqueta / Gala',
    'COCKTAIL': 'Cóctel',
    'GUAYABERA': 'Guayabera / Clima Cálido',
    'CASUAL': 'Casual',
    'PLAYA': 'Playa'
  };
  return types[props.config.type] || props.config.type || 'Formal';
});
</script>
