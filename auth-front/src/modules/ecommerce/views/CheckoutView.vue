<template>
  <div class="flex justify-center py-12 px-4">
    <div class="card w-full max-w-lg bg-white shadow-2xl border border-slate-100">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold text-slate-800">Finalizar Compra</h2>
        <p class="text-slate-500 mb-6">Estás a un paso de obtener tu diseño de alta calidad.</p>

        <div v-if="product" class="bg-slate-50 p-6 rounded-xl border border-slate-200 mb-6">
          <div class="flex justify-between items-center mb-4">
            <span class="text-slate-600 font-medium">Producto:</span>
            <strong class="text-slate-800 text-right">{{ product.name }}</strong>
          </div>
          <div class="divider my-2"></div>
          <div class="flex justify-between items-center mt-4">
            <span class="text-slate-600 font-medium">Total a Pagar:</span>
            <strong class="text-2xl text-slate-800">${{ product.base_price }} <span class="text-sm font-normal text-slate-500">MXN</span></strong>
          </div>
        </div>

        <div class="mt-4 text-center">
          <p class="text-xs text-slate-400 mb-3 uppercase tracking-widest font-bold">🔒 Pago Seguro Encriptado</p>
          <!-- Abrimos el modal en lugar de procesar directo -->
          <button class="btn btn-success w-full h-16 text-lg" @click="showModal = true" :disabled="loading">
            Pagar Ahora
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Simulación de Pago -->
    <div :class="['modal', { 'modal-open': showModal }]">
      <div class="modal-box">
        <h3 class="font-bold text-xl mb-4">💳 Simulación de Pago</h3>
        <p class="text-slate-500 mb-6 text-sm">Ingresa datos de prueba para completar la compra de tu invitación.</p>
        
        <div class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Nombre en la tarjeta</span></label>
            <input type="text" placeholder="Ej: Juan Pérez" class="input input-bordered w-full" v-model="cardName" />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Número de Tarjeta</span></label>
            <input type="text" placeholder="XXXX XXXX XXXX XXXX" class="input input-bordered w-full" v-model="cardNumber" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-bold">Expira (MM/YY)</span></label>
              <input type="text" placeholder="12/28" class="input input-bordered w-full" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-bold">CVV</span></label>
              <input type="text" placeholder="123" class="input input-bordered w-full" />
            </div>
          </div>
        </div>

        <div class="modal-action">
          <button class="btn btn-ghost" @click="showModal = false" :disabled="loading">Cancelar</button>
          <button class="btn btn-primary px-8" @click="processPayment" :disabled="loading">
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Validando...' : 'Confirmar y Pagar' }}
          </button>
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
import { orderService } from '@/modules/ecommerce/services/orderService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const product = ref(null);
const loading = ref(false);
const showModal = ref(false);

// Datos fake para el modal
const cardName = ref('');
const cardNumber = ref('');

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

const processPayment = async () => {
  if (!cardName.value || !cardNumber.value) {
    toast.warning('Por favor completa los campos de la tarjeta');
    return;
  }

  loading.value = true;
  try {
    // 1. Crear la Orden en el Backend
    await orderService.createOrder(product.value.id, product.value.base_price);
    
    // 2. Crear el despliegue (Sandbox)
    // Nota: En una fase más avanzada, esto podría activarse vía Señales en Django tras el pago.
    await deploymentService.createSandbox(product.value.id);
    
    toast.success('¡Compra finalizada con éxito!');
    showModal.value = false;
    
    // 3. Redirigir al Dashboard para que vea su nuevo diseño
    router.push('/dashboard');
  } catch (error) {
    if (error.response && error.response.status === 401) {
      toast.error('Tu sesión ha expirado. Por favor ingresa de nuevo.');
      router.push('/login');
    } else {
      console.error(error);
      toast.error('Hubo un problema al procesar tu orden. Intenta más tarde.');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tailwind maneja los estilos */
</style>
