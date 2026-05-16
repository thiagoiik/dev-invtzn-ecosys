<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6">
    <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12">
      
      <!-- Left: Order Summary & Info -->
      <div class="lg:col-span-7 space-y-8">
        <div class="bg-white rounded-[2rem] p-10 shadow-sm border border-slate-100">
          <h2 class="text-3xl font-black text-slate-900 mb-8">Resumen de tu Compra</h2>
          
          <div v-if="product" class="space-y-6">
            <div class="flex gap-6 p-4 rounded-2xl bg-slate-50 border border-slate-100">
              <div class="w-24 h-24 bg-white rounded-xl shadow-sm flex items-center justify-center text-4xl">
                💎
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-bold text-slate-800">{{ product.name }}</h3>
                <p class="text-sm text-slate-500 line-clamp-2 mt-1">{{ product.description || 'Diseño premium interactivo.' }}</p>
                <div class="mt-2 font-black text-slate-900">${{ product.base_price }} MXN</div>
              </div>
            </div>

            <!-- Aquí podrías iterar addons si los pasaras por params o store -->
            <div class="space-y-4 pt-4">
              <h4 class="text-xs font-black text-slate-400 uppercase tracking-widest">Incluye:</h4>
              <ul class="space-y-3">
                <li v-for="item in ['Soporte VIP 24/7', 'Hosting ilimitado', 'RSVP en tiempo real']" :key="item" class="flex items-center gap-3 text-slate-600 text-sm">
                  <svg class="h-5 w-5 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-6 p-6 rounded-2xl bg-indigo-50 border border-indigo-100">
          <span class="text-3xl">🛡️</span>
          <div>
            <h4 class="font-bold text-indigo-900">Garantía de Satisfacción</h4>
            <p class="text-sm text-indigo-700/70">Si no estás conforme con el diseño tras 24h, te devolvemos tu dinero sin preguntas.</p>
          </div>
        </div>
      </div>

      <!-- Right: Checkout Card -->
      <div class="lg:col-span-5 space-y-6">
        <div class="bg-white rounded-[2rem] p-10 shadow-2xl shadow-slate-200/50 border border-slate-100">
          <div class="space-y-6">
            <div class="flex justify-between items-center pb-6 border-b border-slate-50">
              <span class="text-slate-400 font-bold uppercase tracking-widest text-xs">Total del pedido</span>
              <span class="text-3xl font-black text-slate-900" v-if="product">${{ product.base_price }}</span>
            </div>

            <div class="space-y-4">
              <button 
                class="btn btn-primary btn-lg w-full h-16 rounded-2xl text-lg font-black shadow-lg shadow-primary/20"
                @click="initiateStripePayment"
                :disabled="loading"
              >
                <span v-if="loading" class="loading loading-spinner"></span>
                {{ loading ? 'Preparando Pago...' : 'Confirmar y Pagar' }}
              </button>
              
              <div class="flex items-center justify-center gap-4 py-2 opacity-50 grayscale">
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg" alt="Stripe" class="h-6" />
              </div>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 border border-slate-100 flex gap-4">
              <span class="text-2xl">📧</span>
              <p class="text-[10px] text-slate-500 font-medium leading-relaxed">
                Al pagar, aceptas nuestros términos de servicio. Recibirás tu recibo fiscal y acceso al editor vía correo electrónico.
              </p>
            </div>
          </div>
        </div>

        <!-- Security Badges -->
        <div class="grid grid-cols-3 gap-4 text-center opacity-40">
          <div class="space-y-1">
            <div class="text-xl">SSL</div>
            <div class="text-[8px] font-black uppercase">Seguro</div>
          </div>
          <div class="space-y-1">
            <div class="text-xl">PCI</div>
            <div class="text-[8px] font-black uppercase">Cumplimiento</div>
          </div>
          <div class="space-y-1">
            <div class="text-xl">256</div>
            <div class="text-[8px] font-black uppercase">Bits AES</div>
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
import { useAuthStore } from '@/modules/auth/store/auth';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { orderService } from '@/modules/ecommerce/services/orderService';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const product = ref(null);
const loading = ref(false);

onMounted(async () => {
  try {
    const productId = route.params.id;
    const response = await catalogService.fetchProducts();
    product.value = response.data.find(p => p.id === parseInt(productId));
    
    if (!product.value) {
      toast.error('Producto no válido');
      router.push('/catalog');
    }
  } catch (error) {
    toast.error('Error al cargar la orden');
  }
});

const initiateStripePayment = async () => {
  // 1. Verificación de Autenticación
  if (!authStore.isAuthenticated) {
    toast.info('Para continuar con la compra, por favor inicia sesión o regístrate.');
    // Guardamos la intención de compra para retornar después
    localStorage.setItem('pending_checkout_id', product.value.id);
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }

  loading.value = true;
  try {
    // 2. Crear la Orden
    const orderRes = await orderService.createOrder(product.value.id, product.value.base_price);
    const orderId = orderRes.data.id;
    
    // 3. Generar Link de Stripe
    const successUrl = `${window.location.origin}/dashboard?payment=success`;
    const cancelUrl = `${window.location.origin}/checkout/${product.value.id}?payment=cancel`;
    
    const stripeRes = await orderService.createStripeCheckout(orderId, successUrl, cancelUrl);
    
    // 4. Redirigir a Stripe
    window.location.href = stripeRes.data.url;
  } catch (error) {
    console.error(error);
    toast.error('No pudimos procesar tu solicitud de pago. Intenta más tarde.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tailwind maneja los estilos */
</style>
