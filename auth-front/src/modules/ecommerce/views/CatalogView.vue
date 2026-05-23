<template>
  <div class="min-h-screen bg-slate-50">
    <HeroBanner @explore="scrollToCatalog" />

    <div ref="catalogSection" class="container mx-auto px-6 py-20 space-y-16">
      <div class="text-center max-w-3xl mx-auto space-y-4">
        <h2 class="text-4xl font-black text-slate-900 tracking-tight">Colecciones Exclusivas</h2>
        <p class="text-lg text-slate-500 leading-relaxed">Seleccionamos cuidadosamente cada diseño para garantizar que tu evento comience con la elegancia que merece.</p>
        <div class="w-20 h-1.5 bg-primary mx-auto rounded-full"></div>
      </div>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
    
    <div v-else-if="products.length === 0" class="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 text-center">
      <div class="text-5xl mb-4">🛍️</div>
      <h3 class="text-xl font-bold text-slate-800">Próximamente</h3>
      <p class="text-slate-500 mt-2">Aún no hay productos disponibles en el catálogo.</p>
    </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div v-for="product in products" :key="product.id" 
          class="group bg-white rounded-3xl shadow-sm hover:shadow-2xl transition-all duration-500 border border-slate-100 overflow-hidden flex flex-col h-full"
        >
          <!-- Premium Product Figure -->
          <figure class="h-64 bg-slate-100 relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-900/40 to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <!-- Aquí iría la imagen real del producto si existiera, usamos un gradiente por ahora -->
            <div class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-primary/20 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform duration-700 ease-out">💎</span>
            </div>
            
            <div class="absolute top-4 right-4 z-20">
              <span class="bg-white/90 backdrop-blur-md text-slate-900 px-3 py-1 rounded-full text-xs font-bold shadow-sm">
                {{ translateType(product.product_type) }}
              </span>
            </div>
          </figure>

          <div class="p-8 flex flex-col flex-1 space-y-4">
            <div class="flex items-center gap-2">
              <span v-if="product.has_template" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-amber-50 text-amber-600 border border-amber-100">
                INTERACTIVO
              </span>
            </div>

            <h3 class="text-2xl font-bold text-slate-900 group-hover:text-primary transition-colors">{{ product.name }}</h3>
            
            <p class="text-slate-500 text-sm leading-relaxed line-clamp-3 flex-1">
              {{ product.description || 'Una pieza maestra diseñada para cautivar a tus invitados desde el primer clic.' }}
            </p>
            
            <div class="flex items-center justify-between pt-6 border-t border-slate-50">
              <div class="flex flex-col">
                <span class="text-xs text-slate-400 font-bold uppercase tracking-wider">Desde</span>
                <span class="text-3xl font-black text-slate-900">${{ product.base_price }}</span>
              </div>
              <button 
                class="btn btn-primary rounded-2xl px-6 shadow-lg shadow-primary/20 group-hover:scale-105 transition-transform"
                @click="handleBuy(product)"
              >
                Personalizar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import HeroBanner from '../components/HeroBanner.vue';

const router = useRouter();
const toast = useToast();
const products = ref([]);
const loading = ref(true);
const catalogSection = ref(null);

const scrollToCatalog = () => {
  catalogSection.value?.scrollIntoView({ behavior: 'smooth' });
};

const loadProducts = async () => {
  loading.value = true;
  try {
    const response = await catalogService.fetchProducts();
    // Filtramos solo los productos activos, plantillas y físicos (ocultando Tiers/Servicios)
    products.value = response.data.filter(p => 
      p.is_active && ['DIGITAL', 'PHYSICAL'].includes(p.product_type)
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

const translateType = (type) => {
  const types = {
    'DIGITAL': 'Digital',
    'PHYSICAL': 'Impreso',
    'SERVICE': 'Servicio'
  };
  return types[type] || type;
};

const handleBuy = (product) => {
  router.push({ name: 'product-detail', params: { id: product.id } });
};
</script>

<style scoped>
/* Estilos manuales eliminados. Tailwind se encarga. */
</style>
