<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 animate-fade-in">
    <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12">
      
      <!-- Left: Order Summary & Info -->
      <div class="lg:col-span-7 space-y-8">
        <div class="bg-white rounded-[2.5rem] p-10 shadow-xl shadow-slate-200/40 border border-slate-100">
          <h2 class="text-3xl font-black text-slate-900 mb-8 tracking-tight">Resumen de tu Compra</h2>
          
          <div v-if="product" class="space-y-8">
            <!-- Main Product -->
            <div class="flex gap-6 p-5 rounded-3xl bg-slate-50/80 border border-slate-100 relative overflow-hidden group hover:border-primary/20 transition-all duration-300">
              <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-primary/10 to-transparent rounded-bl-full pointer-events-none"></div>
              <div class="w-24 h-24 bg-white rounded-2xl shadow-md flex items-center justify-center text-4xl border border-slate-50 transform group-hover:scale-105 transition-transform duration-300">
                💎
              </div>
              <div class="flex-1">
                <span class="inline-block bg-primary/10 text-primary px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider mb-2">Diseño Base</span>
                <h3 class="text-xl font-bold text-slate-800 leading-snug">{{ product.name }}</h3>
                <p class="text-sm text-slate-500 mt-1 line-clamp-2">{{ product.description || 'Diseño premium interactivo.' }}</p>
                <div class="mt-3 font-black text-slate-900 text-lg">${{ product.base_price }} MXN</div>
              </div>
            </div>

            <!-- Selected Addons / Services -->
            <div v-if="selectedAddons.length > 0" class="space-y-4 pt-6 border-t border-slate-100">
              <h4 class="text-xs font-black text-slate-400 uppercase tracking-widest">Servicios adicionales seleccionados:</h4>
              <div class="space-y-3">
                <div v-for="addon in selectedAddons" :key="addon.id" class="flex justify-between items-center p-4 rounded-2xl bg-indigo-50/40 border border-indigo-100/30 hover:border-indigo-100/70 transition-colors">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-lg border border-slate-100/50">
                      ✨
                    </div>
                    <div>
                      <h5 class="text-sm font-bold text-slate-800">{{ addon.name }}</h5>
                      <p class="text-xs text-slate-400 mt-0.5">{{ addon.description || 'Servicio adicional optimizado' }}</p>
                    </div>
                  </div>
                  <span class="text-sm font-black text-slate-900">${{ addon.base_price }} MXN</span>
                </div>
              </div>
            </div>

            <!-- Features Breakdown -->
            <div class="space-y-4 pt-6 border-t border-slate-100">
              <h4 class="text-xs font-black text-slate-400 uppercase tracking-widest">Tu experiencia incluye:</h4>
              <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <li v-for="item in ['Soporte VIP 24/7', 'Hosting ilimitado', 'RSVP en tiempo real', 'Panel de administración']" :key="item" class="flex items-center gap-3 text-slate-600 text-sm font-medium">
                  <span class="w-5 h-5 rounded-full bg-success/15 flex items-center justify-center">
                    <svg class="h-3.5 w-3.5 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3.5" d="M5 13l4 4L19 7" />
                    </svg>
                  </span>
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Shipping Address Form -->
        <div v-if="hasPhysicalProducts" class="bg-white rounded-[2.5rem] p-10 shadow-xl shadow-slate-200/40 border border-slate-100 space-y-6">
          <div class="flex items-center gap-4 border-b border-slate-50 pb-4">
            <span class="text-3xl">🚚</span>
            <div>
              <h2 class="text-2xl font-bold text-slate-800 leading-snug">Dirección de Envío</h2>
              <p class="text-xs text-slate-500 mt-1">Requerido para la entrega de tus productos físicos.</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Recipient Name -->
            <div class="md:col-span-2 flex flex-col gap-2">
              <label for="recipient_name" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Nombre del Destinatario <span class="text-red-500">*</span>
              </label>
              <input 
                id="recipient_name"
                v-model="shippingAddress.recipient_name"
                type="text" 
                placeholder="Ej. Juan Pérez López"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>

            <!-- Address Line 1 -->
            <div class="md:col-span-2 flex flex-col gap-2">
              <label for="address_line1" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Calle y Número <span class="text-red-500">*</span>
              </label>
              <input 
                id="address_line1"
                v-model="shippingAddress.address_line1"
                type="text" 
                placeholder="Ej. Av. Reforma 123 Int 4B"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>

            <!-- Address Line 2 -->
            <div class="md:col-span-2 flex flex-col gap-2">
              <label for="address_line2" class="text-xs font-black text-slate-500 uppercase tracking-widest flex justify-between">
                <span>Colonia / Referencias <span class="text-slate-400 font-medium font-sans lowercase">(opcional)</span></span>
              </label>
              <input 
                id="address_line2"
                v-model="shippingAddress.address_line2"
                type="text" 
                placeholder="Ej. Col. Juárez, portón negro"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
              />
            </div>

            <!-- City -->
            <div class="flex flex-col gap-2">
              <label for="city" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Ciudad / Municipio <span class="text-red-500">*</span>
              </label>
              <input 
                id="city"
                v-model="shippingAddress.city"
                type="text" 
                placeholder="Ej. Monterrey"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>

            <!-- State -->
            <div class="flex flex-col gap-2">
              <label for="state" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Estado <span class="text-red-500">*</span>
              </label>
              <input 
                id="state"
                v-model="shippingAddress.state"
                type="text" 
                placeholder="Ej. Nuevo León"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>

            <!-- Postal Code -->
            <div class="flex flex-col gap-2">
              <label for="postal_code" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Código Postal <span class="text-red-500">*</span>
              </label>
              <input 
                id="postal_code"
                v-model="shippingAddress.postal_code"
                type="text" 
                placeholder="Ej. 64000"
                maxlength="5"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>

            <!-- Phone -->
            <div class="flex flex-col gap-2">
              <label for="phone" class="text-xs font-black text-slate-500 uppercase tracking-widest">
                Teléfono de Contacto <span class="text-red-500">*</span>
              </label>
              <input 
                id="phone"
                v-model="shippingAddress.phone"
                type="tel" 
                placeholder="Ej. 8112345678"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 transition-all outline-none text-slate-700 text-sm font-semibold"
                required
              />
            </div>
          </div>
        </div>

        <div class="flex items-center gap-6 p-6 rounded-[2rem] bg-indigo-50/50 border border-indigo-100/50">
          <span class="text-3xl">🛡️</span>
          <div>
            <h4 class="font-bold text-indigo-900">Garantía de Satisfacción</h4>
            <p class="text-sm text-indigo-700/80 leading-relaxed">Si no estás conforme con el diseño tras 24h de uso, te devolvemos tu dinero sin preguntas.</p>
          </div>
        </div>
      </div>

      <!-- Right: Checkout Card -->
      <div class="lg:col-span-5 space-y-6">
        <div class="bg-white rounded-[2.5rem] p-10 shadow-2xl shadow-slate-200/50 border border-slate-100 sticky top-8">
          <div class="space-y-8">
            <h3 class="text-lg font-black text-slate-800 border-b border-slate-50 pb-4 uppercase tracking-wider text-xs">Resumen del Pago</h3>
            
            <div class="space-y-4" v-if="product">
              <!-- Itemized pricing breakdown -->
              <div class="flex justify-between text-sm text-slate-500 font-medium">
                <span>{{ product.name }}</span>
                <span>${{ product.base_price }} MXN</span>
              </div>
              <div v-if="selectedAddons.length > 0" class="flex justify-between text-sm text-slate-500 font-medium">
                <span>Servicios Adicionales ({{ selectedAddons.length }})</span>
                <span>${{ addonsTotal }} MXN</span>
              </div>
              
              <div class="flex justify-between items-center pt-6 border-t border-slate-100">
                <span class="text-slate-900 font-black uppercase tracking-widest text-xs">Total del pedido</span>
                <div class="text-right">
                  <span class="text-3xl font-black text-slate-900">${{ totalPrice }}</span>
                  <span class="text-slate-400 font-bold block text-[10px] tracking-wider mt-0.5">MXN</span>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <button 
                class="btn btn-primary btn-lg w-full h-16 rounded-2xl text-lg font-black shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300"
                @click="initiateStripePayment"
                :disabled="loading"
              >
                <span v-if="loading" class="loading loading-spinner"></span>
                {{ loading ? 'Preparando Pago...' : 'Confirmar y Pagar' }}
              </button>
              
              <div class="flex items-center justify-center gap-4 py-2 opacity-50 grayscale hover:opacity-75 transition-opacity">
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg" alt="Stripe" class="h-6" />
              </div>
            </div>

            <div class="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex gap-4">
              <span class="text-2xl">📧</span>
              <p class="text-[10px] text-slate-500 font-medium leading-relaxed">
                Al pagar, aceptas nuestros términos de servicio. Recibirás tu recibo fiscal y acceso instantáneo al editor vía correo electrónico.
              </p>
            </div>
          </div>
        </div>

        <!-- Security Badges -->
        <div class="grid grid-cols-3 gap-4 text-center opacity-40">
          <div class="space-y-1">
            <div class="text-xl">SSL</div>
            <div class="text-[8px] font-black uppercase tracking-widest">Seguro</div>
          </div>
          <div class="space-y-1">
            <div class="text-xl">PCI</div>
            <div class="text-[8px] font-black uppercase tracking-widest">Cumplimiento</div>
          </div>
          <div class="space-y-1">
            <div class="text-xl">256</div>
            <div class="text-[8px] font-black uppercase tracking-widest">Bits AES</div>
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
import { useAuthStore } from '@/modules/auth/store/auth';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { orderService } from '@/modules/ecommerce/services/orderService';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const product = ref(null);
const selectedAddonIds = ref([]);
const selectedAddons = ref([]);
const loading = ref(false);

