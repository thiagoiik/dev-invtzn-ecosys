<template>
  <div 
    v-if="config && config.type"
    class="dress-code-wrapper py-10 px-5 sm:py-14 sm:px-8 max-w-2xl mx-auto w-full my-8 group"
  >
    <!-- Glassmorphism Card -->
    <div class="relative overflow-hidden bg-white/30 dark:bg-black/20 backdrop-blur-xl rounded-[2rem] border border-white/40 dark:border-slate-700/50 shadow-xl transition-all duration-500 hover:-translate-y-1 hover:shadow-primary/20">
      
      <!-- Decorative Background Glow -->
      <div class="absolute -top-24 -right-24 w-48 h-48 bg-primary/20 rounded-full blur-3xl opacity-50 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"></div>
      <div class="absolute -bottom-24 -left-24 w-48 h-48 bg-primary/10 rounded-full blur-3xl opacity-50 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"></div>

      <div class="relative p-8 sm:p-12 text-center flex flex-col items-center justify-center space-y-6">
        
        <!-- Icon / Silhouette -->
        <div class="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center mb-2 transform group-hover:scale-110 transition-transform duration-500">
          <div class="absolute inset-0 bg-primary/10 rounded-full blur-md"></div>
          <div class="absolute inset-2 bg-gradient-to-br from-white/60 to-white/20 dark:from-slate-800/60 dark:to-slate-900/20 rounded-full border border-white/40 dark:border-slate-700/50 backdrop-blur-sm"></div>
          
          <img v-if="config.icon && isUrl(config.icon)" :src="config.icon" class="relative w-12 h-12 sm:w-14 sm:h-14 object-contain z-10 drop-shadow-md" alt="icon" />
          <span v-else class="relative text-4xl sm:text-5xl block select-none z-10 drop-shadow-lg" v-html="typeIcon"></span>
        </div>

        <!-- Typography & Titles -->
        <div class="space-y-3 z-10 w-full">
          <h2 class="text-2xl sm:text-3xl font-black text-slate-800 dark:text-slate-100 tracking-tight" style="font-family: var(--title-font, inherit);">
            Código de Vestimenta
          </h2>
          
          <!-- Decorative Divider -->
          <div class="flex items-center justify-center gap-3 opacity-60">
            <div class="h-px w-12 bg-gradient-to-r from-transparent to-primary"></div>
            <div class="w-1.5 h-1.5 rotate-45 bg-primary"></div>
            <div class="h-px w-12 bg-gradient-to-l from-transparent to-primary"></div>
          </div>
        </div>

        <!-- Badge & Details -->
        <div class="z-10 w-full flex flex-col items-center gap-4 mt-2">
          <div class="inline-flex items-center justify-center bg-gradient-to-r from-primary/15 to-primary/5 dark:from-primary/20 dark:to-primary/10 border border-primary/30 text-primary dark:text-primary-light font-black px-6 py-2.5 rounded-full uppercase tracking-[0.2em] text-xs sm:text-sm shadow-inner">
            {{ dressCodeLabel }}
          </div>
          
          <p v-if="config.details" class="text-sm sm:text-base text-slate-700 dark:text-slate-300 max-w-md mx-auto leading-relaxed mt-2 whitespace-pre-line font-medium px-4">
            {{ config.details }}
          </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      type: 'FORMAL',
      details: '',
      icon: ''
    })
  }
});

const isUrl = (val) => {
  if (!val) return false;
  return val.startsWith('http') || val.startsWith('/') || val.startsWith('.') || val.includes('/');
};

const typeIcon = computed(() => {
  if (props.config.icon && !isUrl(props.config.icon)) {
    return props.config.icon; // El usuario puso un emoji personalizado, respetarlo.
  }
  
  const icons = {
    'FORMAL': '👔👗',
    'ETIQUETA': '✨🥂',
    'COCKTAIL': '🍸👗',
    'GUAYABERA': '🌴🍃',
    'CASUAL': '🕶️👟',
    'PLAYA': '🏖️🐚'
  };
  return icons[props.config.type] || '👗👔';
});

const dressCodeLabel = computed(() => {
  const types = {
    'FORMAL': 'Formal',
    'ETIQUETA': 'Etiqueta / Gala',
    'COCKTAIL': 'Cóctel',
    'GUAYABERA': 'Guayabera',
    'CASUAL': 'Casual',
    'PLAYA': 'Playa'
  };
  return types[props.config.type] || props.config.type || 'Formal';
});
</script>
