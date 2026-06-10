<template>
  <div class="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950 text-white">
    <!-- Ken Burns Effect Zoom Background -->
    <div 
      class="absolute inset-0 bg-cover bg-center transition-transform duration-[20000ms] ease-out scale-110 hover:scale-100"
      :style="{ 
        backgroundImage: `url(${config.coverPhoto || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80'})`,
      }"
    ></div>
    
    <!-- Sophisticated Overlay Layer -->
    <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-slate-950/60"></div>

    <!-- Decorative Frame Overlay -->
    <div 
      v-if="config.frame_overlay" 
      class="absolute inset-0 pointer-events-none bg-contain bg-center bg-no-repeat z-[5]"
      :style="{ backgroundImage: `url(${config.frame_overlay})` }"
    ></div>

    <!-- Content Card -->
    <div class="relative z-10 text-center max-w-2xl px-6 space-y-8 animate-fade-in-up">
      <!-- Header Label -->
      <span class="text-xs font-black uppercase tracking-[0.4em] text-amber-400/90 drop-shadow-md">
        {{ config.headerLabel || 'Nuestra Invitación' }}
      </span>

      <!-- Main Custom Typography Title -->
      <h1 
        class="text-6xl md:text-7xl lg:text-8xl font-light leading-none drop-shadow-2xl font-serif text-white tracking-wide"
        :style="titleStyles"
      >
        {{ config.title || 'Ana & Luis' }}
      </h1>

      <div class="w-16 h-[1px] bg-gradient-to-r from-transparent via-amber-400 to-transparent mx-auto"></div>

      <!-- Subtitle Description -->
      <p 
        class="text-lg md:text-xl font-light tracking-wide text-slate-200/90 drop-shadow-md font-sans"
        :style="{ color: config.subtitleColor }"
      >
        {{ config.subtitle || '¡Nos casamos y queremos celebrar contigo!' }}
      </p>

      <!-- Date Display Box -->
      <div class="inline-block px-8 py-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md shadow-xl">
        <p class="text-xl md:text-2xl font-black uppercase tracking-[0.2em] text-white">
          {{ config.date || '25 DICIEMBRE 2026' }}
        </p>
      </div>
    </div>

    <!-- Scroll Down Elegant Indicator -->
    <div class="absolute bottom-10 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 opacity-60">
      <span class="text-[9px] font-black uppercase tracking-[0.3em] text-white/80">Deslizar</span>
      <div class="w-[20px] h-[34px] border-2 border-white/40 rounded-full flex items-start justify-center p-1">
        <div class="w-1.5 h-1.5 bg-amber-400 rounded-full animate-scroll-dot"></div>
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

const titleStyles = computed(() => {
  const styles = {};
  if (props.config.titleColor) styles.color = props.config.titleColor;
  if (props.config.fontFamily) styles.fontFamily = props.config.fontFamily;
  return styles;
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Great+Vibes&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}

.animate-fade-in-up {
  animation: fadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scrollDot {
  0% { transform: translateY(0); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(12px); opacity: 0; }
}

.animate-scroll-dot {
  animation: scrollDot 2s infinite ease-in-out;
}
</style>
