<template>
  <div class="flex justify-center py-12 px-4">
    <div class="card w-full max-w-lg bg-white shadow-2xl border border-slate-100">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold text-slate-800">Finalizar Compra</h2>
        <p class="text-slate-500 mb-6">Estás a un paso de obtener tu diseño.</p>

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
          <button class="btn btn-success w-full h-16 text-lg" @click="processPayment" :disabled="loading">
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Procesando Tarjeta...' : 'Pagar Ahora' }}
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
  loading.value = true;
  try {
    await orderService.createOrder(product.value.id, product.value.base_price);
    
    // Crear el borrador (sandbox) del diseño para el usuario
    await deploymentService.createSandbox(product.value.id);
    
    toast.success('¡Pago exitoso! Tu orden ha sido creada.');
    router.push('/dashboard'); // Redirigir al portal privado post-compra
  } catch (error) {
    if (error.response && error.response.status === 401) {
      toast.error('Debes iniciar sesión para comprar.');
      router.push('/login');
    } else {
      toast.error('Error al procesar el pago.');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tailwind maneja los estilos */
</style>
