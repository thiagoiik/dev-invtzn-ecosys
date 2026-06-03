<template>
  <div class="py-12 px-6 max-w-4xl mx-auto space-y-8 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6">
    <div class="text-center space-y-2">
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">{{ config.title || 'Nuestra Galería' }}</h2>
      <p v-if="config.description" class="text-sm text-slate-500 max-w-md mx-auto leading-relaxed">{{ config.description }}</p>
    </div>

    <!-- Carrusel Táctil Responsivo -->
    <div v-if="config.images && config.images.length > 0" class="relative">
      <div class="carousel carousel-center w-full p-4 space-x-6 bg-slate-50/50 rounded-3xl border border-slate-100">
        <div 
          v-for="(img, idx) in config.images" 
          :key="idx" 
          class="carousel-item relative group aspect-[3/4] w-64 md:w-80 overflow-hidden rounded-2xl shadow-md border border-slate-100/50 bg-slate-200 cursor-zoom-in"
          @click="openLightbox(idx)"
        >
          <img 
            :src="img" 
            alt="Foto del evento" 
            class="object-cover w-full h-full group-hover:scale-105 transition-transform duration-700" 
            loading="lazy"
          />
          <div class="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors"></div>
        </div>
      </div>
      
      <!-- Indicador visual de scroll lateral -->
      <div class="text-center mt-2 text-[10px] text-slate-400 font-bold uppercase tracking-widest flex items-center justify-center gap-1">
        <span>↔ Desliza para ver más</span>
      </div>
    </div>

    <div v-else class="text-center py-8 text-slate-400 font-medium">
      📸 Aún no hay fotografías agregadas.
    </div>

    <!-- Lightbox Modal para visualización pantalla completa -->
    <Transition name="fade">
      <div 
        v-if="lightboxOpen" 
        class="fixed inset-0 z-[300] flex items-center justify-center bg-black/95 backdrop-blur-md p-4"
        @click="closeLightbox"
      >
        <button 
          @click.stop="closeLightbox" 
          class="absolute top-6 right-6 text-white/75 hover:text-white text-3xl font-black focus:outline-none transition-colors w-12 h-12 flex items-center justify-center bg-white/10 rounded-full hover:bg-white/20"
        >
          ✕
        </button>

        <!-- Navegación Izquierda -->
        <button 
          v-if="config.images.length > 1"
          @click.stop="prevPhoto" 
          class="absolute left-4 md:left-8 text-white/75 hover:text-white text-3xl font-black w-14 h-14 flex items-center justify-center bg-white/10 rounded-full hover:bg-white/20 focus:outline-none transition-all"
        >
          ⟨
        </button>

        <!-- Contenedor Imagen Central con zoom fluido -->
        <div class="relative max-w-full max-h-[85vh] overflow-hidden flex items-center justify-center" @click.stop>
          <img 
            :src="config.images[currentIndex]" 
            alt="Foto pantalla completa" 
            class="object-contain max-w-[90vw] max-h-[80vh] rounded-xl shadow-2xl select-none"
          />
          <div class="absolute bottom-[-2.5rem] left-0 right-0 text-center text-white/60 font-semibold text-sm">
            {{ currentIndex + 1 }} / {{ config.images.length }}
          </div>
        </div>

        <!-- Navegación Derecha -->
        <button 
          v-if="config.images.length > 1"
          @click.stop="nextPhoto" 
          class="absolute right-4 md:right-8 text-white/75 hover:text-white text-3xl font-black w-14 h-14 flex items-center justify-center bg-white/10 rounded-full hover:bg-white/20 focus:outline-none transition-all"
        >
          ⟩
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      title: 'Nuestra Galería',
      description: '',
      images: []
    })
  }
});

const lightboxOpen = ref(false);
const currentIndex = ref(0);

const openLightbox = (index) => {
  currentIndex.value = index;
  lightboxOpen.value = true;
  document.body.style.overflow = 'hidden';
};

const closeLightbox = () => {
  lightboxOpen.value = false;
  document.body.style.overflow = '';
};

const nextPhoto = () => {
  if (props.config.images.length > 0) {
    currentIndex.value = (currentIndex.value + 1) % props.config.images.length;
  }
};

const prevPhoto = () => {
  if (props.config.images.length > 0) {
    currentIndex.value = (currentIndex.value - 1 + props.config.images.length) % props.config.images.length;
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
