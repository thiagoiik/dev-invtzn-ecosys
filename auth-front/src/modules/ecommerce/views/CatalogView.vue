<template>
  <div class="min-h-screen bg-slate-50">
    <HeroBanner @explore="scrollToCatalog" />

    <div ref="catalogSection" class="container mx-auto px-6 py-20 space-y-16">
      <!-- Breadcrumbs -->
      <nav class="flex text-sm font-bold uppercase tracking-widest text-slate-400">
        <router-link to="/" class="hover:text-primary transition-colors">Inicio</router-link>
        <span class="mx-2">/</span>
        <span class="text-slate-600">Catálogo</span>
      </nav>

      <div class="text-center max-w-3xl mx-auto space-y-4">
        <h2 class="text-4xl font-black text-slate-900 tracking-tight">Colecciones Exclusivas</h2>
        <p class="text-lg text-slate-500 leading-relaxed">Seleccionamos cuidadosamente cada diseño para garantizar que tu evento comience con la elegancia que merece.</p>
        <div class="w-20 h-1.5 bg-primary mx-auto rounded-full"></div>
      </div>

      <!-- Categorías de Catálogo -->
      <div class="flex flex-wrap justify-center gap-4 py-2">
        <button 
          v-for="cat in ['ALL', 'DIGITAL', 'SERVICE']" 
          :key="cat"
          @click="selectedCategory = cat"
          class="btn rounded-full px-6 py-2.5 font-bold transition-all duration-300"
          :class="selectedCategory === cat ? 'btn-primary shadow-lg shadow-primary/20 scale-105' : 'btn-ghost text-slate-500 hover:bg-slate-100'"
        >
          {{ translateCategory(cat) }}
        </button>
      </div>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
    
    <div v-else-if="products.length === 0" class="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 text-center">
      <div class="text-5xl mb-4">🛍️</div>
      <h3 class="text-xl font-bold text-slate-800">Próximamente</h3>
      <p class="text-slate-500 mt-2">Aún no hay productos disponibles en el catálogo.</p>
    </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 justify-items-center">
        <div v-for="product in filteredProducts" :key="product.id" 
          @click="openProductModal(product)"
          class="group cursor-pointer relative bg-slate-900 aspect-[9/16] w-full max-w-[300px] rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.10)] hover:shadow-[0_25px_60px_rgba(0,0,0,0.25)] hover:scale-[1.03] hover:-translate-y-2 transition-all duration-500 border border-slate-100 overflow-hidden"
        >
          <!-- Card Background Preview (CoverBlock or fallback image) -->
          <div 
            v-if="product.has_template && product.template_config" 
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
          <template v-else>
            <img 
              v-if="product.thumbnail_url" 
              :src="product.thumbnail_url" 
              alt="Vista previa" 
              class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
            />
            <div v-else class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-primary/20 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-105 transition-transform duration-700 ease-out">💎</span>
            </div>
          </template>

          <!-- Hover Overlay Info (Micro-interaction) -->
          <div class="absolute inset-0 bg-slate-950/0 group-hover:bg-slate-950/40 transition-colors duration-500 flex items-center justify-center z-20">
            <span class="opacity-0 group-hover:opacity-100 transition-all duration-500 bg-white text-slate-955 px-5 py-2.5 rounded-full text-xs font-black uppercase tracking-widest shadow-xl transform translate-y-4 group-hover:translate-y-0">
              Ver Detalles
            </span>
          </div>

          <!-- Product Type Badge (absolute top right) -->
          <div class="absolute top-5 right-5 z-20">
            <span class="bg-slate-950/80 backdrop-blur-md text-white px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest shadow-sm">
              {{ translateType(product.product_type) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Product Details Modal -->
      <div 
        v-if="isDetailsModalOpen && selectedProductForModal" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-955/60 backdrop-blur-sm"
        @click.self="closeProductModal"
      >
        <div 
          class="bg-white rounded-[2rem] max-w-lg w-full overflow-hidden shadow-2xl border border-slate-100 animate-fade-in-up"
        >
          <!-- Modal Header Preview (mini header) -->
          <div class="h-48 bg-slate-900 relative overflow-hidden flex items-center justify-center">
            <div 
              v-if="selectedProductForModal.has_template && selectedProductForModal.template_config" 
              class="absolute inset-0 pointer-events-none"
            >
              <div 
                class="absolute top-0 left-0 w-[200%] h-[200%] origin-top-left scale-50"
              >
                <CoverBlock 
                  :config="getCoverConfig(selectedProductForModal.template_config)"
                  :style="{ minHeight: '100%', height: '100%', ...getThemeVariables(selectedProductForModal.template_config) }"
                />
              </div>
            </div>
            <template v-else>
              <img 
                v-if="selectedProductForModal.thumbnail_url" 
                :src="selectedProductForModal.thumbnail_url" 
                alt="Vista previa" 
                class="absolute inset-0 w-full h-full object-cover"
              />
              <div v-else class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-primary/20 flex items-center justify-center">
                <span class="text-5xl">💎</span>
              </div>
            </template>
            
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/10 to-transparent"></div>
            
            <!-- Close button -->
            <button 
              @click="closeProductModal" 
              class="absolute top-4 right-4 w-9 h-9 flex items-center justify-center bg-white/20 hover:bg-white/40 text-white rounded-full backdrop-blur-md transition-colors border-none cursor-pointer"
            >
              ✕
            </button>
            
            <!-- Title overlay -->
            <div class="absolute bottom-4 left-6 text-white">
              <span class="bg-primary text-white text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded">
                {{ translateType(selectedProductForModal.product_type) }}
              </span>
              <h3 class="text-2xl font-bold mt-1">{{ selectedProductForModal.name }}</h3>
            </div>
          </div>

          <!-- Modal Body -->
          <div class="p-8 space-y-6">
            <div class="space-y-2">
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400">Descripción</h4>
              <p class="text-slate-600 text-sm leading-relaxed">
                {{ selectedProductForModal.description || 'Una pieza maestra diseñada para cautivar a tus invitados desde el primer clic.' }}
              </p>
            </div>

            <!-- Price & Features Summary -->
            <div class="flex items-center justify-between p-4 rounded-2xl bg-slate-50 border border-slate-100">
              <div>
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Precio desde</span>
                <p class="text-3xl font-black text-slate-950">${{ selectedProductForModal.base_price }} <span class="text-xs font-medium text-slate-400">MXN</span></p>
              </div>
              <div v-if="selectedProductForModal.has_template" class="text-right">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Tipo</span>
                <p class="text-sm font-black text-amber-600">Interactivo Digital</p>
              </div>
            </div>

            <!-- Modal Actions -->
            <div class="flex gap-4 pt-2">
              <button 
                v-if="selectedProductForModal.product_type === 'DIGITAL' && selectedProductForModal.template_slug"
                class="btn btn-outline flex-1 rounded-xl h-12 font-bold hover:bg-slate-100 hover:text-slate-900 border-slate-200 text-slate-700"
                @click="handlePreviewFromModal"
              >
                Ver Demo
              </button>
              <button 
                class="btn btn-primary flex-1 rounded-xl h-12 font-black shadow-lg shadow-primary/20"
                @click="handleBuyFromModal"
              >
                Características
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import HeroBanner from '../components/HeroBanner.vue';
import CoverBlock from '@/modules/engine/components/CoverBlock.vue';

const getCoverConfig = (templateConfig) => {
  if (!templateConfig) return {};
  if (templateConfig.cover) {
    return templateConfig.cover;
  }
  if (Array.isArray(templateConfig.blocks)) {
    const coverBlock = templateConfig.blocks.find(b => b.type === 'CoverBlock');
    if (coverBlock) {
      return coverBlock.config || {};
    }
  }
  return {};
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

const router = useRouter();
const toast = useToast();
const products = ref([]);
const loading = ref(true);
const catalogSection = ref(null);
const selectedCategory = ref('ALL');

const selectedProductForModal = ref(null);
const isDetailsModalOpen = ref(false);

const openProductModal = (product) => {
  selectedProductForModal.value = product;
  isDetailsModalOpen.value = true;
};

const closeProductModal = () => {
  selectedProductForModal.value = null;
  isDetailsModalOpen.value = false;
};

const handlePreviewFromModal = () => {
  if (selectedProductForModal.value) {
    handlePreview(selectedProductForModal.value);
  }
};

const handleBuyFromModal = () => {
  if (selectedProductForModal.value) {
    handleBuy(selectedProductForModal.value);
    closeProductModal();
  }
};

const scrollToCatalog = () => {
  catalogSection.value?.scrollIntoView({ behavior: 'smooth' });
};

const loadProducts = async () => {
  loading.value = true;
  try {
    const response = await catalogService.fetchProducts();
    // Filtramos solo los productos activos. Si es DIGITAL, debe tener plantilla (has_template = true) para mostrarse en el catálogo principal de diseños.
    products.value = response.data.filter(p => 
      p.is_active && ['DIGITAL', 'PHYSICAL', 'SERVICE'].includes(p.product_type) && (p.product_type !== 'DIGITAL' || p.has_template)
    );
  } catch (error) {
    toast.error('Ocurrió un error al cargar el catálogo de productos.');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadProducts();
});

const translateCategory = (cat) => {
  const map = {
    'ALL': 'Todos los Productos',
    'DIGITAL': 'Invitaciones Digitales',
    /* 'PHYSICAL': 'Impresos Físicos', */
    'SERVICE': 'Servicios a Medida'
  };
  return map[cat] || cat;
};

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'ALL') {
    return products.value;
  }
  return products.value.filter(p => p.product_type === selectedCategory.value);
});

const translateType = (type) => {
  const typeMap = {
    'DIGITAL': 'Digital',
    'SERVICE': 'Servicio a Medida',
    'PHYSICAL': 'Físico'
  };
  return typeMap[type] || type;
};

const handleBuy = (product) => {
  router.push({ name: 'product-detail', params: { id: product.id } });
};

const handlePreview = (product) => {
  if (product.product_type !== 'DIGITAL') {
    toast.info('Las demos en vivo solo están disponibles para invitaciones digitales.');
    return;
  }
  
  if (!product.template_slug) {
    toast.info('Este diseño no cuenta con una demo en vivo actualmente.');
    return;
  }
  
  window.open(`/i/${product.template_slug}`, '_blank');
};
</script>

<style scoped>
/* Estilos manuales eliminados. Tailwind se encarga. */
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.animate-fade-in-up {
  animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
