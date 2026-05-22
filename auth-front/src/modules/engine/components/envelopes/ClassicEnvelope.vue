<template>
  <div class="classic-envelope-container" :class="{ 'is-open': isOpen, 'is-hidden': isHidden }">
    <div class="envelope-classic-wrapper" id="envelope-1">
      <div class="envelope-classic-shadow"></div>
      <div class="envelope-classic">
        <!-- Solapa superior -->
        <div class="envelope-flap-top"></div>
        
        <!-- Cuerpo del sobre -->
        <div class="envelope-body-pocket"></div>
        
        <!-- Sello de lacre interactivo -->
        <div 
          class="envelope-wax-seal cursor-pointer transition-transform hover:scale-110 active:scale-95" 
          id="seal-1" 
          title="Toca el lacre para abrir"
          @click="openEnvelope"
        >
          <div class="seal-crest">S&A</div>
          <div class="seal-crack-line"></div>
        </div>
        
        <!-- Aquí metemos el contenido cuando se abre -->
        <div class="invitation-card-slot" id="card-1">
          <div class="scrollable-content-wrapper">
             <slot v-if="renderContent"></slot>
          </div>
        </div>
      </div>
      <div class="interaction-tip animate-pulse mt-8 text-white font-serif tracking-widest text-sm" v-if="!isOpen">
        Toca el sello de lacre dorado
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
const renderContent = ref(false); // To delay rendering the heavy content

const openEnvelope = () => {
  if (isOpen.value) return;
  
  // Play sound
  audioFX.playEnvelopeAudio('classic');
  
  isOpen.value = true;
  renderContent.value = true;
  
  setTimeout(() => {
    emit('opened');
    // Hide the envelope completely after animation so it doesn't block scrolling
    setTimeout(() => {
       isHidden.value = true;
    }, 1500); // 1.5s is enough for the transition to complete
  }, 1000);
};
</script>

<style scoped>
.classic-envelope-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1a1a1a;
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 50;
  transition: opacity 1s ease-in-out;
}

.classic-envelope-container.is-hidden {
  opacity: 0;
  pointer-events: none;
  z-index: -1;
}

.envelope-classic-wrapper {
  position: relative;
  width: 90vw;
  max-width: 600px;
  aspect-ratio: 1.5 / 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  perspective: 1500px;
}

.envelope-classic {
  width: 100%;
  height: 100%;
  position: relative;
  background-color: #f4ebd8; /* Papel crema */
  border-radius: 8px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  transform-style: preserve-3d;
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.is-open .envelope-classic {
  transform: translateY(100vh) rotateX(10deg); /* Se cae hacia abajo */
}

.envelope-flap-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 60%;
  background-color: #e9deca;
  clip-path: polygon(0 0, 50% 100%, 100% 0);
  transform-origin: top;
  z-index: 4;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.is-open .envelope-flap-top {
  transform: rotateX(180deg);
  z-index: 1;
}

.envelope-body-pocket {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #f4ebd8;
  clip-path: polygon(0 100%, 0 40%, 50% 70%, 100% 40%, 100% 100%);
  z-index: 3;
}

.envelope-wax-seal {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, #b8860b, #8b6508);
  border-radius: 50%;
  z-index: 5;
  box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset 0 2px 5px rgba(255,255,255,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #daa520;
}

.seal-crest {
  font-family: 'Cinzel', serif;
  color: #fff8e7;
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.is-open .envelope-wax-seal {
  opacity: 0;
  transition: opacity 0.2s;
}

.invitation-card-slot {
  position: absolute;
  bottom: 0;
  left: 5%;
  width: 90%;
  height: 95%;
  background-color: #fff;
  border-radius: 4px;
  z-index: 2;
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1) 0.5s;
  box-shadow: 0 -5px 15px rgba(0,0,0,0.1);
}

.is-open .invitation-card-slot {
  /* La carta sale hacia arriba y toma la pantalla, mientras el sobre cae */
  transform: translateY(-120vh) scale(1.1);
}

.scrollable-content-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden; /* Evita scrolls antes de tiempo */
}
</style>
