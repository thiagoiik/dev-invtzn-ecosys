<template>
  <div class="origami-envelope-container" :class="{ 'is-open': isOpen, 'is-released': isReleased }">
    <!-- El sobre físico (se remueve al abrirse completamente) -->
    <div v-if="!isReleased" class="origami-wrapper" id="envelope-3">
      <div class="origami-box relative w-[90vw] max-w-[400px] aspect-square mx-auto">
        
        <!-- CAPA 1: Fondo crema del origami -->
        <div class="origami-back"></div>

        <!-- Solapas que se desdoblan en orden -->
        <div class="origami-flap flap-left"></div>
        <div class="origami-flap flap-right"></div>
        <div class="origami-flap flap-bottom"></div>
        <div class="origami-flap flap-top"></div>
        
        <!-- Sello Central -->
        <div 
          class="origami-seal cursor-pointer transition-transform hover:scale-110 active:scale-95" 
          id="seal-3" 
          title="Haz clic para desdoblar"
          @click="openEnvelope"
        >
          <div class="seal-inner">
            <span class="text-2xl">❤️</span>
          </div>
        </div>
      </div>
      <div class="interaction-tip mt-8 text-center text-slate-800 font-bold tracking-wider" v-if="!isOpen">
        Toca el corazón
      </div>
    </div>

    <!-- La tarjeta de invitación (slot de contenido) -->
    <div 
      class="invitation-card-slot" 
      :class="{ 'is-visible': isCardVisible, 'is-released': isReleased }"
      id="card-3"
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
  
  audioFX.playEnvelopeAudio('origami');
  isOpen.value = true;
  
  // A los 1.2s (cuando las 4 solapas terminan de desdoblarse), la tarjeta se vuelve visible y se eleva
  setTimeout(() => {
    isCardVisible.value = true;
  }, 1200);
  
  setTimeout(() => {
    emit('opened');
    // Esperamos 1.2s adicionales para liberar la tarjeta al scroll nativo
    setTimeout(() => {
       isReleased.value = true;
    }, 1200);
  }, 1200);
};
</script>

<style scoped>
.origami-envelope-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f1f5f9;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  transition: background-color 0.8s ease;
}

.origami-envelope-container.is-released {
  position: relative;
  background-color: transparent;
  min-height: auto;
  z-index: 1;
  inset: auto;
}

.origami-wrapper {
  position: relative;
  width: 90vw;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 5;
  transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.8s ease;
}

/* El sobre desdoblado cae y se desvanece tras la apertura */
.is-open .origami-wrapper {
  transform: translateY(15vh) scale(0.95);
  opacity: 0;
  transition-delay: 1.2s;
}

.origami-back {
  position: absolute;
  inset: 0;
  background-color: #cbd5e1; /* Revestimiento interior de papel */
  border-radius: 4px;
  z-index: 1;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
}

.origami-box {
  width: 100%;
  aspect-ratio: 1;
  perspective: 1200px;
}

.origami-flap {
  position: absolute;
  background-color: #cbd5e1;
  z-index: 2;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  opacity: 0.95;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  will-change: transform;
  backface-visibility: hidden;
}

.flap-top {
  top: 0; left: 0; width: 100%; height: 50%;
  clip-path: polygon(0 0, 100% 0, 50% 100%);
  transform-origin: top;
  z-index: 5;
  transform: scale(1.015);
}

.flap-right {
  top: 0; right: 0; width: 50%; height: 100%;
  clip-path: polygon(100% 0, 100% 100%, 0 50%);
  transform-origin: right;
  z-index: 4;
  transform: scale(1.015);
}

.flap-bottom {
  bottom: 0; left: 0; width: 100%; height: 50%;
  clip-path: polygon(0 100%, 100% 100%, 50% 0);
  transform-origin: bottom;
  z-index: 3;
  transform: scale(1.015);
}

.flap-left {
  top: 0; left: 0; width: 50%; height: 100%;
  clip-path: polygon(0 0, 0 100%, 100% 50%);
  transform-origin: left;
  z-index: 2;
  transform: scale(1.015);
}

/* Sequential opening */
.is-open .flap-top { transform: rotateX(180deg) scale(1.015); transition-delay: 0.6s; }
.is-open .flap-right { transform: rotateY(180deg) scale(1.015); transition-delay: 0.4s; }
.is-open .flap-bottom { transform: rotateX(-180deg) scale(1.015); transition-delay: 0.2s; }
.is-open .flap-left { transform: rotateY(-180deg) scale(1.015); transition-delay: 0s; }

.origami-seal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 6;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  transition: opacity 0.3s ease;
}

.is-open .origami-seal {
  opacity: 0;
  pointer-events: none;
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
  max-width: 420px;
  height: 90vh;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  overflow: hidden;
  z-index: 2;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: scale(0.9) translateY(4vh);
  transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.8s ease, visibility 0.8s ease;
  will-change: transform, opacity;
  backface-visibility: hidden;
}

.invitation-card-slot.is-visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: scale(1.0) translateY(0);
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

@media (max-width: 640px) {
  .origami-wrapper {
    width: 85vw;
    max-width: 320px;
  }
  .invitation-card-slot {
    width: 90vw;
    max-width: 360px;
    height: 80vh;
    top: 8vh;
  }
  .invitation-card-slot.is-visible {
    transform: scale(1.0) translateY(0);
  }
}
</style>
