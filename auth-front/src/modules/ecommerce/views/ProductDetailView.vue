<template>
  <div class="max-w-6xl mx-auto space-y-8">
    
    <div class="text-center">
      <h2 class="text-4xl font-extrabold text-slate-800">{{ product?.name || 'Cargando...' }}</h2>
      <div v-if="product?.has_template" class="badge badge-accent badge-lg mt-4 font-bold border-none bg-amber-100 text-amber-700">★ Diseño Interactivo Incluido</div>
    </div>

    <div v-if="!product" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-12 mt-8">
      
      <!-- Visualización del producto -->
      <div class="bg-slate-100 rounded-3xl min-h-[500px] flex items-center justify-center relative overflow-hidden border-2 border-dashed border-slate-300">
        <div class="absolute inset-0 bg-gradient-to-tr from-primary/5 to-transparent"></div>
        <span class="text-slate-400 font-medium z-10 flex flex-col items-center gap-4">
          <span class="text-6xl">🖼️</span>
          Previsualización del Diseño
        </span>
      </div>

      <!-- Información y Acciones -->
      <div class="card bg-white shadow-xl border border-slate-100 h-fit">
        <div class="card-body p-8 lg:p-10">
          <h3 class="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-4 mb-4">Detalles del Producto</h3>
          
          <p class="text-slate-600 leading-relaxed text-lg mb-8">{{ product?.description || 'Sin descripción detallada.' }}</p>
          
          <div class="bg-slate-50 p-6 rounded-2xl border border-slate-100 mb-8 flex justify-between items-center">
            <span class="text-slate-500 font-medium uppercase tracking-wider text-sm">Inversión</span>
            <span class="text-4xl font-black text-slate-800">${{ product?.base_price }} <span class="text-lg text-slate-400 font-normal">MXN</span></span>
          </div>
          
          <div class="card-actions flex-col gap-4">
            <button class="btn btn-primary btn-lg w-full text-lg h-16 shadow-lg shadow-primary/30" @click="buyNow">
              💳 Comprar Ahora
            </button>
            
            <button v-if="product?.has_template" class="btn btn-outline btn-lg w-full text-lg h-16 border-slate-300 text-slate-600 hover:bg-slate-50 hover:text-slate-800 hover:border-slate-400" @click="trySandbox" :disabled="loadingSandbox">
              <span v-if="loadingSandbox" class="loading loading-spinner"></span>
              {{ loadingSandbox ? 'Preparando...' : '🛠️ Probar Gratis en Sandbox' }}
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const product = ref(null);
const loadingSandbox = ref(false);

onMounted(async () => {
  try {
    const productId = route.params.id;
    // Por ahora, traemos todo el catálogo y filtramos en frontend (lo ideal sería un GET /products/:id)
    const response = await catalogService.fetchProducts();
    product.value = response.data.find(p => p.id === parseInt(productId));
    
    if (!product.value) {
      toast.error('Producto no encontrado');
      router.push('/catalog');
    }
  } catch (error) {
    toast.error('Error al cargar detalles');
  }
});

const trySandbox = async () => {
  loadingSandbox.value = true;
  try {
    await deploymentService.createSandbox(product.value.id);
    toast.success('¡Tu entorno de prueba está listo!');
    // Aquí el roadmap dice redirigir a DraftSuccess, por ahora mandaremos al dashboard
    router.push('/dashboard'); 
  } catch (error) {
    toast.error('Necesitas iniciar sesión para probar la invitación.');
    router.push('/login');
  } finally {
    loadingSandbox.value = false;
  }
};

const buyNow = () => {
  router.push({ name: 'checkout', params: { id: product.value.id } });
};
</script>

<style scoped>
/* Estilos manuales eliminados. Tailwind se encarga de todo. */
</style>