const shippingAddress = ref({
  recipient_name: '',
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  postal_code: '',
  phone: ''
});

const hasPhysicalProducts = computed(() => {
  if (product.value?.is_physical) return true;
  return selectedAddons.value.some(addon => addon.is_physical);
});

const addonsTotal = computed(() => {
  return selectedAddons.value.reduce((acc, addon) => acc + parseFloat(addon.base_price), 0);
});

const totalPrice = computed(() => {
  if (!product.value) return 0;
  return parseFloat(product.value.base_price) + addonsTotal.value;
});

onMounted(async () => {
  try {
    const productId = route.params.id;
    const response = await catalogService.fetchProducts();
    const allProducts = response.data;
    
    product.value = allProducts.find(p => p.id === parseInt(productId));
    
    if (!product.value) {
      toast.error('Producto no válido');
      router.push('/catalog');
      return;
    }
    
    // Recuperar add-ons guardados
    const addonsJson = localStorage.getItem('selected_addon_ids');
    if (addonsJson) {
      try {
        selectedAddonIds.value = JSON.parse(addonsJson);
        selectedAddons.value = allProducts.filter(p => selectedAddonIds.value.includes(p.id));
      } catch (e) {
        console.error('Error al parsear addons seleccionados', e);
      }
    }
  } catch (error) {
    toast.error('Error al cargar la orden');
  }
});

