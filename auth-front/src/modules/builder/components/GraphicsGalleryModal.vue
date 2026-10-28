<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
    <div class="w-full max-w-4xl h-[80vh] flex flex-col rounded-2xl border border-white/10 bg-white/10 backdrop-blur-md shadow-2xl overflow-hidden text-white">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 flex items-center justify-between border-b border-white/10 bg-black/20">
        <div class="flex items-center gap-2">
          <span class="text-xl">🎨</span>
          <h2 class="text-lg font-semibold tracking-wide">Galería de Recursos Gráficos</h2>
        </div>
        <button @click="$emit('close')" class="btn btn-sm btn-circle btn-ghost text-white/70 hover:text-white">✕</button>
      </div>

      <!-- Tabs Navigation -->
      <div class="flex border-b border-white/10 bg-black/10 select-none">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 py-3 text-sm font-medium transition-colors border-b-2"
          :class="activeTab === tab.id ? 'border-primary text-white bg-white/5' : 'border-transparent text-white/60 hover:text-white/80'"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="flex-1 overflow-y-auto p-6 bg-black/10">
        
        <!-- Pestaña 1: Fondos & Texturas -->
        <div v-if="activeTab === 'backgrounds'" class="grid grid-cols-2 sm:grid-cols-3 gap-6">
          <div 
            v-for="bg in localBackgrounds" 
            :key="bg.id"
            @click="selectBackground(bg.url)"
            class="group relative aspect-[3/4] rounded-xl overflow-hidden border border-white/10 bg-black/40 cursor-pointer transition-all hover:scale-[1.02] hover:border-primary/50"
          >
            <!-- Background Preview -->
            <iframe 
              v-if="bg.url.endsWith('.svg')"
              :src="bg.url" 
              class="w-full h-full pointer-events-none border-none scale-105"
            ></iframe>
            <div v-else class="w-full h-full bg-cover bg-center" :style="{ backgroundImage: `url(${bg.url})` }"></div>

            <!-- Hover overlay -->
            <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <span class="px-4 py-2 rounded-lg bg-primary text-white text-xs font-semibold uppercase tracking-wide">Aplicar</span>
            </div>
            <!-- Title -->
            <div class="absolute bottom-0 inset-x-0 p-3 bg-gradient-to-t from-black/80 to-transparent">
              <p class="text-xs font-medium text-white/90">{{ bg.name }}</p>
            </div>
          </div>
        </div>

        <!-- Pestaña 2: Fotos Libres (Unsplash) -->
        <div v-else-if="activeTab === 'unsplash'" class="flex flex-col h-full gap-4">
          <!-- Search Bar -->
          <div class="flex gap-2">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar fotos de bodas, flores, naturaleza..." 
              class="input input-bordered flex-1 bg-black/40 border-white/10 text-white placeholder-white/40 focus:border-primary/50"
              @keyup.enter="searchPhotos"
            />
            <button @click="searchPhotos" class="btn btn-primary px-6" :disabled="isLoading">
              <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
              <span v-else>Buscar</span>
            </button>
          </div>

          <!-- Loading state -->
          <div v-if="isLoading" class="flex-1 flex flex-col items-center justify-center gap-2">
            <span class="loading loading-ring loading-lg text-primary"></span>
            <p class="text-white/60 text-sm">Consultando galería libre de derechos...</p>
          </div>

          <!-- Error state -->
          <div v-else-if="errorMessage" class="flex-1 flex flex-col items-center justify-center gap-2 text-center p-4">
            <span class="text-3xl">⚠️</span>
            <p class="text-red-400 font-semibold">{{ errorMessage }}</p>
            <p class="text-white/60 text-xs max-w-md">Verifica que la clave de Unsplash esté debidamente configurada en las variables de entorno del Backend.</p>
          </div>

          <!-- Empty state -->
          <div v-else-if="photos.length === 0" class="flex-1 flex flex-col items-center justify-center gap-2 text-white/50">
            <span class="text-4xl">📸</span>
            <p class="text-sm">Realiza una búsqueda para encontrar fotografías de alta calidad libres de marcas de agua.</p>
          </div>

          <!-- Results Grid -->
          <div v-else class="flex-1 flex flex-col justify-between gap-6">
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              <div 
                v-for="photo in photos" 
                :key="photo.id"
                @click="selectBackground(photo.url)"
                class="group relative aspect-square rounded-lg overflow-hidden border border-white/10 bg-black/40 cursor-pointer transition-all hover:scale-[1.02] hover:border-primary/50"
              >
                <!-- Thumbnail -->
                <img :src="photo.thumb" alt="Unsplash search result" class="w-full h-full object-cover" />
                <!-- Hover overlay -->
                <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-between p-2">
                  <span class="self-center my-auto px-3 py-1.5 rounded bg-primary text-white text-xs font-semibold uppercase tracking-wide">Aplicar</span>
                  <!-- Attribution -->
                  <div class="text-[10px] text-white/80 line-clamp-1 pointer-events-auto bg-black/60 px-1 py-0.5 rounded" @click.stop>
                    Por <a :href="photo.author_link" target="_blank" class="underline hover:text-white">{{ photo.author }}</a> en <a href="https://unsplash.com" target="_blank" class="underline hover:text-white">Unsplash</a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pagination -->
            <div class="flex items-center justify-center gap-4 py-2 border-t border-white/5">
              <button 
                class="btn btn-sm btn-outline text-white hover:bg-white/10 border-white/20" 
                :disabled="currentPage === 1 || isLoading"
                @click="changePage(currentPage - 1)"
              >
                Anterior
              </button>
              <span class="text-sm text-white/70">Página {{ currentPage }} de {{ totalPages }}</span>
              <button 
                class="btn btn-sm btn-outline text-white hover:bg-white/10 border-white/20" 
                :disabled="currentPage === totalPages || isLoading"
                @click="changePage(currentPage + 1)"
              >
                Siguiente
              </button>
            </div>
          </div>
        </div>

        <!-- Pestaña 3: Marcos Decorativos -->
        <div v-else-if="activeTab === 'frames'" class="grid grid-cols-2 sm:grid-cols-3 gap-6">
          <!-- Option: Ninguno (clear) -->
          <div 
            @click="selectFrame(null)"
            class="group relative aspect-[3/4] rounded-xl border-2 border-dashed border-white/20 hover:border-red-400/50 flex flex-col items-center justify-center cursor-pointer transition-all hover:scale-[1.02]"
          >
            <span class="text-3xl text-white/40 group-hover:text-red-400 transition-colors">🚫</span>
            <span class="mt-2 text-xs font-medium text-white/60 group-hover:text-white transition-colors">Quitar Marco</span>
          </div>

          <!-- Frames List -->
          <div 
            v-for="frame in localFrames" 
            :key="frame.id"
            @click="selectFrame(frame.url)"
            class="group relative aspect-[3/4] rounded-xl overflow-hidden border border-white/10 bg-black/40 cursor-pointer transition-all hover:scale-[1.02] hover:border-primary/50"
          >
            <!-- Frame Preview wrapped with dark cover simulation -->
            <div class="w-full h-full bg-[#1e1e24] relative p-4 flex items-center justify-center">
              <span class="text-[10px] text-white/30 tracking-widest uppercase">Vista Previa</span>
              <iframe 
                :src="frame.url" 
                class="absolute inset-0 w-full h-full pointer-events-none border-none"
              ></iframe>
            </div>

            <!-- Hover overlay -->
            <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <span class="px-4 py-2 rounded-lg bg-primary text-white text-xs font-semibold uppercase tracking-wide">Aplicar</span>
            </div>
            <!-- Title -->
            <div class="absolute bottom-0 inset-x-0 p-3 bg-gradient-to-t from-black/80 to-transparent">
              <p class="text-xs font-medium text-white/90">{{ frame.name }}</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import invtznClient from '@/core/api/invtznClient';

