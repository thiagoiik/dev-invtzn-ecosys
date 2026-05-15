<template>
  <div class="space-y-6">
    <!-- Header dinámico con tienda -->
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
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
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Columna Izquierda: Selección de Producto -->
      <div class="lg:col-span-2 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="prod in products" 
            :key="prod.id"
            class="card bg-white border cursor-pointer transition-all hover:border-primary"
            :class="selectedProduct?.id === prod.id ? 'border-primary ring-2 ring-primary/20 shadow-lg' : 'border-slate-200 shadow-sm'"
            @click="selectedProduct = prod"
          >
            <div class="card-body p-6">
              <div class="flex justify-between items-start">
                <h3 class="font-bold text-slate-800">{{ prod.name }}</h3>
                <span class="text-primary font-black">${{ prod.base_price }}</span>
              </div>
              <p class="text-sm text-slate-500 mt-2 line-clamp-2">{{ prod.description }}</p>
            </div>
          </div>
        </div>

        <div v-if="loadingProducts" class="flex justify-center py-10">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>
      </div>

      <!-- Columna Derecha: Resumen y Cliente -->
      <div class="space-y-6">
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

            <!-- Resumen -->
            <div class="space-y-4 mb-8">
              <div class="flex justify-between text-slate-600">
                <span>Producto:</span>
                <span class="font-bold text-slate-800">{{ selectedProduct?.name || 'Ninguno' }}</span>
              </div>
              <div class="divider my-0"></div>
              <div class="flex justify-between items-center text-xl">
                <span class="font-bold text-slate-800">Total:</span>
                <span class="font-black text-primary">${{ selectedProduct?.base_price || '0.00' }}</span>
              </div>
            </div>

            <!-- Botón Acción -->
            <button 
              class="btn btn-primary btn-block h-16 text-lg" 
              :disabled="!selectedProduct || !customer || processing"
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { crmService } from '@/modules/workspace/services/crmService';
import { orderService } from '@/modules/ecommerce/services/orderService';
import { profileService } from '@/modules/dashboard/services/profileService';

const toast = useToast();

const products = ref([]);
const loadingProducts = ref(true);
const selectedProduct = ref(null);

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

// Comisiones
const totalCommissions = ref(0);

const initProfileData = async () => {
  try {
    const resProfile = await profileService.fetchMyProfile();
    vendorMode.value = resProfile.data.vendor_mode;
    
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
  if (!selectedProduct.value || !customer.value) return;
  processing.value = true;
  try {
    await orderService.createOrder(
      selectedProduct.value.id, 
      selectedProduct.value.base_price,
      customer.value.remote_auth_id
    );
    toast.success('Venta registrada con éxito');
    selectedProduct.value = null;
    customer.value = null;
    customerSearchId.value = '';
    // Recargar comisiones
    initProfileData();
  } catch (e) {
    toast.error('Error al procesar la venta.');
  } finally {
    processing.value = false;
  }
};

onMounted(() => {
  initProfileData();
  fetchProducts();
});
</script>
