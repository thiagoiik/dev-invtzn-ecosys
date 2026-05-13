<template>
  <div class="catalog-container">
    <h2>Catálogo de Invitaciones y Servicios</h2>
    <p class="subtitle">Explora nuestras plantillas y productos disponibles para tu próximo evento.</p>

    <div v-if="loading" class="loading-state">
      <p>Cargando catálogo...</p>
    </div>
    
    <div v-else-if="products.length === 0" class="empty-state">
      <p>Aún no hay productos disponibles en el catálogo.</p>
    </div>

    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        
        <div class="product-badges">
          <span class="badge type-badge">{{ translateType(product.product_type) }}</span>
          <span v-if="product.has_template" class="badge template-badge">★ Diseño Interactivo</span>
        </div>

        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-description">{{ product.description || 'Sin descripción disponible.' }}</p>
        
        <div class="product-footer">
          <span class="product-price">${{ product.base_price }} MXN</span>
          <button class="btn-buy" @click="handleBuy(product)">Ver Detalles</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';

const router = useRouter();
const toast = useToast();
const products = ref([]);
const loading = ref(true);

const loadProducts = async () => {
  loading.value = true;
  try {
    const response = await catalogService.fetchProducts();
    // Filtramos solo los productos activos
    products.value = response.data.filter(p => p.is_active);
  } catch (error) {
    toast.error('Ocurrió un error al cargar el catálogo de productos.');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadProducts();
});

const translateType = (type) => {
  const types = {
    'DIGITAL': 'Digital',
    'PHYSICAL': 'Impreso',
    'SERVICE': 'Servicio'
  };
  return types[type] || type;
};

const handleBuy = (product) => {
  router.push({ name: 'product-detail', params: { id: product.id } });
};
</script>

<style scoped>
.catalog-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}
.subtitle {
  color: #666;
  margin-bottom: 2rem;
}
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}
.product-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #eee;
}
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}
.product-badges {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-weight: bold;
}
.type-badge {
  background: #e2e8f0;
  color: #475569;
}
.template-badge {
  background: #fef3c7;
  color: #d97706;
}
.product-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  color: #1e293b;
}
.product-description {
  color: #64748b;
  font-size: 0.9rem;
  flex-grow: 1;
  margin-bottom: 1.5rem;
}
.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}
.product-price {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
}
.btn-buy {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-buy:hover {
  background: #2563eb;
}
</style>
