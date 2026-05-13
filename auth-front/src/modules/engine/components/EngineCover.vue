<template>
  <div class="engine-cover">
    <div class="photo-container">
      <!-- Muestra una imagen placeholder si no hay foto configurada -->
      <img :src="config.coverPhoto || 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80'" alt="Portada" />
      
      <div class="overlay">
        <h1 :style="{ color: config.titleColor || '#ffffff', fontFamily: config.fontFamily || 'serif' }">
          {{ config.title || 'Nuestra Boda' }}
        </h1>
        <p :style="{ color: config.subtitleColor || '#ffffff' }">
          {{ config.subtitle || '¡Te invitamos a celebrar!' }}
        </p>
        <p class="date">{{ config.date || '25 de Diciembre 2026' }}</p>
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
.engine-cover {
  width: 100%;
  height: 100vh; /* Ocupa toda la pantalla del celular/pc */
  position: relative;
  overflow: hidden;
}
.photo-container {
  width: 100%;
  height: 100%;
  position: relative;
}
.photo-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}
.overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
}
h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
p {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
.date {
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 2rem;
  border-top: 1px solid white;
  border-bottom: 1px solid white;
  padding: 0.5rem 0;
}
</style>
