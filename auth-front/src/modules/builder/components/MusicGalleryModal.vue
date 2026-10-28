<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
    <div class="w-full max-w-3xl h-[75vh] flex flex-col rounded-2xl border border-white/10 bg-white/10 backdrop-blur-md shadow-2xl overflow-hidden text-white">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 flex items-center justify-between border-b border-white/10 bg-black/20">
        <div class="flex items-center gap-2">
          <span class="text-xl">🎵</span>
          <h2 class="text-lg font-semibold tracking-wide">Buscar Melodías (Jamendo)</h2>
        </div>
        <button @click="closeModal" class="btn btn-sm btn-circle btn-ghost text-white/70 hover:text-white">✕</button>
      </div>

      <!-- Content Area -->
      <div class="flex-1 flex flex-col p-6 overflow-hidden bg-black/10">
        
        <!-- Search Bar -->
        <div class="flex gap-2 mb-4">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por género, artista o palabra clave (ej. romantic acoustic, upbeat, piano)..." 
            class="input input-bordered flex-1 bg-black/40 border-white/10 text-white placeholder-white/40 focus:border-primary/50"
            @keyup.enter="searchTracks"
          />
          <button @click="searchTracks" class="btn btn-primary px-6" :disabled="isLoading">
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            <span v-else>🔍 Buscar</span>
          </button>
        </div>

        <!-- States -->
        <div class="flex-1 overflow-y-auto">
          <!-- Loading state -->
          <div v-if="isLoading" class="h-full flex flex-col items-center justify-center gap-2">
            <span class="loading loading-ring loading-lg text-primary"></span>
            <p class="text-white/60 text-sm">Consultando biblioteca de música libre de derechos...</p>
          </div>

          <!-- Error state -->
          <div v-else-if="errorMessage" class="h-full flex flex-col items-center justify-center gap-2 text-center p-4">
            <span class="text-3xl">⚠️</span>
            <p class="text-red-400 font-semibold">{{ errorMessage }}</p>
            <p class="text-white/60 text-xs max-w-md">Verifica la conexión o la configuración de tu JAMENDO_CLIENT_ID en el servidor.</p>
          </div>

          <!-- Empty state -->
          <div v-else-if="tracks.length === 0" class="h-full flex flex-col items-center justify-center gap-2 text-white/50">
            <span class="text-4xl">🎵</span>
            <p class="text-sm">Encuentra la banda sonora perfecta para tu invitación.</p>
          </div>

          <!-- Results List -->
          <div v-else class="space-y-2 pr-1">
            <div 
              v-for="track in tracks" 
              :key="track.id"
              class="flex items-center justify-between p-3 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 hover:border-white/10 transition-all group"
            >
              <!-- Info Column -->
              <div class="flex items-center gap-3 min-w-0 flex-1">
                <!-- Cover Image -->
                <div class="w-12 h-12 rounded-lg bg-black/40 overflow-hidden flex-shrink-0 border border-white/10 relative">
                  <img 
                    :src="track.cover || '/assets/music-default-cover.png'" 
                    @error="track.cover = null" 
                    alt="Cover" 
                    class="w-full h-full object-cover" 
                  />
                  <!-- Playing overlay icon -->
                  <div 
                    v-if="currentPlayingId === track.id" 
                    class="absolute inset-0 bg-black/50 flex items-center justify-center"
                  >
                    <span class="loading loading-bounce loading-xs text-primary"></span>
                  </div>
                </div>

                <!-- Title & Artist -->
                <div class="min-w-0 flex-1">
                  <h3 class="font-medium text-sm text-white truncate group-hover:text-primary transition-colors">
                    {{ track.title }}
                  </h3>
                  <p class="text-xs text-white/50 truncate">
                    {{ track.artist }}
                  </p>
                </div>
              </div>

              <!-- Controls Column -->
              <div class="flex items-center gap-4 ml-4">
                <!-- Duration -->
                <span class="text-xs text-white/45 font-mono select-none">
                  {{ formatDuration(track.duration) }}
                </span>

                <!-- Play/Pause Preview -->
                <button 
                  @click="togglePreview(track)"
                  class="btn btn-sm btn-circle btn-outline border-white/20 text-white hover:bg-white/10 hover:border-white/40"
                  :title="currentPlayingId === track.id ? 'Pausar pre-escucha' : 'Escuchar demo'"
                >
                  <span v-if="currentPlayingId === track.id">⏸️</span>
                  <span v-else>▶️</span>
                </button>

                <!-- Select Track -->
                <button 
                  @click="selectTrack(track.audio)"
                  class="btn btn-sm btn-primary px-4 rounded-lg text-xs font-semibold tracking-wide"
                >
                  Seleccionar
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';
import invtznClient from '@/core/api/invtznClient';

const props = defineProps({
  isOpen: { type: Boolean, required: true }
});

const emit = defineEmits(['close', 'select-audio']);

const searchQuery = ref('');
const tracks = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');

// Preview player state
const currentPlayingId = ref(null);
let audioPlayer = null;

const searchTracks = async () => {
  if (!searchQuery.value.trim()) return;
  isLoading.value = true;
  errorMessage.value = '';
  stopPreview();

  try {
    const res = await invtznClient.get('deployments/jamendo-search/', {
      params: {
        q: searchQuery.value
      }
    });
    tracks.value = res.data.results || [];
  } catch (err) {
    console.error('Error fetching Jamendo tracks', err);
    errorMessage.value = err.response?.data?.error || 'No se pudo conectar al buscador de música.';
    tracks.value = [];
  } finally {
    isLoading.value = false;
  }
};

const formatDuration = (secs) => {
  if (!secs) return '0:00';
  const m = Math.floor(secs / 60);
  const s = Math.floor(secs % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
};

const togglePreview = (track) => {
  if (currentPlayingId.value === track.id) {
    stopPreview();
  } else {
    playPreview(track);
  }
};

const playPreview = (track) => {
  stopPreview();
  currentPlayingId.value = track.id;

  audioPlayer = new Audio(track.audio);
  audioPlayer.volume = 0.5; // Moderate volume for previews
  
  audioPlayer.addEventListener('ended', () => {
    stopPreview();
  });
  
  audioPlayer.addEventListener('error', (e) => {
    console.error('Error playing preview', e);
    stopPreview();
  });

  audioPlayer.play().catch(err => {
    console.error('Audio play failed', err);
    stopPreview();
  });
};

const stopPreview = () => {
  if (audioPlayer) {
    try {
      audioPlayer.pause();
      audioPlayer.src = '';
    } catch (err) {
      console.warn('Error pausing preview player', err);
    }
    audioPlayer = null;
  }
  currentPlayingId.value = null;
};

const selectTrack = (audioUrl) => {
  stopPreview();
  emit('select-audio', audioUrl);
  closeModal();
};

const closeModal = () => {
  stopPreview();
  emit('close');
};

// Clean up player on unmount
onBeforeUnmount(() => {
  stopPreview();
});

// Watch for modal state change
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    searchQuery.value = '';
    tracks.value = [];
    errorMessage.value = '';
  } else {
    stopPreview();
  }
});
</script>

<style scoped>
.btn-primary {
  background-color: hsl(var(--p));
  border-color: hsl(var(--p));
  color: white;
}
.btn-primary:hover {
  background-color: hsl(var(--p) / 0.85);
  border-color: hsl(var(--p) / 0.85);
}
.border-primary {
  border-color: hsl(var(--p));
}
.text-primary {
  color: hsl(var(--p));
}
.loading-bounce {
  animation: bounce 0.6s infinite alternate;
}
</style>
