<template>
  <div class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6 animate-fade-in">
    <!-- Backdrop Blur -->
    <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="$emit('close')"></div>
    
    <!-- Modal Content -->
    <div class="relative w-full max-w-5xl bg-white/10 backdrop-blur-xl border border-white/20 rounded-[2.5rem] shadow-2xl shadow-black/50 overflow-hidden flex flex-col max-h-[95vh]">
      
      <!-- Close button -->
      <button 
        @click="$emit('close')"
        class="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors z-10"
      >
        ✕
      </button>

      <!-- Header -->
      <div class="text-center p-8 md:p-10 pb-6">
        <h2 class="text-3xl md:text-4xl font-black text-white mb-3">Sube de Nivel tu Evento ✨</h2>
        <p class="text-slate-200 text-sm md:text-base max-w-2xl mx-auto">
          Desbloquea animaciones 3D impresionantes, cronogramas detallados y el codiciado "Wow Factor" musical.
        </p>
      </div>

      <!-- Pricing Cards Scrollable Area -->
      <div class="flex-1 overflow-y-auto p-6 md:p-10 pt-0 pb-10">
        
        <div v-if="loading" class="flex justify-center items-center py-20 text-white gap-3">
          <div class="w-6 h-6 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
          Cargando planes disponibles...
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- Basic Tier (Free/Fallback if not loaded) -->
          <div class="pricing-card bg-slate-800/80 border-slate-700">
            <div class="text-slate-400 text-xs font-black uppercase tracking-widest mb-4">Plan Actual</div>
            <h3 class="text-2xl font-bold text-white mb-2">Básico</h3>
            <div class="text-4xl font-black text-white mb-6">Gratis</div>
            <ul class="space-y-3 mb-8 flex-1">
              <li class="flex items-center gap-2 text-slate-300 text-sm">
                <span class="text-emerald-400">✓</span> Diseño Base de Invitación
              </li>
              <li class="flex items-center gap-2 text-slate-300 text-sm">
                <span class="text-emerald-400">✓</span> Formulario de RSVP
              </li>
              <li class="flex items-center gap-2 text-slate-500 text-sm opacity-50">
                <span class="text-slate-600">✕</span> Cuenta Regresiva
              </li>
              <li class="flex items-center gap-2 text-slate-500 text-sm opacity-50">
                <span class="text-slate-600">✕</span> Sobres 3D y Sonido
              </li>
            </ul>
            <button 
              class="w-full py-3 rounded-xl bg-slate-700/50 text-slate-300 font-bold cursor-not-allowed"
              disabled
            >
              Plan Activo
            </button>
          </div>

          <!-- Dynamic Products from Catalog (Standard & Premium) -->
          <div 
            v-for="(product, idx) in premiumProducts" 
            :key="product.id"
            class="pricing-card relative overflow-hidden group"
            :class="idx === 1 ? 'bg-gradient-to-b from-indigo-900/90 to-slate-900/90 border-indigo-500/50 transform md:-translate-y-4 shadow-xl shadow-indigo-500/20' : 'bg-slate-800/90 border-slate-600/50 hover:border-slate-400/50'"
          >
            <!-- Popular Badge for Premium -->
            <div v-if="idx === 1" class="absolute top-0 inset-x-0 bg-indigo-500 text-white text-[10px] font-black uppercase tracking-widest text-center py-1">
              Más Popular
            </div>

            <div class="text-indigo-300 text-xs font-black uppercase tracking-widest mb-4 mt-2">
              Nivel {{ idx === 0 ? 'Standard' : 'Premium' }}
            </div>
            
            <h3 class="text-2xl font-bold text-white mb-2">{{ product.name }}</h3>
            <div class="text-4xl font-black text-white mb-2">${{ product.base_price }}<span class="text-sm text-slate-400 ml-1">MXN</span></div>
            <p class="text-xs text-slate-400 mb-6 min-h-[40px]">{{ product.description }}</p>
            
            <ul class="space-y-3 mb-8 flex-1">
              <li class="flex items-center gap-2 text-slate-200 text-sm">
                <span class="text-emerald-400">✓</span> Todo lo de Básico
              </li>
              <li class="flex items-center gap-2 text-slate-200 text-sm">
                <span class="text-emerald-400">✓</span> Cuenta Regresiva
              </li>
              <li class="flex items-center gap-2 text-sm" :class="idx === 1 ? 'text-white font-bold' : 'text-slate-500 opacity-50'">
                <span :class="idx === 1 ? 'text-emerald-400' : 'text-slate-600'">{{ idx === 1 ? '✓' : '✕' }}</span> Sobres 3D Premium
              </li>
              <li class="flex items-center gap-2 text-sm" :class="idx === 1 ? 'text-white font-bold' : 'text-slate-500 opacity-50'">
                <span :class="idx === 1 ? 'text-emerald-400' : 'text-slate-600'">{{ idx === 1 ? '✓' : '✕' }}</span> Música Sintetizada
              </li>
              <li class="flex items-center gap-2 text-sm" :class="idx === 1 ? 'text-white font-bold' : 'text-slate-500 opacity-50'">
                <span :class="idx === 1 ? 'text-emerald-400' : 'text-slate-600'">{{ idx === 1 ? '✓' : '✕' }}</span> Cronograma / Itinerario
              </li>
            </ul>

            <button 
              @click="$emit('select-tier', product.id)"
              class="w-full py-3 rounded-xl font-black text-sm transition-all duration-300 hover:scale-105 active:scale-95"
              :class="idx === 1 ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/30' : 'bg-slate-100 text-slate-900 hover:bg-white'"
            >
              Seleccionar y Pagar
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { catalogService } from '@/modules/ecommerce/services/catalogService';

const emit = defineEmits(['close', 'select-tier']);
const loading = ref(true);
const premiumProducts = ref([]);

onMounted(async () => {
  try {
    const res = await catalogService.fetchProducts();
    // Suponemos que los productos tienen is_physical=false o ciertos nombres
    // Para no mostrar complementos físicos en el tier, filtramos los principales
    const mainProducts = res.data.filter(p => !p.is_physical && parseFloat(p.base_price) > 0);
    // Tomamos hasta 2 productos (Standard y Premium) para la demo
    premiumProducts.value = mainProducts.slice(0, 2);
  } catch (error) {
    console.error("Error cargando productos de catálogo", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.pricing-card {
  border: 1px solid;
  border-radius: 1.5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}
</style>
