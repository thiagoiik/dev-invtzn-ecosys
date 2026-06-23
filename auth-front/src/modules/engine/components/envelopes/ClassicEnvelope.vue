<template>
  <div class="classic-envelope-container" :class="{ 'is-open': isOpen, 'is-released': isReleased }">
    <!-- El sobre y sus partes físicas (se remueven al finalizar la transición) -->
    <div v-if="!isReleased" class="envelope-classic-wrapper" id="envelope-1">
      <div class="envelope-classic-shadow"></div>
      
      <!-- CAPA 1: Parte trasera del sobre (Fondo crema) -->
      <div class="envelope-classic-back"></div>

      <!-- CAPA 3: Parte delantera del sobre (Bolsillo, solapa y lacre) -->
      <div class="envelope-classic-front" :class="{ 'flap-open': isOpen }">
        <!-- Cuerpo del sobre / Bolsillo frontal -->
        <div class="envelope-body-pocket"></div>
        
        <!-- Solapa superior -->
        <div class="envelope-flap-top"></div>
        
        <!-- Sello de lacre interactivo -->
        <div 
          class="envelope-wax-seal cursor-pointer transition-all hover:scale-110 active:scale-95" 
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

    <!-- CAPA 2: La tarjeta de invitación (Hermano plano) -->
    <div 
      class="invitation-card-slot" 
      :class="{ 'is-visible': isCardVisible, 'is-released': isReleased }"
      id="card-1"
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
  
  // Reproducir sonido
  audioFX.playEnvelopeAudio('classic');
  isOpen.value = true;
  
  // A los 800ms (cuando la solapa termina de abrirse), la tarjeta se vuelve visible y empieza a subir
  setTimeout(() => {
    isCardVisible.value = true;
  }, 800);
  
  setTimeout(() => {
    emit('opened');
    // Esperamos 2.0s en total (1.2s de animación de deslizamiento y caída) para liberar la tarjeta al scroll
    setTimeout(() => {
       isReleased.value = true;
    }, 1200);
  }, 800);
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
  transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.8s ease;
  will-change: transform, opacity;
  backface-visibility: hidden;
}

/* El sobre completo cae y se desvanece al abrirse */
.is-open .envelope-classic-wrapper {
  transform: translateY(100vh) rotateX(15deg);
  opacity: 0;
  transition-delay: 0.8s;
}

.envelope-classic-shadow {
  position: absolute;
  inset: 0;
  border-radius: 8px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.6);
  z-index: 0;
}

/* Capa 1: Trasera */
.envelope-classic-back {
  position: absolute;
  inset: 0;
  background-color: #f4ebd8; /* Papel crema */
  border-radius: 8px;
  z-index: 1;
}

/* Capa 3: Frente */
.envelope-classic-front {
  position: absolute;
  inset: 0;
  z-index: 3;
  transform-style: preserve-3d;
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
  box-shadow: inset 0 4px 20px rgba(0,0,0,0.05);
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
  will-change: transform;
  backface-visibility: hidden;
}

.flap-open .envelope-flap-top {
  transform: rotateX(180deg);
  z-index: 1;
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
  transition: opacity 0.3s;
}

.flap-open .envelope-wax-seal {
  opacity: 0;
  pointer-events: none;
}

.seal-crest {
  font-family: 'Cinzel', serif;
  color: #fff8e7;
  font-size: 1.25rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

.interaction-tip {
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  color: #daa520;
}

/* Capa 2: La tarjeta que se desliza fuera del sobre */
.invitation-card-slot {
  position: absolute;
  top: 15vh;
  width: 86%;
  max-width: 430px;
  height: 70vh;
  background-color: #fff;
  border-radius: 16px;
  z-index: 2; /* Entre la trasera (1) y el frente (3) */
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateY(12vh) scale(0.9); /* Oculta y metida dentro */
  transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.6s ease, visibility 0.6s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  overflow: hidden;
  will-change: transform, opacity;
  backface-visibility: hidden;
}

/* La carta sale hacia arriba y toma la pantalla */
.invitation-card-slot.is-visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateY(-24vh) scale(1.02); /* Sube suavemente saliendo del bolsillo */
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
  .envelope-classic-wrapper {
    width: 85vw;
    max-width: 320px;
  }
  .invitation-card-slot {
    width: 90vw;
    max-width: 360px;
    height: 75vh;
    top: 12vh;
  }
  .invitation-card-slot.is-visible {
    transform: translateY(-16vh) scale(1.0);
  }
}
</style>
