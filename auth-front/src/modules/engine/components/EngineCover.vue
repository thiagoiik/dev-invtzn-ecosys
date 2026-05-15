<template>
  <div 
    class="hero min-h-screen" 
    :style="{ 
      backgroundImage: `url(${config.coverPhoto || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80'})`,
      backgroundPosition: 'center',
      backgroundSize: 'cover'
    }"
  >
    <div class="hero-overlay bg-opacity-60" style="background-color: rgba(0,0,0,0.5);"></div>
    <div class="hero-content text-center text-neutral-content">
      <div class="max-w-md">
        <h1 
          class="mb-5 text-5xl font-bold tracking-tight drop-shadow-md"
          :style="{ color: config.titleColor || '#ffffff', fontFamily: config.fontFamily || 'serif' }"
        >
          {{ config.title || 'Nuestra Boda' }}
        </h1>
        <p 
          class="mb-5 text-xl drop-shadow-md"
          :style="{ color: config.subtitleColor || '#e2e8f0' }"
        >
          {{ config.subtitle || '¡Te invitamos a celebrar!' }}
        </p>
        <div class="divider divider-neutral opacity-50"></div>
        <p class="text-2xl font-light tracking-widest drop-shadow-md text-white">
          {{ config.date || '25 DICIEMBRE 2026' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});
</script>

<style scoped>
/* Tailwind handles the styles */
</style>
