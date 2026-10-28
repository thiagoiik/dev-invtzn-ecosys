<template>
  <div class="w-full max-w-md p-2 text-center space-y-6 animate-scale-in">
    <!-- Pulse Success Icon -->
    <div class="relative w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mx-auto shadow-inner">
      <div class="absolute inset-0 bg-emerald-100/40 rounded-full animate-ping"></div>
      <span class="text-4xl relative z-10">✨</span>
    </div>

    <!-- Text Information -->
    <div class="space-y-3">
      <h3 class="text-2xl font-black text-slate-900 leading-tight">
        {{ title }}
      </h3>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">
        {{ message }}
      </p>
    </div>

    <!-- Action Section -->
    <div class="pt-6 border-t border-slate-50 flex flex-col gap-3">
      <!-- Add to Calendar Link if Attending -->
      <a 
        v-if="attending" 
        :href="calendarUrl" 
        target="_blank"
        class="btn btn-primary rounded-2xl h-14 font-black shadow-lg shadow-primary/20 flex items-center justify-center gap-2"
      >
        📅 Agendar en mi Calendario
      </a>
      <p class="text-[9px] font-black text-slate-300 uppercase tracking-[0.2em]">
        Invitazyon Digital Luxury
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
  attending: { type: Boolean, required: true },
  fullName: { type: String, required: true },
  eventTitle: { type: String, default: 'El Gran Día' },
  eventDate: { type: String, default: '2026-12-25T18:00:00' }
});

const title = computed(() => {
  return props.attending ? '¡Asistencia Confirmada!' : 'Gracias por avisar';
});

const message = computed(() => {
  return props.attending 
    ? `¡Excelente noticia, ${props.fullName}! Hemos registrado que nos acompañarás en este momento tan especial.` 
    : `Lamentamos que no puedas asistir, ${props.fullName}. Agradecemos mucho que te hayas tomado el tiempo de avisarnos.`;
});

// Creates a basic Google Calendar invitation link
const calendarUrl = computed(() => {
  const base = 'https://calendar.google.com/calendar/render?action=TEMPLATE';
  const text = encodeURIComponent(`Boda: ${props.eventTitle}`);
  // Parse date to basic standard format YYYYMMDDTHHMMSSZ (simplified here)
  const dateStr = props.eventDate.replace(/[-:]/g, '');
  const dates = `${dateStr}/${dateStr}`;
  const details = encodeURIComponent('¡Te esperamos para celebrar juntos!');
  
  return `${base}&text=${text}&dates=${dates}&details=${details}`;
});
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
</style>
