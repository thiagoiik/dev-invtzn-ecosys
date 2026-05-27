<template>
  <div class="classic-envelope-container" :class="{ 'is-open': isOpen, 'is-released': isReleased }">
    <!-- El sobre y sus partes físicas (se remueven al finalizar la transición) -->
    <div v-if="!isReleased" class="envelope-classic-wrapper" id="envelope-1">
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
      </div>
      <div class="interaction-tip animate-pulse mt-8 text-white font-serif tracking-widest text-sm" v-if="!isOpen">
        Toca el sello de lacre dorado
      </div>
    </div>

    <!-- La tarjeta de invitación (slot de contenido) -->
    <div 
      class="invitation-card-slot" 
      :class="{ 'is-active': isOpen, 'is-released': isReleased }"
      id="card-1"
    >
      <div class="scrollable-content-wrapper">
         <slot v-slot="{ isOpened }"></slot>
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
const renderContent = ref(false); // To delay rendering the heavy content

const openEnvelope = () => {
  if (isOpen.value) return;
  
  // Play sound
  audioFX.playEnvelopeAudio('classic');
  
  isOpen.value = true;
  renderContent.value = true;
  
  setTimeout(() => {
    emit('opened');
    // Esperamos 1.5s a que termine la animación de deslizamiento y liberamos la tarjeta
    setTimeout(() => {
       isReleased.value = true;
    }, 1500);
  }, 1000);
};
</script>

<style scoped>
.classic-envelope-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #111111;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  transition: background-color 0.8s ease;
}

/* Al abrirse del todo, se vuelve transparente y relativo para no estorbar el scroll global */
.classic-envelope-container.is-released {
  position: relative;
  background-color: transparent;
  min-height: auto;
  z-index: 1;
  inset: auto;
}

.envelope-classic-wrapper {
  position: relative;
  width: 90vw;
  max-width: 500px;
  aspect-ratio: 1.4 / 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  perspective: 1500px;
  z-index: 5;
}

.envelope-classic {
  width: 100%;
  height: 100%;
  position: relative;
  background-color: #f4ebd8; /* Papel crema */
  border-radius: 8px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  transform-style: preserve-3d;
  transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.is-open .envelope-classic {
  transform: translateY(100vh) rotateX(15deg); /* Cae con rotación 3D */
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
  width: 70px;
  height: 70px;
  background: radial-gradient(circle, #b8860b, #8b6508);
  border-radius: 50%;
  z-index: 6;
  box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset 0 2px 5px rgba(255,255,255,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #daa520;
}

.seal-crest {
  font-family: 'Cinzel', serif;
  color: #fff8e7;
  font-size: 1.25rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.is-open .envelope-wax-seal {
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}

.interaction-tip {
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  color: #daa520;
}

/* La tarjeta que se desliza fuera del sobre */
.invitation-card-slot {
  position: absolute;
  top: 10vh;
  width: 90%;
  max-width: 450px;
  height: 80vh;
  background-color: #fff;
  border-radius: 16px;
  z-index: 2;
  transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  overflow: hidden;
}

/* La carta sale hacia arriba y toma la pantalla */
.invitation-card-slot.is-active:not(.is-released) {
  transform: translateY(-110vh) scale(1.03);
  z-index: 100;
}

/* Cuando se libera al final, toma el control de scroll global */
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
