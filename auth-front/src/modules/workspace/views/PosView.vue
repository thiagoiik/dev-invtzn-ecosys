<template>
  <div class="space-y-6">
    <!-- Header dinámico con tienda -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Terminal Punto de Venta (POS)</h2>
        <p class="text-slate-500">
          {{ assignedStore ? `Sucursal: ${assignedStore.name}` : 'Modo Venta a Distancia' }}
        </p>
      </div>
      <div class="flex gap-3">
        <button v-if="activeSession" class="btn btn-outline btn-error" @click="closeSession">
          Cerrar Turno
        </button>
        <div class="badge badge-primary p-4 font-bold uppercase">{{ vendorMode }}</div>
      </div>
    </div>

    <!-- Pantalla de Bloqueo: Apertura de Turno (Solo para Vendedores Físicos) -->
    <div v-if="vendorMode === 'PHYSICAL' && !activeSession" class="flex justify-center py-20">
      <div class="card w-96 bg-white shadow-xl border border-primary/20">
        <div class="card-body text-center">
          <div class="bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold">Apertura de Caja</h3>
          <p class="text-slate-500 text-sm mb-6">Ingresa el saldo inicial para comenzar a vender en esta sucursal.</p>
          <div class="form-control">
            <input v-model="openingBalance" type="number" placeholder="$0.00" class="input input-bordered text-center text-2xl font-bold" />
          </div>
          <button class="btn btn-primary btn-block mt-6" @click="startShift" :disabled="loadingSession">
            <span v-if="loadingSession" class="loading loading-spinner"></span>
            Abrir Turno
          </button>
        </div>
      </div>
    </div>

    <!-- Interfaz de Venta (Visible si hay sesión o si es remoto) -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Columna Izquierda: Búsqueda y Selección de Producto -->
      <div class="md:col-span-2 space-y-6">
        <!-- Buscador -->
        <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="🔍 Buscar por nombre o SKU..." 
            class="input input-bordered w-full font-medium" 
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="prod in filteredProducts" 
            :key="prod.id"
            class="card bg-white border border-slate-200 shadow-sm cursor-pointer transition-all hover:border-primary hover:shadow-md flex flex-col justify-between"
            @click="addToCart(prod)"
          >
            <div class="card-body p-6">
              <div class="flex justify-between items-start gap-2">
                <div>
                  <h3 class="font-bold text-slate-800">{{ prod.name }}</h3>
                  <span v-if="prod.sku" class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono font-bold mt-1 inline-block">SKU: {{ prod.sku }}</span>
                </div>
                <span class="text-primary font-black shrink-0">${{ parseFloat(prod.base_price).toFixed(2) }}</span>
              </div>
              <p class="text-sm text-slate-500 mt-2 line-clamp-2">{{ prod.description }}</p>
            </div>
          </div>
        </div>

        <div v-if="loadingProducts" class="flex justify-center py-10">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>

        <div v-if="!loadingProducts && filteredProducts.length === 0" class="text-center py-12 text-slate-400 font-medium">
          No se encontraron productos.
        </div>
      </div>

      <!-- Columna Derecha: Carrito, Cliente, Pago y Total -->
      <div class="space-y-6">
        <!-- Card de Carrito de Compras -->
        <div class="card bg-white shadow-md border border-slate-200">
          <div class="card-body p-6">
            <h3 class="text-lg font-bold text-slate-800 border-b pb-3 mb-4">Carrito de Compras</h3>
            
            <!-- Items de Carrito -->
            <div v-if="cart.length > 0" class="space-y-4 max-h-60 overflow-y-auto pr-1">
              <div v-for="item in cart" :key="item.product.id" class="flex items-center justify-between gap-2 pb-3 border-b border-slate-100 last:border-0 last:pb-0">
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-sm text-slate-800 truncate">{{ item.product.name }}</p>
                  <p class="text-xs text-slate-500">${{ parseFloat(item.price).toFixed(2) }} c/u</p>
                </div>
                <div class="flex items-center gap-2">
                  <button class="btn btn-xs btn-circle btn-outline btn-neutral" @click.stop="decrementQty(item)">-</button>
                  <span class="font-bold text-sm w-4 text-center">{{ item.quantity }}</span>
                  <button class="btn btn-xs btn-circle btn-outline btn-neutral" @click.stop="incrementQty(item)">+</button>
                  <button class="btn btn-xs btn-ghost btn-circle text-error ml-1" @click.stop="removeFromCart(item)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-6 text-slate-400 text-sm italic">
              El carrito está vacío.
            </div>
          </div>
        </div>

        <!-- Card de Checkout / Cliente / Pago -->
        <div class="card bg-white shadow-xl border border-slate-200 overflow-hidden">
          <!-- Panel de Comisiones Rápido -->
          <div class="bg-slate-900 p-4 text-white flex justify-between items-center">
            <span class="text-xs font-bold uppercase opacity-60">Mis Comisiones</span>
            <span class="font-black text-green-400">${{ totalCommissions.toFixed(2) }}</span>
          </div>
          
          <div class="card-body p-6">
            <h3 class="text-lg font-bold text-slate-800 border-b pb-4 mb-4">Finalizar Venta</h3>
            
            <!-- Buscador de Cliente -->
            <div class="form-control w-full mb-6">
              <label class="label">
                <span class="label-text font-bold">ID del Cliente (api-auth)</span>
              </label>
              <div class="join w-full">
                <input 
                  v-model="customerSearchId" 
                  type="number" 
                  placeholder="Ej: 14" 
                  class="input input-bordered join-item w-full" 
                />
                <button 
                  class="btn btn-primary join-item" 
                  @click="findCustomer" 
                  :disabled="searching"
                >
                  <span v-if="searching" class="loading loading-spinner loading-xs"></span>
                  Buscar
                </button>
              </div>
              <div v-if="customer" class="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
                <div class="bg-green-500 text-white rounded-full p-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-bold text-green-800">{{ customer.full_name || 'Sin Nombre' }}</p>
                  <p class="text-xs text-green-600">ID #{{ customer.remote_auth_id }} - {{ customer.custom_role }}</p>
                </div>
              </div>
            </div>

            <!-- Método de Pago -->
            <div class="form-control w-full mb-4">
              <label class="label">
                <span class="label-text font-bold text-slate-700">Método de Pago</span>
              </label>
              <select v-model="paymentMethod" class="select select-bordered w-full font-semibold">
                <option v-if="vendorMode !== 'REMOTE'" value="CASH">💵 Efectivo (Cierre Inmediato)</option>
                <option v-if="vendorMode !== 'REMOTE'" value="CARD">💳 Tarjeta (Terminal Física)</option>
                <option value="BANK_TRANSFER">📲 Transferencia Bancaria (Referenciada)</option>
                <option value="OXXO">🏪 OXXO Referenciado</option>
              </select>
            </div>

            <!-- Descuento Directo (Solo ADMIN o FRANCHISEE) -->
            <div v-if="userRole === 'ADMIN' || userRole === 'FRANCHISEE'" class="form-control w-full mb-6">
              <label class="label">
                <span class="label-text font-bold text-slate-700">Descuento Directo ($)</span>
              </label>
              <input 
                v-model.number="discountAmount" 
                type="number" 
                min="0" 
                :max="subtotalAmount"
                placeholder="0.00" 
                class="input input-bordered w-full font-semibold" 
              />
            </div>

            <!-- Resumen de Costos -->
            <div class="space-y-3 mb-8">
              <div class="flex justify-between text-slate-600 text-sm">
                <span>Subtotal:</span>
                <span class="font-bold text-slate-800">${{ subtotalAmount.toFixed(2) }}</span>
              </div>
              <div v-if="discountAmount > 0" class="flex justify-between text-error text-sm">
                <span>Descuento:</span>
                <span class="font-bold">-${{ discountAmount.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-slate-600 text-sm">
                <span>Impuestos:</span>
                <span class="font-bold text-slate-800">${{ taxAmount.toFixed(2) }}</span>
              </div>
              <div class="divider my-0"></div>
              <div class="flex justify-between items-center text-xl">
                <span class="font-bold text-slate-800">Total:</span>
                <span class="font-black text-primary">${{ totalAmount.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Botón Acción -->
            <button 
              class="btn btn-primary btn-block h-16 text-lg" 
              :disabled="cart.length === 0 || !customer || processing"
              @click="processSale"
            >
              <span v-if="processing" class="loading loading-spinner"></span>
              Registrar Venta Directa
            </button>
            <p v-if="!customer" class="text-xs text-center text-slate-400 mt-4 italic">Debes buscar y validar un cliente primero.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE CIERRE DE CAJA (ARQUEO) -->
    <div v-if="showCloseModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-96 bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <h3 class="text-xl font-bold text-slate-800">Cierre de Caja y Arqueo</h3>
          <p class="text-slate-500 text-sm mb-4">Por favor cuenta el dinero en efectivo de la caja física e ingrésalo a continuación.</p>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text font-bold">Efectivo Contado Real</span>
            </label>
            <input v-model="closingBalanceInput" type="number" placeholder="$0.00" class="input input-bordered text-center text-2xl font-bold" />
          </div>

          <div class="flex gap-3 mt-6">
            <button class="btn btn-outline flex-1" @click="showCloseModal = false">Cancelar</button>
            <button class="btn btn-error flex-1" @click="confirmCloseSession" :disabled="closingSession">
              <span v-if="closingSession" class="loading loading-spinner"></span>
              Cerrar Turno
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE RESUMEN DE CIERRE -->
    <div v-if="showSummaryModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-[450px] bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <div class="text-center mb-4">
            <div class="bg-red-100 text-red-600 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-800">Turno Cerrado Correctamente</h3>
            <p class="text-xs text-slate-400">ID de Sesión: #{{ closeResult?.session_id }}</p>
          </div>

          <div class="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-100 text-sm">
            <div class="flex justify-between">
              <span class="text-slate-500">Saldo Inicial:</span>
              <span class="font-bold text-slate-700">${{ parseFloat(closeResult?.opening_balance).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Ventas en el Turno:</span>
              <span class="font-bold text-slate-700">${{ parseFloat(closeResult?.total_sales_amount).toFixed(2) }}</span>
            </div>
            <div class="divider my-0"></div>
            <div class="flex justify-between font-bold text-slate-800">
              <span class="text-slate-500">Esperado en Caja:</span>
              <span>${{ parseFloat(closeResult?.expected_closing_balance).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between font-bold text-slate-800">
              <span class="text-slate-500">Reportado Real:</span>
              <span>${{ parseFloat(closeResult?.closing_balance).toFixed(2) }}</span>
            </div>
            <div class="divider my-0"></div>
            <div class="flex justify-between items-center">
              <span class="text-slate-500 font-bold">Diferencia / Arqueo:</span>
              <span class="font-black p-2 rounded-lg text-xs" :class="closeResult?.difference >= 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                {{ closeResult?.difference >= 0 ? '+' : '' }}${{ parseFloat(closeResult?.difference).toFixed(2) }}
              </span>
            </div>
          </div>

          <button class="btn btn-primary btn-block mt-6" @click="closeSummaryModal">Entendido</button>
        </div>
      </div>
    </div>

    <!-- MODAL DE PAGO WHATSAPP REMOTO -->
    <div v-if="showWhatsappModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-[450px] bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="text-green-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.724-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.725 1.45 5.515.003 10.003-4.484 10.006-9.997.002-2.67-1.037-5.18-2.927-7.072C16.565 1.642 14.062.603 11.39.601 5.87.601 1.38 5.087 1.378 10.601c-.001 1.705.474 3.327 1.377 4.728l-.994 3.63 3.731-.978-.172-.25c.003.001.003.001.002 0z"/>
              </svg>
            </span>
            {{ paymentMethod === 'OXXO' ? 'Referencia OXXO Generada' : 'Venta Registrada Exitosamente' }}
          </h3>
          <p class="text-slate-500 text-sm mb-4">Copia el siguiente mensaje y compártelo con el cliente por WhatsApp para completar el pago remoto:</p>
          
          <div class="relative bg-slate-900 text-slate-300 p-4 rounded-xl text-sm font-mono whitespace-pre-wrap border border-slate-800 max-h-48 overflow-y-auto">
            {{ whatsappMessage }}
          </div>

          <div class="flex gap-3 mt-6">
            <button class="btn btn-outline flex-1" @click="showWhatsappModal = false">Cerrar</button>
            <button class="btn btn-success text-white flex-1 flex items-center gap-2" @click="copyWhatsappMessage">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
              </svg>
              Copiar Mensaje
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { crmService } from '@/modules/workspace/services/crmService';
import { orderService } from '@/modules/ecommerce/services/orderService';
import { profileService } from '@/modules/dashboard/services/profileService';

const toast = useToast();

const products = ref([]);
const loadingProducts = ref(true);

const searchQuery = ref('');
const cart = ref([]);

const customerSearchId = ref('');
const customer = ref(null);
const searching = ref(false);

const processing = ref(false);

// Perfil y Tienda
const vendorMode = ref('REMOTE');
const assignedStore = ref(null);
const activeSession = ref(null);
const openingBalance = ref(0);
const loadingSession = ref(false);
const userRole = ref('');

// Comisiones
const totalCommissions = ref(0);

// Descuentos y totales
const discountAmount = ref(0);

// Control de Modales
const showCloseModal = ref(false);
const showSummaryModal = ref(false);
const showWhatsappModal = ref(false);

const closingBalanceInput = ref(0);
const closingSession = ref(false);
const closeResult = ref(null);
const whatsappMessage = ref('');
const paymentMethod = ref('CASH');

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value;
  const q = searchQuery.value.toLowerCase();
  return products.value.filter(p => 
    p.name.toLowerCase().includes(q) || 
    (p.sku && p.sku.toLowerCase().includes(q))
  );
});

const subtotalAmount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0);
});

const taxAmount = computed(() => {
  return cart.value.reduce((sum, item) => {
    const rate = parseFloat(item.product.tax_rate) || 0;
    return sum + (item.price * item.quantity) * rate;
  }, 0);
});

const totalAmount = computed(() => {
  const tot = subtotalAmount.value - discountAmount.value + taxAmount.value;
  return tot > 0 ? tot : 0;
});

// Watchers para validar limites de descuento
watch(subtotalAmount, (newSubtotal) => {
  if (discountAmount.value > newSubtotal) {
    discountAmount.value = newSubtotal;
  }
});

watch(discountAmount, (newDiscount) => {
  if (newDiscount < 0) {
    discountAmount.value = 0;
  } else if (newDiscount > subtotalAmount.value) {
    discountAmount.value = subtotalAmount.value;
  }
});

const addToCart = (product) => {
  const existing = cart.value.find(item => item.product.id === product.id);
  if (existing) {
    existing.quantity++;
  } else {
    cart.value.push({
      product,
      quantity: 1,
      price: parseFloat(product.base_price)
    });
  }
  toast.success(`Agregado al carrito: ${product.name}`);
};

const incrementQty = (item) => {
  item.quantity++;
};

const decrementQty = (item) => {
  if (item.quantity > 1) {
    item.quantity--;
  } else {
    removeFromCart(item);
  }
};

const removeFromCart = (item) => {
  cart.value = cart.value.filter(i => i.product.id !== item.product.id);
  toast.info(`Quitado del carrito: ${item.product.name}`);
};

const initProfileData = async () => {
  try {
    const resProfile = await profileService.fetchMyProfile();
    vendorMode.value = resProfile.data.vendor_mode;
    userRole.value = resProfile.data.custom_role;
    
    // Configurar método de pago inicial por modo del vendedor
    paymentMethod.value = resProfile.data.vendor_mode === 'PHYSICAL' ? 'CASH' : 'BANK_TRANSFER';
    
    // Si tiene tienda asignada, cargar sus datos
    if (resProfile.data.assigned_store) {
      const storesRes = await crmService.fetchAllStores();
      assignedStore.value = storesRes.data.find(s => s.id === resProfile.data.assigned_store);
    }

    // Cargar comisiones
    const commRes = await crmService.fetchMyCommissions();
    totalCommissions.value = commRes.data.reduce((acc, curr) => acc + parseFloat(curr.amount), 0);

    // Cargar sesión activa
    const sessionRes = await crmService.fetchMySessions();
    activeSession.value = sessionRes.data.find(s => s.is_open);

  } catch (e) {
    console.error(e);
  }
};

const startShift = async () => {
  if (!assignedStore.value) {
    toast.error('No tienes una sucursal asignada. Contacta al Admin.');
    return;
  }
  loadingSession.value = true;
  try {
    const res = await crmService.openCashSession(openingBalance.value, assignedStore.value.id);
    activeSession.value = res.data;
    toast.success('Turno abierto correctamente. ¡Buena venta!');
  } catch (e) {
    toast.error('Error al abrir turno.');
  } finally {
    loadingSession.value = false;
  }
};

const closeSession = () => {
  closingBalanceInput.value = 0;
  showCloseModal.value = true;
};

const confirmCloseSession = async () => {
  if (!activeSession.value) return;
  closingSession.value = true;
  try {
    const res = await crmService.closeCashSession(activeSession.value.id, closingBalanceInput.value);
    closeResult.value = res.data;
    showCloseModal.value = false;
    showSummaryModal.value = true;
    toast.success('Turno cerrado con éxito.');
  } catch (error) {
    toast.error('Error al cerrar el turno.');
  } finally {
    closingSession.value = false;
  }
};

const closeSummaryModal = () => {
  showSummaryModal.value = false;
  activeSession.value = null;
  initProfileData();
};

const copyWhatsappMessage = async () => {
  try {
    await navigator.clipboard.writeText(whatsappMessage.value);
    toast.success('¡Mensaje copiado al portapapeles!');
    showWhatsappModal.value = false;
  } catch (err) {
    toast.error('No se pudo copiar el mensaje automáticamente.');
  }
};

const fetchProducts = async () => {
  loadingProducts.value = true;
  try {
    const res = await catalogService.fetchProducts();
    products.value = res.data;
  } catch (e) {
    toast.error('Error al cargar productos');
  } finally {
    loadingProducts.value = false;
  }
};

const findCustomer = async () => {
  if (!customerSearchId.value) return;
  searching.value = true;
  customer.value = null;
  try {
    const res = await crmService.searchProfile(customerSearchId.value);
    customer.value = res.data;
    toast.success('Cliente validado');
  } catch (e) {
    toast.error('Cliente no encontrado');
  } finally {
    searching.value = false;
  }
};

const processSale = async () => {
  if (cart.value.length === 0 || !customer.value) return;
  processing.value = true;
  try {
    // 1. Crear la orden en estado PENDING con múltiples ítems
    const payload = {
      user: customer.value.remote_auth_id,
      subtotal_amount: subtotalAmount.value.toFixed(2),
      discount_amount: discountAmount.value.toFixed(2),
      tax_amount: taxAmount.value.toFixed(2),
      total_amount: totalAmount.value.toFixed(2),
      status: 'PENDING',
      items: cart.value.map(item => ({
        product: item.product.id,
        quantity: item.quantity,
        price_at_sale: parseFloat(item.price).toFixed(2)
      }))
    };

    const orderRes = await orderService.createOrder(payload);
    const orderId = orderRes.data.id;

    // 2. Determinar flujo según el método de pago seleccionado
    if (paymentMethod.value === 'CASH' || paymentMethod.value === 'CARD') {
      // Completar cobro presencial de inmediato
      await orderService.completePosOrder(orderId, paymentMethod.value);
      toast.success(`Venta completada con éxito en ${paymentMethod.value === 'CASH' ? 'Efectivo' : 'Tarjeta'}`);
    } else if (paymentMethod.value === 'OXXO') {
      // Generar mensaje OXXO referenciado
      const referenceNumber = `73812903${String(orderId).padStart(6, '0')}`;
      const clientName = customer.value.full_name || 'Cliente';
      
      const itemsList = cart.value.map(item => `• ${item.quantity}x ${item.product.name} ($${parseFloat(item.price).toFixed(2)} c/u)`).join('\n');
      const amount = totalAmount.value.toFixed(2);
      
      whatsappMessage.value = `¡Hola, ${clientName}! Se ha registrado tu orden:\n${itemsList}\n\nSubtotal: $${subtotalAmount.value.toFixed(2)}\nDescuento: -$${discountAmount.value.toFixed(2)}\nImpuestos: $${taxAmount.value.toFixed(2)}\nTotal a pagar: $${amount} MXN\n\nPara completar tu pago referenciado de OXXO, acude a tu sucursal OXXO más cercana y proporciona el número de referencia:\n👉 ${referenceNumber}\n\nCompártenos el ticket de pago una vez realizado. ¡Muchas gracias!`;
      showWhatsappModal.value = true;
      toast.success('Orden registrada. En espera de pago por OXXO.');
    } else {
      // Transferencia bancaria estándar
      const clientName = customer.value.full_name || 'Cliente';
      const itemsList = cart.value.map(item => `• ${item.quantity}x ${item.product.name} ($${parseFloat(item.price).toFixed(2)} c/u)`).join('\n');
      const amount = totalAmount.value.toFixed(2);
      
      whatsappMessage.value = `¡Hola, ${clientName}! Se ha registrado tu orden:\n${itemsList}\n\nSubtotal: $${subtotalAmount.value.toFixed(2)}\nDescuento: -$${discountAmount.value.toFixed(2)}\nImpuestos: $${taxAmount.value.toFixed(2)}\nTotal a pagar: $${amount} MXN\n\nPor favor realiza tu transferencia a la CLABE: 012180000000000000 de ECOSYS y compártenos tu comprobante por este medio. ¡Muchas gracias!`;
      showWhatsappModal.value = true;
      toast.success('Orden registrada. En espera de transferencia.');
    }

    cart.value = [];
    discountAmount.value = 0;
    customer.value = null;
    customerSearchId.value = '';
    
    // Recargar comisiones y estado de caja
    initProfileData();
  } catch (e) {
    console.error(e);
    const errorMsg = e.response?.data?.error || 'Error al procesar la venta.';
    toast.error(errorMsg);
  } finally {
    processing.value = false;
  }
};

onMounted(() => {
  initProfileData();
  fetchProducts();
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.25s ease-out forwards;
}
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
