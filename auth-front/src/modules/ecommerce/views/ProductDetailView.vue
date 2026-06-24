<template>
  <div class="min-h-screen bg-slate-50 py-12 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Breadcrumbs -->
      <nav class="flex mb-8 text-sm font-bold uppercase tracking-widest text-slate-400">
        <router-link to="/" class="hover:text-primary transition-colors">Inicio</router-link>
        <span class="mx-2">/</span>
        <router-link to="/catalog" class="hover:text-primary transition-colors">Catálogo</router-link>
        <span class="mx-2">/</span>
        <span class="text-slate-600">{{ product?.name || '...' }}</span>
      </nav>

      <div v-if="!product" class="flex flex-col items-center justify-center py-40 space-y-4">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="text-slate-400 font-bold animate-pulse">Cargando experiencia...</p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
        
        <!-- Left: Product Showcase -->
        <div class="lg:col-span-7 space-y-8 flex flex-col items-center">
          <div class="group relative bg-slate-900 aspect-[9/16] w-full max-w-[420px] rounded-[2.5rem] shadow-2xl border border-slate-100 overflow-hidden">
            <!-- Dynamic CSS Preview -->
            <div 
              v-if="product && product.has_template && product.template_config" 
              class="absolute inset-0 overflow-hidden pointer-events-none"
            >
              <div 
                class="absolute top-0 left-0 w-[200%] h-[200%] origin-top-left scale-50"
              >
                <CoverBlock 
                  :config="getCoverConfig(product.template_config)"
                  :style="{ minHeight: '100%', height: '100%', ...getThemeVariables(product.template_config) }"
                />
              </div>
            </div>

            <!-- Fallback Static Image or Gem -->
            <template v-else-if="product">
              <img 
                v-if="product.thumbnail_url" 
                :src="product.thumbnail_url" 
                alt="Vista previa del diseño" 
                class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
              />
              <div v-else class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-primary/20 flex items-center justify-center">
                <!-- Content fallback -->
                <div class="relative z-10 text-center space-y-6">
                  <div class="w-32 h-32 bg-white rounded-3xl shadow-xl flex items-center justify-center text-6xl mx-auto transform -rotate-6 group-hover:rotate-0 transition-transform duration-500">
                    💎
                  </div>
                  <div>
                    <h3 class="text-3xl font-black text-slate-800">{{ product.name }}</h3>
                    <p class="text-slate-400 font-medium">Diseño interactivo de alta gama</p>
                  </div>
                </div>
              </div>
            </template>

            <!-- Badges -->
            <div class="absolute top-6 left-6 flex gap-2">
              <span class="bg-primary text-white px-4 py-1.5 rounded-full text-xs font-black tracking-widest uppercase shadow-lg shadow-primary/20">
                Best Seller
              </span>
            </div>
          </div>

          <!-- Description Section -->
          <div class="bg-white rounded-[2rem] p-10 border border-slate-100 shadow-sm space-y-6 w-full">
            <h4 class="text-xl font-black text-slate-900 border-b border-slate-50 pb-4">Acerca de este diseño</h4>
            <p class="text-slate-500 leading-relaxed text-lg">
              {{ product.description || 'Este diseño ha sido meticulosamente creado para reflejar elegancia y modernidad. Con una interfaz fluida y optimizada para dispositivos móviles, tus invitados quedarán maravillados desde el primer segundo.' }}
            </p>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-6 pt-4">
              <div v-for="feat in dynamicFeatures" :key="feat.name" class="flex flex-col items-center text-center gap-2 p-5 rounded-3xl bg-slate-50 border border-slate-100/50 hover:bg-slate-100/30 transition-colors">
                <span class="text-3xl">{{ feat.icon }}</span>
                <span class="text-[10px] font-black text-slate-900 uppercase tracking-widest mt-1">{{ feat.name }}</span>
                <span class="text-[9px] text-slate-400 font-bold uppercase tracking-tight">{{ feat.desc }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Purchase Sidebar -->
        <div class="lg:col-span-5 space-y-8 sticky top-8">
          <div class="bg-white rounded-[2.5rem] p-10 shadow-2xl shadow-slate-200/50 border border-slate-100 space-y-8">
            <div class="space-y-2">
              <h1 class="text-4xl font-black text-slate-900">{{ product.name }}</h1>
              <div class="flex items-center gap-2">
                <div class="rating rating-xs">
                  <input v-for="i in 5" :key="i" type="radio" class="mask mask-star-2 bg-orange-400" :checked="i === 5" />
                </div>
                <span class="text-xs font-bold text-slate-400">(48 reseñas)</span>
              </div>
            </div>

            <!-- Addon Selector Integration -->
            <AddonSelector :addons="availableAddons" v-model:selectedIds="selectedAddonIds" />

            <!-- Price Breakdown -->
            <div class="bg-slate-950 rounded-3xl p-8 text-white space-y-4">
              <div class="flex justify-between items-center text-slate-400 text-sm font-bold uppercase tracking-widest">
                <span>Total estimado</span>
                <span class="text-primary">MXN</span>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-5xl font-black">${{ totalPrice }}</span>
                <span class="text-slate-500 line-through text-lg" v-if="selectedAddonIds.length > 0">${{ totalPrice + 200 }}</span>
              </div>
              
              <div class="pt-6 space-y-4">
                <button class="btn btn-primary btn-lg w-full rounded-2xl h-16 text-lg font-black shadow-lg shadow-primary/20" @click="buyNow">
                  Continuar al Pago
                </button>
                <button v-if="product.has_template" class="btn btn-ghost w-full text-slate-400 hover:text-white" @click="isModalOpen = true">
                  🛠️ Probar Demo Gratis
                </button>
              </div>
            </div>

            <p class="text-center text-[10px] text-slate-400 font-bold uppercase tracking-widest px-4 leading-relaxed">
              Compra 100% segura. Acceso instantáneo al editor tras el pago exitoso.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Draft Modal -->
    <QuickDraftModal 
      :isOpen="isModalOpen" 
      :productId="product?.id" 
      @close="isModalOpen = false" 
      @success="handleSandboxSuccess" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import AddonSelector from '../components/AddonSelector.vue';
import QuickDraftModal from '../components/QuickDraftModal.vue';
import CoverBlock from '@/modules/engine/components/CoverBlock.vue';

const getCoverConfig = (templateConfig) => {
  if (!templateConfig) return {};
  // La configuración real de la portada siempre se guarda en la raíz (templateConfig.cover)
  // por la arquitectura reactiva del Studio, sin importar si existe en el array de blocks.
  let config = templateConfig.cover || {};
  
  if (Array.isArray(templateConfig.blocks) && Object.keys(config).length === 0) {
    const coverBlock = templateConfig.blocks.find(b => b.type === 'CoverBlock');
    if (coverBlock && coverBlock.config) {
      config = coverBlock.config;
    }
  }
  return config;
};

const getThemeVariables = (templateConfig) => {
  if (!templateConfig) return {};
  const theme = templateConfig.theme || {};
  const h = theme.hue || 38;      // Golden hue
  const s = theme.saturation || '80%';
  const l = theme.lightness || '50%';

  return {
    '--p': `${h} ${s} ${l}`, // Primary brand color variable
  };
};

const route = useRoute();
const router = useRouter();
const toast = useToast();

const product = ref(null);
const availableAddons = ref([]);
const selectedAddonIds = ref([]);
const isModalOpen = ref(false);
const loadingSandbox = ref(false);

const totalPrice = computed(() => {
  if (!product.value) return 0;
  const base = parseFloat(product.value.base_price);
  const addonsTotal = selectedAddonIds.value.reduce((acc, id) => {
    const addon = availableAddons.value.find(a => a.id === id);
    return acc + (addon ? parseFloat(addon.base_price) : 0);
  }, 0);
  return base + addonsTotal;
});

const dynamicFeatures = computed(() => {
  if (!product.value) return [];
  
  // Extraer características reales de los bloques del diseño seleccionado
  const blocks = product.value.template_config?.blocks;
  if (Array.isArray(blocks) && blocks.length > 0) {
    const blockMap = {
      'CoverBlock': { name: 'Portada Impactante', icon: '🎨', desc: 'Diseño visual de inicio' },
      'CountdownBlock': { name: 'Cuenta Regresiva', icon: '🕰️', desc: 'Para el gran día' },
      'LocationBlock': { name: 'Ubicación y Mapas', icon: '📍', desc: 'Rutas e indicaciones' },
      'RSVPBlock': { name: 'Confirmación', icon: '✉️', desc: 'Control de asistencia' },
      'DressCodeBlock': { name: 'Código Vestimenta', icon: '👔', desc: 'Sugerencias de estilo' },
      'GalleryBlock': { name: 'Galería de Fotos', icon: '📸', desc: 'Tus mejores momentos' },
      'AudioBlock': { name: 'Música de Fondo', icon: '🎵', desc: 'Banda sonora' },
      'ScheduleBlock': { name: 'Cronograma', icon: '📅', desc: 'Itinerario del evento' },
      'GiftRegistryBlock': { name: 'Mesa de Regalos', icon: '🎁', desc: 'Sugerencias y detalles' },
      'EnvelopeBlock': { name: 'Sobre Interactivo', icon: '✉️', desc: 'Apertura en 3D' }
    };

    const features = [];
    const seen = new Set();
    blocks.forEach(block => {
      const type = block.type;
      if (blockMap[type] && !seen.has(type)) {
        features.push(blockMap[type]);
        seen.add(type);
      }
    });
    
    // Si es premium, podemos agregar la característica de compartición si hay espacio
    if (product.value.tier_level === 'PREMIUM' && features.length < 6) {
       features.push({ name: 'Compartido Premium', icon: '🔗', desc: 'Vista optimizada en redes' });
    }
    
    if (features.length > 0) {
      return features.slice(0, 6); // Max 6 para encajar bien en el grid (2x3)
    }
  }

  // Fallback si no hay config de bloques
  const tier = product.value.tier_level;
  if (tier === 'PREMIUM') {
    return [
      { name: 'RSVP Avanzado', icon: '✉️', desc: 'Alergias, menú y pases' },
      { name: 'Música de Fondo', icon: '🎵', desc: 'Carga tus archivos' },
      { name: 'Contador', icon: '🕰️', desc: 'Cuenta regresiva' },
      { name: 'Cronograma', icon: '📅', desc: 'Línea de tiempo' },
      { name: 'Sobres 3D', icon: '✉️', desc: 'Apertura interactiva' },
      { name: 'Compartido Premium', icon: '🔗', desc: 'Vista en redes optimizada' }
    ];
  } else if (tier === 'STANDARD') {
    return [
      { name: 'RSVP en Panel', icon: '✉️', desc: 'Control en tiempo real' },
      { name: 'Música de Fondo', icon: '🎵', desc: 'Música predeterminada' },
      { name: 'Contador', icon: '🕰️', desc: 'Cuenta regresiva' },
      { name: 'Temas', icon: '🎨', desc: 'Colores personalizables' }
    ];
  } else {
    return [
      { name: 'RSVP WhatsApp', icon: '🟢', desc: 'Confirmación directa' },
      { name: 'Diseño Básico', icon: '✨', desc: 'Lienzo moderno' }
    ];
  }
});

onMounted(async () => {
  window.scrollTo(0, 0);
  try {
    const productId = route.params.id;
    const response = await catalogService.fetchProducts();
    const allProducts = response.data;
    
    product.value = allProducts.find(p => p.id === parseInt(productId));
    availableAddons.value = allProducts.filter(p => p.product_type === 'SERVICE' && p.is_active);
    
    if (!product.value) {
      toast.error('Producto no encontrado');
      router.push('/catalog');
    }
  } catch (error) {
    toast.error('Error al cargar detalles');
  }
});

const handleSandboxSuccess = (deployment) => {
  isModalOpen.value = false;
  // Guardamos en localStorage para persistencia anónima
  localStorage.setItem('pending_sandbox_id', deployment.id);
  
  // Abrimos en nueva pestaña o redirigimos
  window.open(`/i/${deployment.slug}`, '_blank');
};

const buyNow = () => {
  localStorage.setItem('selected_addon_ids', JSON.stringify(selectedAddonIds.value));
  router.push({ name: 'checkout', params: { id: product.value.id } });
};
</script>

<style scoped>
/* Estilos manuales eliminados. Tailwind se encarga de todo. */
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>
