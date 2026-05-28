<template>
  <div class="gatefold-envelope-container" :class="{ 'is-open': isOpen, 'is-released': isReleased }">
    <!-- El sobre físico (se remueve al abrirse completamente) -->
    <div v-if="!isReleased" class="gatefold-wrapper" id="envelope-2">
      <div class="gatefold-container relative w-full max-w-2xl aspect-[3/4] mx-auto perspective-1000">
        
        <!-- Puerta Izquierda -->
        <div class="gatefold-door door-left">
          <div class="door-inner-pattern"></div>
        </div>
        
        <!-- Puerta Derecha -->
        <div class="gatefold-door door-right">
          <div class="door-inner-pattern"></div>
        </div>

        <!-- Listón y Moño interactivo -->
        <div 
          class="ribbon-bow-container cursor-pointer transition-transform hover:scale-105" 
          id="seal-2" 
          title="Toca el lazo para desatar"
          @click="openEnvelope"
        >
          <div class="ribbon-band-horizontal"></div>
          <div class="ribbon-bow-knot flex justify-center items-center">
             <div class="w-16 h-16 rounded-full bg-slate-100 shadow-md flex items-center justify-center border-2 border-slate-200">
               🎀
             </div>
          </div>
        </div>

      </div>
      <div class="interaction-tip mt-6 text-center text-slate-800 font-serif" v-if="!isOpen">
        Toca el lazo central de seda
      </div>
    </div>

    <!-- La tarjeta de invitación (slot de contenido) -->
    <div 
      class="invitation-card-slot" 
      :class="{ 'is-visible': isCardVisible, 'is-released': isReleased }"
      id="card-2"
    >
      <div class="scrollable-content-wrapper">
         <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import { useAudioFX } from '../../composables/useAudioFX';

const emit = defineEmits(['opened']);
const audioFX = useAudioFX();

const isOpen = ref(false);
const isReleased = ref(false);
const isCardVisible = ref(false);

const openEnvelope = () => {
  if (isOpen.value) return;
  
  audioFX.playEnvelopeAudio('gatefold');
  isOpen.value = true;
  
  // A los 500ms (las puertas se están abriendo), la tarjeta se vuelve visible
  setTimeout(() => {
    isCardVisible.value = true;
  }, 500);
  
  setTimeout(() => {
    emit('opened');
    setTimeout(() => {
       isReleased.value = true;
    }, 1500); 
  }, 1200);
};
</script>

<style scoped>
.gatefold-envelope-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8fafc;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  transition: background-color 0.8s ease;
}

.gatefold-envelope-container.is-released {
  position: relative;
  background-color: transparent;
  min-height: auto;
  z-index: 1;
  inset: auto;
}

.gatefold-wrapper {
  position: relative;
  width: 90vw;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 5;
  transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.8s ease;
}

/* El tríptico completo cae y se desvanece al abrirse */
.is-open .gatefold-wrapper {
  transform: translateY(20vh);
  opacity: 0;
}

.perspective-1000 {
  perspective: 1500px;
}

.gatefold-container {
  width: 100%;
  height: 100%;
  aspect-ratio: 3/4;
}

.gatefold-door {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  background-color: #e2e8f0;
  z-index: 2;
  transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}

.door-left {
  left: 0;
  transform-origin: left center;
  border-right: 1px solid rgba(0,0,0,0.05);
}

.door-right {
  right: 0;
  transform-origin: right center;
  border-left: 1px solid rgba(0,0,0,0.05);
}

.is-open .door-left {
  transform: rotateY(-120deg);
}

.is-open .door-right {
  transform: rotateY(120deg);
}

.door-inner-pattern {
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.5;
}

.ribbon-bow-container {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  transform: translateY(-50%);
  z-index: 3;
  transition: opacity 0.5s ease;
}

.is-open .ribbon-bow-container {
  opacity: 0;
  pointer-events: none;
}

.ribbon-band-horizontal {
  width: 100%;
  height: 40px;
  background-color: #cbd5e1;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.ribbon-bow-knot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.interaction-tip {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  color: #475569;
}

/* La tarjeta que se expone */
.invitation-card-slot {
  position: absolute;
  top: 5vh;
  width: 90%;
  max-width: 450px;
  height: 90vh;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  overflow: hidden;
  z-index: 2;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: scale(0.95);
  transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.8s ease, visibility 0.8s ease;
}

.invitation-card-slot.is-visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: scale(1.0);
  z-index: 100;
}

.invitation-card-slot.is-released {
  position: relative;
  top: 0;
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 0;
  box-shadow: none;
  transform: none;
  z-index: 1;
  background-color: transparent;
  transition: none;
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.scrollable-content-wrapper {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.is-released .scrollable-content-wrapper {
  height: auto;
  overflow: visible;
}
</style>
