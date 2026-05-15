<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <div>
        <h3 class="text-2xl font-bold text-slate-800">Punto de Venta (POS)</h3>
        <p class="text-slate-500 text-sm mt-1">Registra ventas presenciales o remotas manualmente</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Lado Izquierdo: Catálogo y Selección -->
      <div class="card bg-base-100 shadow-xl border border-slate-100">
        <div class="card-body">
          <h4 class="card-title text-lg border-b border-slate-100 pb-2">Seleccionar Producto</h4>
          
          <div v-if="loadingCatalog" class="flex justify-center py-8">
            <span class="loading loading-spinner text-primary"></span>
          </div>

          <div v-else class="space-y-4 mt-4">
            <div 
              v-for="product in products" 
              :key="product.id"
              @click="selectedProduct = product"
              :class="['p-4 border rounded-xl cursor-pointer transition-all', selectedProduct?.id === product.id ? 'border-primary bg-primary/5 ring-2 ring-primary/20' : 'border-slate-200 hover:border-primary/50 hover:bg-slate-50']"
            >
              <div class="flex justify-between items-center">
                <div>
                  <h5 class="font-bold text-slate-800">{{ product.name }}</h5>
                  <span class="text-xs text-slate-500">{{ product.product_type }}</span>
                </div>
                <div class="text-lg font-black text-slate-800">
                  ${{ product.base_price }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lado Derecho: Checkout y Cliente -->
      <div class="space-y-6">
        
        <div class="card bg-base-100 shadow-xl border border-slate-100">
          <div class="card-body">
            <h4 class="card-title text-lg border-b border-slate-100 pb-2">Datos del Cliente</h4>
            
            <div class="form-control w-full mt-4">
              <label class="label"><span class="label-text font-medium">ID del Usuario (Destinatario)</span></label>
              <input v-model="customerId" type="number" placeholder="Ej. 1" class="input input-bordered w-full" />
              <label class="label"><span class="label-text-alt text-slate-500">Puedes buscar el ID en la pestaña de CRM.</span></label>
            </div>
          </div>
        </div>

        <div class="card bg-base-100 shadow-xl border border-slate-100">
          <div class="card-body">
            <h4 class="card-title text-lg border-b border-slate-100 pb-2">Resumen de Venta</h4>
            
            <div v-if="!selectedProduct" class="py-8 text-center text-slate-500">
              Selecciona un producto para continuar
            </div>
            
            <div v-else class="mt-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-slate-600">Producto:</span>
                <strong class="text-slate-800">{{ selectedProduct.name }}</strong>
              </div>
              <div class="flex justify-between items-center mb-4 border-b border-slate-100 pb-4">
                <span class="text-slate-600">Cliente ID:</span>
                <strong class="text-slate-800">{{ customerId || 'No asignado (Tú mismo)' }}</strong>
              </div>
              
              <div class="flex justify-between items-center mt-4">
                <span class="text-slate-600 font-medium text-lg">Total a cobrar:</span>
                <strong class="text-3xl font-black text-success">${{ selectedProduct.base_price }}</strong>
              </div>

              <div class="card-actions mt-8">
                <button 
                  class="btn btn-success w-full h-16 text-lg" 
                  @click="processSale" 
                  :disabled="loadingSale"
                >
                  <span v-if="loadingSale" class="loading loading-spinner"></span>
                  {{ loadingSale ? 'Procesando...' : '💳 Registrar Venta y Cobrar' }}
                </button>
              </div>
            </div>
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
import { orderService } from '@/modules/ecommerce/services/orderService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';

const toast = useToast();
const products = ref([]);
const selectedProduct = ref(null);
const customerId = ref('');
const loadingCatalog = ref(true);
const loadingSale = ref(false);

const loadCatalog = async () => {
  loadingCatalog.value = true;
  try {
    const res = await catalogService.fetchProducts();
    products.value = res.data;
  } catch (error) {
    toast.error('Error al cargar catálogo');
  } finally {
    loadingCatalog.value = false;
  }
};

const processSale = async () => {
  if (!selectedProduct.value) {
    return toast.warning('Selecciona un producto');
  }
  
  loadingSale.value = true;
  try {
    // Si customerId está vacío, orderService enviará userId = null (se autoasigna al vendedor)
    const targetUserId = customerId.value ? parseInt(customerId.value) : null;
    
    // Crear orden a nombre del cliente indicado
    const resOrder = await orderService.createOrder(selectedProduct.value.id, selectedProduct.value.base_price, targetUserId);
    
    // Crear deployment (diseño) a nombre del cliente indicado
    // Nota: El deploymentService actual NO soporta pasar userId. Habría que ajustarlo en el futuro.
    // Para la demo, el POS solo crea la orden. El deployment podría requerir ajustes extra en backend.
    
    toast.success(`Venta de ${selectedProduct.value.name} registrada exitosamente.`);
    selectedProduct.value = null;
    customerId.value = '';
    
  } catch (error) {
    toast.error('Error al procesar la venta. Verifica permisos y el ID del cliente.');
  } finally {
    loadingSale.value = false;
  }
};

onMounted(() => {
  loadCatalog();
});
</script>
