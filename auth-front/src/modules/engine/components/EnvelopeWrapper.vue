<template>
  <div class="envelope-wrapper-container relative w-full min-h-screen overflow-hidden bg-slate-900">
    <!-- El Sobre Seleccionado Dinámicamente -->
    <component 
      v-if="currentEnvelopeComponent"
      :is="currentEnvelopeComponent"
      @opened="handleEnvelopeOpened"
    >
      <!-- Pasamos el slot hacia el componente de sobre (el contenido real) -->
      <slot></slot>
    </component>
    
    <!-- Fallback si no hay sobre -->
    <div v-else class="w-full h-full">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { shallowRef, watch, defineProps, defineAsyncComponent, onMounted } from 'vue';

const props = defineProps({
  type: {
    type: [String, Number],
    default: null
  }
});

const currentEnvelopeComponent = shallowRef(null);
const isOpened = shallowRef(false);

const loadEnvelope = (typeStr) => {
  if (!typeStr) {
    currentEnvelopeComponent.value = null;
    return;
  }
  
  // Normalizar
  const normalizedType = String(typeStr).toLowerCase();
  
  if (normalizedType === '1' || normalizedType === 'classic') {
    currentEnvelopeComponent.value = defineAsyncComponent(() => import('./envelopes/ClassicEnvelope.vue'));
  } else if (normalizedType === '2' || normalizedType === 'gatefold') {
    currentEnvelopeComponent.value = defineAsyncComponent(() => import('./envelopes/GatefoldEnvelope.vue'));
  } else if (normalizedType === '3' || normalizedType === 'origami') {
    currentEnvelopeComponent.value = defineAsyncComponent(() => import('./envelopes/OrigamiEnvelope.vue'));
  } else if (normalizedType === '4' || normalizedType === 'cyber') {
    currentEnvelopeComponent.value = defineAsyncComponent(() => import('./envelopes/CyberEnvelope.vue'));
  } else if (normalizedType === '5' || normalizedType === 'curtain') {
    currentEnvelopeComponent.value = defineAsyncComponent(() => import('./envelopes/CurtainEnvelope.vue'));
  } else {
    currentEnvelopeComponent.value = null; // fallback
  }
};

watch(() => props.type, (newType) => {
  loadEnvelope(newType);
}, { immediate: true });

const handleEnvelopeOpened = () => {
  isOpened.value = true;
};
</script>

<style scoped>
.envelope-wrapper-container {
  /* Asegura que el sobre ocupe todo antes de abrirse */
}
</style>
