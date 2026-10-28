<template>
  <div class="curtain-envelope-container" :class="{ 'is-open': isOpen, 'is-released': isReleased }">
    <!-- El sobre físico (se remueve al abrirse completamente) -->
    <div v-if="!isReleased" class="curtain-wrapper" id="envelope-5">
      <div class="relative w-full h-screen overflow-hidden bg-black flex justify-center items-center">
        
        <!-- Partículas (Sparkles) -->
        <div class="sparkles-container absolute inset-0 z-10 pointer-events-none" ref="sparklesRef"></div>

        <!-- Telón Izquierdo -->
        <div class="curtain-panel panel-left bg-red-900 border-r border-red-800">
           <div class="silk-folds"></div>
        </div>

        <!-- Telón Derecho -->
        <div class="curtain-panel panel-right bg-red-900 border-l border-red-800">
           <div class="silk-folds"></div>
        </div>

        <!-- Broche Interactivo -->
        <div 
          class="curtain-clasp cursor-pointer transition-transform hover:scale-110 active:scale-95" 
          id="seal-5" 
          title="Toca la estrella para abrir el telón"
          @click="openEnvelope"
        >
          <div class="w-16 h-16 bg-amber-400 rounded-full flex items-center justify-center border-4 border-amber-600 shadow-2xl">
            <span class="text-3xl text-amber-100">⭐</span>
          </div>
        </div>
      </div>
    </div>

    <!-- La tarjeta de invitación (slot de contenido) -->
    <div 
      class="invitation-card-slot" 
      :class="{ 'is-active': isOpen, 'is-released': isReleased }"
      id="card-5"
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
const sparklesRef = ref(null);

const generateSparkles = (count) => {
  if (!sparklesRef.value) return;
  const colors = ["#f1c40f", "#fcd057", "#ffffff", "#e3a2aa", "#d4af37"];
  
  for (let i = 0; i < count; i++) {
    const particle = document.createElement("div");
    particle.className = "sparkle-particle absolute rounded-full";
    
    const left = Math.random() * 100;
    const moveX = (Math.random() * 120 - 60) + "px";
    const delay = Math.random() * 1.2;
    const duration = 1 + Math.random() * 1;
    const size = 3 + Math.random() * 5;
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    particle.style.left = left + "%";
    particle.style.bottom = "10%";
    particle.style.width = size + "px";
    particle.style.height = size + "px";
    particle.style.backgroundColor = color;
    particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;
    particle.style.setProperty("--move-x", moveX);
    particle.style.animation = `floatUp ${duration}s ease-out ${delay}s forwards`;
    
    sparklesRef.value.appendChild(particle);
  }
};

const openEnvelope = () => {
  if (isOpen.value) return;
  
  audioFX.playEnvelopeAudio('curtain');
  isOpen.value = true;
  generateSparkles(40);
  
  setTimeout(() => {
    emit('opened');
    setTimeout(() => {
       isReleased.value = true;
    }, 1500); 
  }, 1500);
};
</script>

<style scoped>
.curtain-envelope-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #000;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  transition: background-color 0.8s ease;
}

.curtain-envelope-container.is-released {
  position: relative;
  background-color: transparent;
  min-height: auto;
  z-index: 1;
  inset: auto;
}

.curtain-wrapper {
  position: absolute;
  inset: 0;
  z-index: 5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.curtain-panel {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  z-index: 2;
  transition: transform 1.5s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
  overflow: hidden;
}

.silk-folds {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg, 
    rgba(255,255,255,0) 0%, 
    rgba(255,255,255,0.1) 20%, 
    rgba(255,255,255,0) 40%, 
    rgba(255,255,255,0.15) 60%, 
    rgba(255,255,255,0) 80%
  );
}

.panel-left { left: 0; transform-origin: top left; }
.panel-right { right: 0; transform-origin: top right; }

/* Efecto de recoger el telón (Skew + scaleX) */
.is-open .panel-left { transform: scaleX(0.1) skewY(5deg); }
.is-open .panel-right { transform: scaleX(0.1) skewY(-5deg); }

.curtain-clasp {
  position: absolute;
  z-index: 5;
  transition: opacity 0.5s, transform 0.3s;
}

.is-open .curtain-clasp {
  opacity: 0;
  pointer-events: none;
}

/* Animación global para las partículas */
:global(.sparkle-particle) {
  opacity: 0;
}

:global(@keyframes floatUp) {
  0% { 
    opacity: 1; 
    transform: translate(0, 0) scale(1); 
  }
  100% { 
    opacity: 0; 
    transform: translate(var(--move-x), -60vh) scale(0); 
  }
}

/* La tarjeta que se expone */
.invitation-card-slot {
  position: absolute;
  inset: 0;
  z-index: 2;
  transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
  overflow: hidden;
}

.invitation-card-slot.is-active:not(.is-released) {
  z-index: 100;
}

.invitation-card-slot.is-released {
  position: relative;
  width: 100%;
  height: auto;
  z-index: 1;
  background-color: transparent;
  transition: none;
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
