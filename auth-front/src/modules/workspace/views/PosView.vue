<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Terminal Punto de Venta (POS)</h2>
        <p class="text-slate-500">Registra ventas manuales y asigna diseños a clientes.</p>
      </div>
      <div class="badge badge-primary p-4 font-bold">MODO VENDEDOR</div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
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
        <div class="card bg-white shadow-xl border border-slate-200">
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
                <span>Producto seleccionado:</span>
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

const toast = useToast();

const products = ref([]);
const loadingProducts = ref(true);
const selectedProduct = ref(null);

const customerSearchId = ref('');
const customer = ref(null);
const searching = ref(false);

const processing = ref(false);

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
    toast.success('Cliente validado correctamente');
  } catch (e) {
    toast.error('No se encontró el cliente o no tienes permisos.');
  } finally {
    searching.value = false;
  }
};

const processSale = async () => {
  if (!selectedProduct.value || !customer.value) return;
  
  processing.value = true;
  try {
    // Registramos la orden en el backend asignándola al cliente encontrado
    await orderService.createOrder(
      selectedProduct.value.id, 
      selectedProduct.value.base_price,
      customer.value.remote_auth_id
    );
    
    toast.success('¡Venta registrada con éxito!');
    
    // Limpiar formulario
    selectedProduct.value = null;
    customer.value = null;
    customerSearchId.value = '';
    
  } catch (e) {
    toast.error('Error al procesar la venta manual.');
  } finally {
    processing.value = false;
  }
};

onMounted(() => {
  fetchProducts();
});
</script>