const initiateStripePayment = async () => {
  // 1. Verificación de Autenticación
  if (!authStore.isAuthenticated) {
    toast.info('Para continuar con la compra, por favor inicia sesión o regístrate.');
    // Guardamos la intención de compra y addons para retornar después
    localStorage.setItem('pending_checkout_id', product.value.id);
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }

  // 1.5. Validar Dirección de Envío si hay productos físicos
  if (hasPhysicalProducts.value) {
    const addr = shippingAddress.value;
    if (!addr.recipient_name.trim() || 
        !addr.address_line1.trim() || 
        !addr.city.trim() || 
        !addr.state.trim() || 
        !addr.postal_code.trim() || 
        !addr.phone.trim()) {
      toast.error('Por favor, completa todos los campos requeridos de la dirección de envío.');
      return;
    }
    
    if (!/^\d{5}$/.test(addr.postal_code.trim())) {
      toast.error('El código postal debe tener exactamente 5 dígitos numéricos.');
      return;
    }
    
    if (addr.phone.trim().replace(/\D/g, '').length < 10) {
      toast.error('El teléfono debe incluir al menos 10 dígitos.');
      return;
    }
  }

  loading.value = true;
  try {
    // 2. Recuperar ID de diseño si viene de un Sandbox
    const deploymentId = localStorage.getItem('pending_sandbox_id');
    
    // 3. Construir items de la orden para el backend multi-producto
    const items = [
      {
        product: product.value.id,
        quantity: 1,
        price_at_sale: product.value.base_price
      }
    ];
    
    selectedAddons.value.forEach(addon => {
      items.push({
        product: addon.id,
        quantity: 1,
        price_at_sale: addon.base_price
      });
    });
    
    // 4. Crear la Orden vinculada al diseño con dirección de envío si aplica
    const orderRes = await orderService.createOrder(
      items, 
      totalPrice.value,
      null,
      deploymentId,
      hasPhysicalProducts.value ? shippingAddress.value : null
    );
    const orderId = orderRes.data.id;
    
    // Limpiar el sandbox y addons pendientes una vez que ya se creó la orden
    if (deploymentId) localStorage.removeItem('pending_sandbox_id');
    localStorage.removeItem('selected_addon_ids');
    
    // 5. Generar Link de Stripe
    const successUrl = `${window.location.origin}/dashboard?payment=success`;
    const cancelUrl = `${window.location.origin}/checkout/${product.value.id}?payment=cancel`;
    
    const stripeRes = await orderService.createStripeCheckout(orderId, successUrl, cancelUrl);
    
    // 6. Redirigir a Stripe
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
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
