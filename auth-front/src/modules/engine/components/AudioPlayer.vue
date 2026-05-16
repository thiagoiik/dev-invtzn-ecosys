<template>
  <div class="fixed bottom-8 left-8 z-50">
    <!-- Main Player Card -->
    <div 
      class="bg-white/90 backdrop-blur-md rounded-2xl p-3 shadow-2xl shadow-slate-900/10 border border-slate-200/50 flex items-center gap-3 transition-all duration-500 hover:scale-105 active:scale-95"
      :class="{ 'pr-5': isPlaying }"
    >
      <!-- Circular CD / Artwork Disc -->
      <button 
        @click="togglePlay"
        class="w-12 h-12 rounded-full bg-slate-950 flex items-center justify-center text-white relative overflow-hidden shadow-lg group"
      >
        <!-- Rotation animation disk -->
        <div 
          class="absolute inset-1 rounded-full border border-white/20 flex items-center justify-center"
          :class="{ 'animate-spin-slow': isPlaying }"
          style="animation-duration: 6s;"
        >
          <span class="text-sm">🎵</span>
        </div>
        
        <!-- Center play/pause overlay on hover -->
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity duration-300">
          <span class="text-xs font-black">{{ isPlaying ? '⏸' : '▶' }}</span>
        </div>
      </button>

      <!-- Music Waveform / Playing Details -->
      <div class="flex flex-col select-none cursor-pointer" @click="togglePlay">
        <span class="text-[10px] font-black text-slate-800 uppercase tracking-widest leading-none">Música de fondo</span>
        <span class="text-[8px] font-bold text-slate-400 mt-1 uppercase tracking-widest">
          {{ isPlaying ? 'Reproduciendo' : 'Silencio' }}
        </span>
        
        <!-- Live Soundwaves indicator -->
        <div v-if="isPlaying" class="flex gap-0.5 items-end h-3 mt-1">
          <span v-for="i in 5" :key="i" 
            class="w-0.5 bg-primary rounded-full animate-soundwave"
            :style="{ 
              height: `${Math.random() * 100}%`,
              animationDelay: `${i * 0.15}s`
            }">
          </span>
        </div>
      </div>
    </div>

    <!-- Hidden HTML5 Audio Element -->
    <audio 
      ref="audioRef" 
      :src="config.audioUrl || 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'"
      loop
    ></audio>
  </div>
</template>

<script setup>
import { ref, defineProps, onBeforeUnmount } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});

const isPlaying = ref(false);
const audioRef = ref(null);

const togglePlay = () => {
  if (!audioRef.value) return;
  
  if (isPlaying.value) {
    audioRef.value.pause();
    isPlaying.value = false;
  } else {
    audioRef.value.play()
      .then(() => {
        isPlaying.value = true;
      })
      .catch(err => {
        console.warn("Autoplay blocked by browser policy. Interaction required.", err);
      });
  }
};

onBeforeUnmount(() => {
  if (audioRef.value) {
    audioRef.value.pause();
  }
});
</script>

<style scoped>
.animate-spin-slow {
  animation: spin infinite linear;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-soundwave {
  animation: soundwave 1s ease-in-out infinite alternate;
}

@keyframes soundwave {
  0% { height: 10%; }
  100% { height: 100%; }
}
</style>
