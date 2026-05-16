<template>
  <div class="min-h-screen bg-slate-50 py-12 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Breadcrumbs -->
      <nav class="flex mb-8 text-sm font-bold uppercase tracking-widest text-slate-400">
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
        <div class="lg:col-span-7 space-y-8">
          <div class="group relative bg-white rounded-[2.5rem] p-4 shadow-2xl shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="aspect-[4/5] md:aspect-video bg-slate-100 rounded-[2rem] flex items-center justify-center relative overflow-hidden">
              <!-- Background glow -->
              <div class="absolute inset-0 bg-gradient-to-br from-primary/20 via-transparent to-indigo-500/10"></div>
              
              <!-- Content -->
              <div class="relative z-10 text-center space-y-6">
                <div class="w-32 h-32 bg-white rounded-3xl shadow-xl flex items-center justify-center text-6xl mx-auto transform -rotate-6 group-hover:rotate-0 transition-transform duration-500">
                  💎
                </div>
                <div>
                  <h3 class="text-3xl font-black text-slate-800">{{ product.name }}</h3>
                  <p class="text-slate-400 font-medium">Diseño interactivo de alta gama</p>
                </div>
              </div>

              <!-- Badges -->
              <div class="absolute top-8 left-8 flex gap-2">
                <span class="bg-primary text-white px-4 py-1.5 rounded-full text-xs font-black tracking-widest uppercase shadow-lg shadow-primary/20">
                  Best Seller
                </span>
              </div>
            </div>
          </div>

          <!-- Description Section -->
          <div class="bg-white rounded-[2rem] p-10 border border-slate-100 shadow-sm space-y-6">
            <h4 class="text-xl font-black text-slate-900 border-b border-slate-50 pb-4">Acerca de este diseño</h4>
            <p class="text-slate-500 leading-relaxed text-lg">
              {{ product.description || 'Este diseño ha sido meticulosamente creado para reflejar elegancia y modernidad. Con una interfaz fluida y optimizada para dispositivos móviles, tus invitados quedarán maravillados desde el primer segundo.' }}
            </p>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 pt-4">
              <div v-for="feat in ['RSVP Digital', 'Mapa Live', 'Galería', 'Música']" :key="feat" class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-slate-50">
                <span class="text-2xl">✨</span>
                <span class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">{{ feat }}</span>
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
                <button v-if="product.has_template" class="btn btn-ghost w-full text-slate-400 hover:text-white" @click="trySandbox" :disabled="loadingSandbox">
                  <span v-if="loadingSandbox" class="loading loading-spinner"></span>
                  {{ loadingSandbox ? 'Preparando...' : '🛠️ Probar Demo Gratis' }}
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import AddonSelector from '../components/AddonSelector.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const product = ref(null);
const availableAddons = ref([]);
const selectedAddonIds = ref([]);
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

onMounted(async () => {
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

const trySandbox = async () => {
  loadingSandbox.value = true;
  try {
    const res = await deploymentService.createSandbox(product.value.id);
    toast.success('¡Tu entorno de prueba está listo!');
    router.push(`/i/${res.data.slug}`);
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
