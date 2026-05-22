<template>
  <div class="origami-envelope-container" :class="{ 'is-open': isOpen, 'is-hidden': isHidden }">
    <div class="origami-wrapper" id="envelope-3">
      <div class="origami-box relative w-[90vw] max-w-[400px] aspect-square mx-auto">
        
        <!-- Tarjeta adentro -->
        <div class="invitation-card-slot" id="card-3">
          <slot v-if="renderContent"></slot>
        </div>

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
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import { useAudioFX } from '../../composables/useAudioFX';

const emit = defineEmits(['opened']);
const audioFX = useAudioFX();

const isOpen = ref(false);
const isHidden = ref(false);
const renderContent = ref(true);

const openEnvelope = () => {
  if (isOpen.value) return;
  
  audioFX.playEnvelopeAudio('origami');
  isOpen.value = true;
  
  setTimeout(() => {
    emit('opened');
    setTimeout(() => {
       isHidden.value = true;
    }, 1500); 
  }, 1400); // 4 clicks of 200ms + ending
};
</script>

<style scoped>
.origami-envelope-container {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f1f5f9;
  z-index: 50;
  transition: opacity 1s ease-in-out;
}

.origami-envelope-container.is-hidden {
  opacity: 0;
  pointer-events: none;
  z-index: -1;
}

.origami-box {
  perspective: 1200px;
}

.invitation-card-slot {
  position: absolute;
  inset: 5%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  overflow: hidden;
  z-index: 1;
}

.origami-flap {
  position: absolute;
  background-color: #cbd5e1;
  z-index: 2;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  opacity: 0.95;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.flap-top {
  top: 0; left: 0; width: 100%; height: 50%;
  clip-path: polygon(0 0, 100% 0, 50% 100%);
  transform-origin: top;
  z-index: 5;
}

.flap-right {
  top: 0; right: 0; width: 50%; height: 100%;
  clip-path: polygon(100% 0, 100% 100%, 0 50%);
  transform-origin: right;
  z-index: 4;
}

.flap-bottom {
  bottom: 0; left: 0; width: 100%; height: 50%;
  clip-path: polygon(0 100%, 100% 100%, 50% 0);
  transform-origin: bottom;
  z-index: 3;
}

.flap-left {
  top: 0; left: 0; width: 50%; height: 100%;
  clip-path: polygon(0 0, 0 100%, 100% 50%);
  transform-origin: left;
  z-index: 2;
}

/* Sequential opening */
.is-open .flap-top { transform: rotateX(180deg); transition-delay: 0.6s; }
.is-open .flap-right { transform: rotateY(180deg); transition-delay: 0.4s; }
.is-open .flap-bottom { transform: rotateX(-180deg); transition-delay: 0.2s; }
.is-open .flap-left { transform: rotateY(-180deg); transition-delay: 0s; }

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
</style>
