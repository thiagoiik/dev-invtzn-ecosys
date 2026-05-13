<template>
  <div class="product-detail">
    <div class="header-banner">
      <h2>{{ product?.name || 'Cargando producto...' }}</h2>
      <p v-if="product?.has_template" class="badge template-badge">★ Diseño Interactivo Incluido</p>
    </div>

    <div class="detail-grid">
      <div class="image-placeholder">
        <span>Previsualización del Diseño</span>
      </div>

      <div class="info-card">
        <h3>Detalles</h3>
        <p class="desc">{{ product?.description || 'Sin descripción.' }}</p>
        <p class="price">Precio: ${{ product?.base_price }} MXN</p>
        
        <div class="actions">
          <button v-if="product?.has_template" class="btn btn-secondary" @click="trySandbox" :disabled="loadingSandbox">
            {{ loadingSandbox ? 'Preparando...' : '🛠️ Probar Gratis' }}
          </button>
          
          <button class="btn btn-primary" @click="buyNow">
            💳 Comprar Ahora
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
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const product = ref(null);
const loadingSandbox = ref(false);

onMounted(async () => {
  try {
    const productId = route.params.id;
    // Por ahora, traemos todo el catálogo y filtramos en frontend (lo ideal sería un GET /products/:id)
    const response = await catalogService.fetchProducts();
    product.value = response.data.find(p => p.id === parseInt(productId));
    
    if (!product.value) {
      toast.error('Producto no encontrado');
      router.push('/catalog');
    }
  } catch (error) {
    toast.error('Error al cargar detalles');
  }
});

const trySandbox = async () => {
  loadingSandbox.value = true;
  try {
    await deploymentService.createSandbox(product.value.id);
    toast.success('¡Tu entorno de prueba está listo!');
    // Aquí el roadmap dice redirigir a DraftSuccess, por ahora mandaremos al dashboard
    router.push('/dashboard'); 
  } catch (error) {
    toast.error('Necesitas iniciar sesión para probar la invitación.');
    router.push('/login');
  } finally {
    loadingSandbox.value = false;
  }
};

const buyNow = () => {
  router.push({ name: 'checkout', params: { id: product.value.id } });
};
</script>

<style scoped>
.product-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}
.header-banner {
  text-align: center;
  margin-bottom: 2rem;
}
.template-badge {
  background: #fef3c7;
  color: #d97706;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-weight: bold;
  display: inline-block;
  margin-top: 1rem;
}
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}
.image-placeholder {
  background: #f1f5f9;
  border-radius: 12px;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 1.2rem;
  border: 2px dashed #cbd5e1;
}
.info-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.desc {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}
.price {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 2rem;
}
.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.btn {
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-size: 1.1rem;
}
.btn-primary {
  background: #3b82f6;
  color: white;
}
.btn-primary:hover { background: #2563eb; }
.btn-secondary {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #cbd5e1;
}
.btn-secondary:hover { background: #f1f5f9; }
</style>
