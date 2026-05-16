<template>
  <div class="py-24 bg-slate-50 flex flex-col items-center px-6">
    <div class="max-w-xl w-full">
      <!-- Section Header -->
      <header class="text-center space-y-2 mb-16">
        <span class="text-[10px] font-black text-amber-500 uppercase tracking-[0.4em]">Itinerario</span>
        <h2 class="text-3xl md:text-4xl font-serif font-bold text-slate-900">
          {{ config.title || 'Cronograma del Evento' }}
        </h2>
        <div class="w-12 h-[1px] bg-slate-200 mx-auto mt-4"></div>
      </header>

      <!-- Vertical Interactive Timeline -->
      <div class="relative pl-8 md:pl-10 space-y-12">
        <!-- Center connecting Line -->
        <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-slate-200"></div>

        <!-- Timeline Items -->
        <div 
          v-for="(item, idx) in schedule" 
          :key="idx" 
          class="relative flex flex-col space-y-2 animate-fade-in group cursor-pointer"
        >
          <!-- Bullet Node Icon Circle -->
          <div class="absolute -left-8 md:-left-10 w-9 h-9 rounded-full bg-white border-2 border-primary flex items-center justify-center text-sm shadow-md transition-all duration-300 group-hover:scale-110 group-hover:bg-primary group-hover:text-white">
            {{ item.icon || '✨' }}
          </div>

          <!-- Time Frame & Event Header -->
          <div class="flex items-baseline gap-3">
            <span class="text-sm font-black text-primary font-mono tracking-tight">{{ item.time }}</span>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-primary transition-colors">
              {{ item.title }}
            </h3>
          </div>

          <!-- Description -->
          <p class="text-sm text-slate-500 font-medium leading-relaxed">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});

// Default Timeline schedule fallback if not provided in custom_data
const defaultSchedule = [
  { time: '17:00', title: 'Ceremonia de Boda', description: 'Bajo el gran árbol del jardín principal.', icon: '💍' },
  { time: '18:30', title: 'Cóctel de Bienvenida', description: 'Bebidas selectas y bocadillos en la terraza.', icon: '🥂' },
  { time: '20:00', title: 'Banquete & Cena', description: 'Cena de gala de 3 tiempos en el salón majestuoso.', icon: '🍽️' },
  { time: '22:00', title: 'Apertura de Pista', description: '¡Baile, diversión y sorpresas hasta el amanecer!', icon: '🕺' }
];

const schedule = computed(() => {
  return props.config.schedule || defaultSchedule;
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}
</style>
