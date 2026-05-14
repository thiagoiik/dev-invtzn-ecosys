<template>
  <div class="space-y-8">
    <div class="text-center max-w-2xl mx-auto">
      <h2 class="text-3xl font-extrabold text-slate-800">Catálogo de Productos</h2>
      <p class="text-slate-500 mt-2">Explora nuestras plantillas e invitaciones premium disponibles para tu próximo evento.</p>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
    
    <div v-else-if="products.length === 0" class="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 text-center">
      <div class="text-5xl mb-4">🛍️</div>
      <h3 class="text-xl font-bold text-slate-800">Próximamente</h3>
      <p class="text-slate-500 mt-2">Aún no hay productos disponibles en el catálogo.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="product in products" :key="product.id" class="card bg-white shadow-lg border border-slate-100 transition-all hover:-translate-y-2 hover:shadow-2xl overflow-hidden group">
        
        <!-- Imagen de placeholder por ahora, como decoración -->
        <figure class="h-48 bg-slate-100 flex items-center justify-center relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent"></div>
          <span class="text-5xl group-hover:scale-110 transition-transform duration-300">🎟️</span>
        </figure>

        <div class="card-body">
          <div class="flex gap-2 flex-wrap mb-2">
            <span class="badge badge-primary badge-outline">{{ translateType(product.product_type) }}</span>
            <span v-if="product.has_template" class="badge badge-accent badge-outline">★ Diseño Interactivo</span>
          </div>

          <h3 class="card-title text-xl text-slate-800">{{ product.name }}</h3>
          <p class="text-slate-500 text-sm flex-grow line-clamp-3">{{ product.description || 'Sin descripción disponible.' }}</p>
          
          <div class="card-actions justify-between items-center mt-6 pt-4 border-t border-slate-100">
            <span class="text-2xl font-black text-slate-800">${{ product.base_price }} <span class="text-xs text-slate-400 font-normal">MXN</span></span>
            <button class="btn btn-primary" @click="handleBuy(product)">Ver Detalles</button>
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

const router = useRouter();
const toast = useToast();
const products = ref([]);
const loading = ref(true);

const loadProducts = async () => {
  loading.value = true;
  try {
    const response = await catalogService.fetchProducts();
    // Filtramos solo los productos activos
    products.value = response.data.filter(p => p.is_active);
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
