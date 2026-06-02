<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 animate-fade-in">
    <div class="max-w-5xl mx-auto">
      <!-- Breadcrumbs -->
      <nav class="flex mb-8 text-sm font-bold uppercase tracking-widest text-slate-400">
        <router-link to="/" class="hover:text-primary transition-colors">Inicio</router-link>
        <span class="mx-2">/</span>
        <router-link to="/catalog" class="hover:text-primary transition-colors">Catálogo</router-link>
        <span class="mx-2">/</span>
        <span class="text-slate-600">Checkout</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
      
      <!-- Left: Order Summary & Info -->
      <div class="lg:col-span-7 space-y-8">
        <div class="bg-white rounded-[2.5rem] p-10 shadow-xl shadow-slate-200/40 border border-slate-100">
          <h2 class="text-3xl font-black text-slate-900 mb-8 tracking-tight">Resumen de tu Compra</h2>
          
          <div v-if="product" class="space-y-8">
            <!-- Main Product -->
            <div class="flex flex-col sm:flex-row items-center gap-6 p-6 sm:p-5 rounded-3xl bg-slate-50/80 border border-slate-100 relative overflow-hidden group hover:border-primary/20 transition-all duration-300">
              <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-primary/10 to-transparent rounded-bl-full pointer-events-none"></div>
              <!-- Bezel smartphone mockup (exactly 9:16 aspect ratio scaled to 0.2 of a 360px viewport) -->
              <div 
                class="bg-slate-950 rounded-[1.25rem] shadow-lg flex items-center justify-center border-4 border-slate-900 transform group-hover:scale-105 transition-transform duration-300 overflow-hidden relative shrink-0 z-10"
                style="width: 80px; height: 136px;"
              >
                <!-- Dynamic CSS Preview -->
                <div 
                  v-if="product && product.has_template && product.template_config" 
                  class="absolute inset-0 overflow-hidden pointer-events-none"
                >
                  <div 
                    class="absolute top-0 left-0 origin-top-left"
                    style="width: 360px; height: 640px; transform: scale(0.2);"
                  >
                    <CoverBlock 
                      :config="getCoverConfig(product.template_config)"
                      :style="{ minHeight: '100%', height: '100%', ...getThemeVariables(product.template_config) }"
                    />
                  </div>
                </div>
                <!-- Fallback static image or diamond -->
                <template v-else-if="product">
                  <img 
                    v-if="product.thumbnail_url" 
                    :src="product.thumbnail_url" 
                    alt="Vista previa" 
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-4xl">💎</span>
                </template>
              </div>
              
              <!-- Product text information structured responsively -->
              <div class="flex-1 text-center sm:text-left w-full z-10">
                <h3 class="text-xl font-bold text-slate-800 leading-snug">{{ product.name }}</h3>
                <p class="text-sm text-slate-500 mt-2 line-clamp-2">{{ product.description || 'Diseño premium interactivo.' }}</p>
                
                <!-- Price and badge arranged cleanly at the bottom of the content area -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mt-4 pt-4 border-t border-slate-100/50">
                  <div class="font-black text-slate-900 text-lg">${{ product.base_price }} MXN</div>
                  <div>
                    <span class="inline-block bg-primary/10 text-primary px-3.5 py-1 rounded-full text-[9px] font-black uppercase tracking-widest shadow-sm">
                      Diseño Base
                    </span>
                  </div>
                </div>
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
          <div class="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-indigo-600 flex-shrink-0">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
          </div>
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
                <span>${{ addonsTotal.toFixed(2) }} MXN</span>
              </div>
              
              <!-- SECCIÓN DE CUPÓN -->
              <div class="pt-4 border-t border-slate-100">
                <div v-if="!appliedCoupon" class="flex gap-2">
                  <input 
                    v-model="couponCode" 
                    type="text" 
                    placeholder="Código de Descuento" 
                    class="input input-sm input-bordered w-full uppercase font-bold text-slate-700" 
                    :disabled="validatingCoupon"
                    @keyup.enter="validateCoupon"
                  />
                  <button 
                    class="btn btn-sm btn-neutral" 
                    @click="validateCoupon" 
                    :disabled="!couponCode || validatingCoupon"
                  >
                    <span v-if="validatingCoupon" class="loading loading-spinner loading-xs"></span>
                    Aplicar
                  </button>
                </div>
                <div v-if="couponError" class="text-xs text-error mt-1 font-semibold">{{ couponError }}</div>
                
                <div v-if="appliedCoupon" class="flex justify-between items-center bg-green-50 text-green-700 p-3 rounded-xl border border-green-200 mt-2">
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                    <span class="font-bold text-sm">{{ appliedCoupon.code }}</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="font-black text-sm">
                      - ${{ discountAmount.toFixed(2) }} MXN
                    </span>
                    <button @click="removeCoupon" class="text-xs text-green-600 hover:text-green-800 underline">Quitar</button>
                  </div>
                </div>
              </div>

              <div class="flex justify-between items-center pt-6 border-t border-slate-100">
                <span class="text-slate-900 font-black uppercase tracking-widest text-xs">Total del pedido</span>
                <div class="text-right">
                  <span class="text-3xl font-black text-slate-900">${{ totalPrice.toFixed(2) }}</span>
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

            <div class="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex gap-4 items-start">
              <svg class="w-5 h-5 text-slate-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/modules/auth/store/auth';
