<template>
  <div class="checkout-container">
    <div class="checkout-card">
      <h2>Finalizar Compra</h2>
      <p class="subtitle">Estás a un paso de obtener tu diseño.</p>

      <div class="order-summary" v-if="product">
        <div class="row">
          <span>Producto:</span>
          <strong>{{ product.name }}</strong>
        </div>
        <div class="row total">
          <span>Total a Pagar:</span>
          <strong>${{ product.base_price }} MXN</strong>
        </div>
      </div>

      <div class="payment-box">
        <p class="mock-text">Simulador de Pago Seguro 🔒</p>
        <button class="btn btn-pay" @click="processPayment" :disabled="loading">
          {{ loading ? 'Procesando Tarjeta...' : 'Pagar Ahora' }}
        </button>
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
.checkout-container {
  display: flex;
  justify-content: center;
  padding: 4rem 1rem;
}
.checkout-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}
.subtitle {
  color: #64748b;
  margin-bottom: 2rem;
}
.order-summary {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.row.total {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
  font-size: 1.25rem;
  margin-bottom: 0;
}
.payment-box {
  text-align: center;
}
.mock-text {
  color: #94a3b8;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.btn-pay {
  width: 100%;
  background: #10b981;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-pay:hover:not(:disabled) {
  background: #059669;
}
.btn-pay:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}
</style>
