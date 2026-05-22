<template>
  <div class="cyber-envelope-container" :class="{ 'is-open': isOpen, 'is-scanning': isScanning, 'is-hidden': isHidden }">
    <div class="cyber-gate-wrapper" id="envelope-4">
      <div class="cyber-gate-container relative w-full h-screen overflow-hidden bg-black flex justify-center items-center">
        
        <!-- Tarjeta adentro -->
        <div class="invitation-card-slot" id="card-4">
          <slot v-if="renderContent"></slot>
        </div>

        <!-- Puerta Metálica Izquierda -->
        <div class="cyber-panel panel-left border-r-2 border-cyan-500/50">
          <div class="panel-circuit-lines"></div>
        </div>

        <!-- Puerta Metálica Derecha -->
        <div class="cyber-panel panel-right border-l-2 border-cyan-500/50">
          <div class="panel-circuit-lines"></div>
        </div>

        <!-- Rayo Láser de Escaneo -->
        <div class="laser-beam" id="cyber-laser" v-if="isScanning"></div>

        <!-- Lector Holográfico Interactivo -->
        <div 
          class="fingerprint-scanner cursor-pointer" 
          id="seal-4" 
          title="Toca para iniciar escáner"
          @click="openEnvelope"
        >
          <div class="scanner-ring" :class="{ 'animate-spin': isScanning }"></div>
          <div class="scanner-icon text-cyan-400 text-4xl">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" /></svg>
          </div>
          <div class="scanner-text text-cyan-400 font-mono text-xs mt-2 font-bold tracking-widest uppercase">
            {{ isScanning ? 'ANALIZANDO' : 'ESCANEAR' }}
          </div>
        </div>

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
const isScanning = ref(false);
const isHidden = ref(false);
const renderContent = ref(true);

const openEnvelope = () => {
  if (isOpen.value || isScanning.value) return;
  
  audioFX.playEnvelopeAudio('cyber');
  isScanning.value = true;
  
  // Detener escáner y abrir después de 1.2 segundos (1 ciclo láser)
  setTimeout(() => {
    isScanning.value = false;
    isOpen.value = true;
    
    setTimeout(() => {
      emit('opened');
      setTimeout(() => {
         isHidden.value = true;
      }, 1500); 
    }, 800); // Wait for door opening
  }, 1200);
};
</script>

<style scoped>
.cyber-envelope-container {
  position: absolute;
  inset: 0;
  z-index: 50;
  transition: opacity 0.5s ease-in-out;
}

.cyber-envelope-container.is-hidden {
  opacity: 0;
  pointer-events: none;
  z-index: -1;
}

.invitation-card-slot {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.cyber-panel {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  background-color: #0f172a; /* Slate 900 */
  z-index: 2;
  transition: transform 0.8s cubic-bezier(0.8, 0, 0.2, 1);
}

.panel-left { left: 0; transform-origin: left; }
.panel-right { right: 0; transform-origin: right; }

.is-open .panel-left { transform: translateX(-100%); }
.is-open .panel-right { transform: translateX(100%); }

.panel-circuit-lines {
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(6, 182, 212, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
}

/* Vibración Glitch justo antes de abrir */
.is-scanning .cyber-panel {
  animation: panel-shake 0.1s infinite alternate;
  animation-delay: 1s; /* Empieza a vibrar al final del escaneo */
}

@keyframes panel-shake {
  0% { transform: translateX(-2px); }
  100% { transform: translateX(2px); }
}

.laser-beam {
  position: absolute;
  top: -10px;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: #00f0ff;
  box-shadow: 0 0 20px 5px rgba(0, 240, 255, 0.5);
  z-index: 4;
  animation: scan-down-up 1.2s ease-in-out forwards;
}

@keyframes scan-down-up {
  0% { top: 10%; }
  50% { top: 90%; }
  100% { top: 50%; opacity: 0; }
}

.fingerprint-scanner {
  position: absolute;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s;
}

.is-open .fingerprint-scanner {
  opacity: 0;
  pointer-events: none;
}

.scanner-ring {
  position: absolute;
  width: 100px;
  height: 100px;
  border: 2px dashed rgba(6, 182, 212, 0.5);
  border-radius: 50%;
}

.is-scanning .scanner-icon {
  color: #00f0ff;
  filter: drop-shadow(0 0 8px #00f0ff);
  animation: pulse-glow 0.5s infinite alternate;
}

@keyframes pulse-glow {
  0% { filter: drop-shadow(0 0 5px #00f0ff); }
  100% { filter: drop-shadow(0 0 15px #00f0ff); }
}
</style>