import CoverBlock from '@/modules/engine/components/CoverBlock.vue';
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

const couponCode = ref('');
const appliedCoupon = ref(null);
const validatingCoupon = ref(false);
const couponError = ref('');

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

const subtotalAmount = computed(() => {
  if (!product.value) return 0;
  return parseFloat(product.value.base_price) + addonsTotal.value;
});

const discountAmount = computed(() => {
  if (!appliedCoupon.value) return 0;
  let discount = 0;
  if (appliedCoupon.value.discount_fixed > 0) {
    discount = appliedCoupon.value.discount_fixed;
  } else if (appliedCoupon.value.discount_percentage > 0) {
    discount = subtotalAmount.value * (appliedCoupon.value.discount_percentage / 100);
  }
  return discount > subtotalAmount.value ? subtotalAmount.value : discount;
});

const totalPrice = computed(() => {
  return subtotalAmount.value - discountAmount.value;
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

const getCoverConfig = (templateConfig) => {
  if (!templateConfig) return {};
  if (Array.isArray(templateConfig.blocks)) {
    const coverBlock = templateConfig.blocks.find(b => b.type === 'CoverBlock');
    if (coverBlock) {
      return coverBlock.config || {};
    }
  }
  return templateConfig.cover || {};
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

const validateCoupon = async () => {
  couponError.value = '';
  if (!couponCode.value.trim()) return;
  
  validatingCoupon.value = true;
  try {
    const response = await catalogService.validateCoupon(couponCode.value);
    appliedCoupon.value = response.data;
    toast.success('¡Cupón aplicado correctamente!');
  } catch (error) {
    couponError.value = error.response?.data?.error || 'Cupón inválido o expirado.';
    appliedCoupon.value = null;
  } finally {
    validatingCoupon.value = false;
  }
};

const removeCoupon = () => {
  appliedCoupon.value = null;
  couponCode.value = '';
  couponError.value = '';
};

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

    const orderPayload = {
      subtotal_amount: subtotalAmount.value,
      total_amount: totalPrice.value,
      origin: 'ONLINE',
      items: items,
      customer_email: authStore.user?.email || null
    };

    if (appliedCoupon.value) {
      orderPayload.coupon_code = appliedCoupon.value.code;
    }

    if (deploymentId) {
      orderPayload.deployment = deploymentId;
    }
    
    if (hasPhysicalProducts.value && shippingAddress.value) {
      orderPayload.shipping_address = shippingAddress.value;
    }
    
    // 4. Crear la Orden vinculada al diseño con dirección de envío si aplica
    const orderRes = await orderService.createOrder(orderPayload);
    const orderId = orderRes.data.id;
    
    // Limpiar el sandbox y addons pendientes una vez que ya se creó la orden
    if (deploymentId) localStorage.removeItem('pending_sandbox_id');
    localStorage.removeItem('selected_addon_ids');
    
    // 5. Generar Link de Stripe
    const successUrl = deploymentId 
      ? `${window.location.origin}/studio/${deploymentId}?payment=success`
      : `${window.location.origin}/dashboard?payment=success`;
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
