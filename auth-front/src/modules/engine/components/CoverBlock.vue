<template>
  <div class="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950 text-white">
    <!-- Ken Burns Effect Zoom Background -->
    <div 
      class="absolute inset-0 bg-cover transition-transform duration-[20000ms] ease-out scale-110 hover:scale-100"
      :style="{ 
        backgroundImage: `url(${config.coverPhoto || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80'})`,
        backgroundPosition: `${(config.backgroundPositionX !== undefined && config.backgroundPositionX !== null) ? config.backgroundPositionX : 50}% ${(config.backgroundPositionY !== undefined && config.backgroundPositionY !== null) ? config.backgroundPositionY : 50}%`
      }"
    ></div>
    
    <!-- Sophisticated Overlay Layer -->
    <div 
      class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-slate-950/60"
      :style="{ opacity: (config.overlayOpacity !== undefined ? config.overlayOpacity : 70) / 100 }"
    ></div>

    <!-- Decorative Frame Overlay -->
    <div 
      v-if="config.frame_overlay" 
      class="absolute inset-0 pointer-events-none bg-[100%_100%] bg-no-repeat z-[5]"
      :style="{ backgroundImage: `url(${frameOverlayUrl})` }"
    ></div>

    <!-- Content Card -->
    <div class="relative z-10 text-center max-w-2xl px-6 space-y-8 animate-fade-in-up">
      <!-- Header Label -->
      <span 
        class="text-xs font-black uppercase tracking-[0.4em] drop-shadow-md"
        :class="[!config.headerLabelColor && 'text-amber-400/90']"
        :style="{ color: config.headerLabelColor }"
      >
        {{ config.headerLabel || 'Nuestra Invitación' }}
      </span>

      <!-- Main Custom Typography Title -->
      <h1 
        class="text-4xl sm:text-5xl md:text-7xl lg:text-8xl font-light leading-none drop-shadow-2xl font-serif tracking-wide break-words"
        :class="[!config.titleColor && 'text-white']"
        :style="titleStyles"
      >
        {{ config.title || 'Ana & Luis' }}
      </h1>

      <div class="w-16 h-[1px] bg-gradient-to-r from-transparent via-amber-400 to-transparent mx-auto"></div>

      <!-- Subtitle Description -->
      <p 
        class="text-lg md:text-xl font-light tracking-wide drop-shadow-md font-sans"
        :class="[!config.subtitleColor && 'text-slate-200/90']"
        :style="{ color: config.subtitleColor }"
      >
        {{ config.subtitle || '¡Nos casamos y queremos celebrar contigo!' }}
      </p>

      <!-- Date Display Box -->
      <div 
        class="inline-block px-8 py-4 rounded-2xl bg-white/5 border backdrop-blur-md shadow-xl"
        :style="dateBoxStyle"
      >
        <p 
          class="text-xl md:text-2xl font-black uppercase tracking-[0.2em]"
          :class="[!(config.subtitleColor || config.headerLabelColor) && 'text-white']"
          :style="{ color: config.subtitleColor || config.headerLabelColor }"
        >
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

const frameOverlayUrl = computed(() => {
  if (!props.config.frame_overlay) return '';
  // Append cache buster to force browser to reload the updated SVGs
  const separator = props.config.frame_overlay.includes('?') ? '&' : '?';
  return `${props.config.frame_overlay}${separator}v=3`;
});

const titleStyles = computed(() => {
  const styles = {};
  if (props.config.titleColor) styles.color = props.config.titleColor;
  if (props.config.fontFamily) styles.fontFamily = props.config.fontFamily;
  if (props.config.titleSize) styles.fontSize = `${props.config.titleSize}rem`;
  return styles;
});

const dateBoxStyle = computed(() => {
  const color = props.config.subtitleColor || props.config.headerLabelColor;
  return {
    borderColor: color ? `${color}30` : 'rgba(255, 255, 255, 0.1)'
  };
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