const props = defineProps({
  isOpen: { type: Boolean, required: true }
});

const emit = defineEmits(['close', 'select-background', 'select-frame']);

const activeTab = ref('backgrounds');

const tabs = [
  { id: 'backgrounds', name: 'Fondos & Texturas' },
  { id: 'unsplash', name: 'Buscador Unsplash' },
  { id: 'frames', name: 'Marcos Decorativos' }
];

// Local asset arrays (predefined paths)
const localBackgrounds = [
  { id: 'watercolor', name: 'Acuarela Suave', url: '/assets/backgrounds/watercolor_soft.svg' },
  { id: 'paper', name: 'Papel Texturizado', url: '/assets/backgrounds/textured_paper.svg' },
  { id: 'canvas', name: 'Lienzo Elegante', url: '/assets/backgrounds/elegant_canvas.svg' }
];

const localFrames = [
  { id: 'geometric', name: 'Geométrico Dorado', url: '/assets/frames/frame_geometric_gold.svg' },
  { id: 'minimalist', name: 'Esquinas Minimalistas', url: '/assets/frames/frame_minimalist_corners.svg' },
  { id: 'floral', name: 'Follaje Elegante', url: '/assets/frames/frame_floral_border.svg' }
];

// Unsplash States
const searchQuery = ref('');
const photos = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const isLoading = ref(false);
const errorMessage = ref('');

const searchPhotos = async () => {
  if (!searchQuery.value.trim()) return;
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const res = await invtznClient.get('deployments/unsplash-search/', {
      params: {
        query: searchQuery.value,
        page: currentPage.value,
        per_page: 12
      }
    });
    photos.value = res.data.results || [];
    totalPages.value = res.data.total_pages || 1;
  } catch (err) {
    console.error('Error fetching Unsplash photos', err);
    errorMessage.value = err.response?.data?.error || 'No se pudo conectar al buscador de imágenes.';
    photos.value = [];
  } finally {
    isLoading.value = false;
  }
};

const changePage = (page) => {
  currentPage.value = page;
  searchPhotos();
};

const selectBackground = (url) => {
  emit('select-background', url);
  emit('close');
};

const selectFrame = (url) => {
  emit('select-frame', url);
  emit('close');
};

// Reset state when modal is opened/closed
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    activeTab.value = 'backgrounds';
    searchQuery.value = '';
    photos.value = [];
    currentPage.value = 1;
    errorMessage.value = '';
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
</style>
