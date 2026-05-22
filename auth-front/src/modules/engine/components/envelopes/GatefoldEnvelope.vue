<template>
  <div class="gatefold-envelope-container" :class="{ 'is-open': isOpen, 'is-hidden': isHidden }">
    <div class="gatefold-wrapper" id="envelope-2">
      <div class="gatefold-container relative w-full max-w-2xl aspect-[3/4] mx-auto perspective-1000">
        
        <!-- Contenido principal (Slot) -->
        <div class="invitation-card-slot" id="card-2">
           <slot v-if="renderContent"></slot>
        </div>

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
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import { useAudioFX } from '../../composables/useAudioFX';

const emit = defineEmits(['opened']);
const audioFX = useAudioFX();

const isOpen = ref(false);
const isHidden = ref(false);
const renderContent = ref(true); // Content needs to be behind doors initially

const openEnvelope = () => {
  if (isOpen.value) return;
  
  audioFX.playEnvelopeAudio('gatefold');
  isOpen.value = true;
  
  setTimeout(() => {
    emit('opened');
    setTimeout(() => {
       isHidden.value = true;
    }, 1500); 
  }, 1200);
};
</script>

<style scoped>
.gatefold-envelope-container {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fafc;
  z-index: 50;
  transition: opacity 1s ease-in-out;
}

.gatefold-envelope-container.is-hidden {
  opacity: 0;
  pointer-events: none;
  z-index: -1;
}

.perspective-1000 {
  perspective: 1500px;
}

.invitation-card-slot {
  position: absolute;
  inset: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  overflow: hidden;
  z-index: 1;
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
</style>
