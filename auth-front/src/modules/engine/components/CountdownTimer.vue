<template>
  <div class="py-20 bg-white flex flex-col items-center justify-center px-6">
    <div class="max-w-xl w-full text-center space-y-8">
      <!-- Section Header -->
      <header class="space-y-2">
        <span class="text-[10px] font-black text-amber-500 uppercase tracking-[0.4em]">Falta muy poco</span>
        <h2 class="text-3xl md:text-4xl font-serif font-bold text-slate-900">
          {{ config.title || 'Cuenta Regresiva' }}
        </h2>
        <div class="w-12 h-[1px] bg-slate-200 mx-auto mt-4"></div>
      </header>

      <!-- Timer Grid -->
      <div class="grid grid-cols-4 gap-4 md:gap-6 pt-4">
        <div 
          v-for="(val, unit) in timeRemaining" 
          :key="unit"
          class="bg-slate-50 border border-slate-100 rounded-3xl p-4 md:p-6 shadow-sm hover:shadow-md transition-shadow"
        >
          <!-- Value Display -->
          <div class="text-3xl md:text-5xl font-black text-slate-800 font-mono tracking-tighter">
            {{ formatNumber(val) }}
          </div>
          <!-- Unit Label -->
          <div class="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-2">
            {{ unitLabels[unit] }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, defineProps } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});

const targetDate = new Date(props.config.targetDate || '2026-12-25T18:00:00');
const timeRemaining = ref({ days: 0, hours: 0, minutes: 0, seconds: 0 });
let timerInterval = null;

const unitLabels = {
  days: 'Días',
  hours: 'Horas',
  minutes: 'Min.',
  seconds: 'Seg.'
};

const formatNumber = (num) => {
  return num.toString().padStart(2, '0');
};

const updateTimer = () => {
  const now = new Date();
  const diff = targetDate - now;

  if (diff <= 0) {
    timeRemaining.value = { days: 0, hours: 0, minutes: 0, seconds: 0 };
    if (timerInterval) clearInterval(timerInterval);
    return;
  }

  timeRemaining.value = {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / 1000 / 60) % 60),
    seconds: Math.floor((diff / 1000) % 60)
  };
};

onMounted(() => {
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
});

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}
</style>
