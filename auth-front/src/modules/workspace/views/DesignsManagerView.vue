<template>
  <div class="designs-manager">
    <div class="header">
      <h3>Gestión de Diseños (Deployments)</h3>
      <button @click="loadDeployments" class="btn btn-refresh">🔄 Actualizar</button>
    </div>

    <div v-if="loading" class="loading">Cargando diseños globales...</div>
    
    <!-- Vista de Tabla (Escritorio / Tablet) -->
    <div v-else-if="!loading" class="hidden md:block overflow-x-auto">
      <table class="data-grid">
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Estado Pago</th>
            <th>Estado Visibilidad</th>
            <th>URL Pública</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dep in deployments" :key="dep.id">
            <td>#{{ dep.id }}</td>
            <td>
              <div class="font-bold">Usuario {{ dep.user }}</div>
              <div class="text-[10px] text-slate-400 uppercase">Prod #{{ dep.product }}</div>
            </td>
            <td>
              <span v-if="dep.is_paid" class="badge paid">✅ PAGADA</span>
              <span v-else class="badge trial">🧪 PRUEBA</span>
            </td>
            <td>
              <span :class="['badge', dep.status.toLowerCase()]">{{ dep.status }}</span>
            </td>
            <td>
              <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="link">/i/{{ dep.slug }}</a>
              <span v-else class="text-muted">Sin asignar</span>
            </td>
            <td class="actions-cell">
              <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-sm btn-outline" title="Previa">👁️</a>
              
              <router-link :to="'/builder/' + dep.id" class="btn btn-sm btn-primary" title="Editar">
                🛠️
              </router-link>
              
              <button v-if="!dep.is_paid" @click="onPay(dep)" class="btn btn-sm btn-success" title="Pagar">
                💰 Pagar
              </button>

              <button @click="onDelete(dep.id)" class="btn btn-sm btn-danger" title="Eliminar">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Vista Móvil (Tarjetas) -->
    <div v-else-if="!loading" class="grid grid-cols-1 gap-4 md:hidden">
      <div 
        v-for="dep in deployments" 
        :key="dep.id"
        class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col gap-4"
      >
        <!-- Fila superior: ID y Visibilidad -->
        <div class="flex items-center justify-between">
          <span class="font-black text-slate-800 text-sm">ID #{{ dep.id }}</span>
          <span :class="['badge font-bold text-[10px] uppercase tracking-wider', dep.status.toLowerCase()]">
            {{ dep.status }}
          </span>
        </div>

        <!-- Cuerpo del Diseño -->
        <div class="space-y-3">
          <div>
            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Cliente</div>
            <div class="font-bold text-slate-800 text-sm">Usuario {{ dep.user }}</div>
            <div class="text-[10px] text-slate-400">Prod #{{ dep.product }}</div>
          </div>
          
          <div>
            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Pago</div>
            <span v-if="dep.is_paid" class="badge paid text-xs">✅ PAGADA</span>
            <span v-else class="badge trial text-xs">🧪 PRUEBA</span>
          </div>

          <div v-if="dep.slug">
            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">URL Pública</div>
            <a :href="'/i/' + dep.slug" target="_blank" class="link text-sm font-bold">/i/{{ dep.slug }}</a>
          </div>
        </div>

        <!-- Acciones -->
        <div class="flex items-center gap-2 pt-3 border-t border-slate-100 flex-wrap">
          <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-sm btn-outline flex-1 text-center py-2">
            👁️ Ver
          </a>
          
          <router-link :to="'/builder/' + dep.id" class="btn btn-sm btn-primary flex-1 text-center py-2">
            🛠️ Editar
          </router-link>
          
          <button v-if="!dep.is_paid" @click="onPay(dep)" class="btn btn-sm btn-success flex-1 py-2">
            💰 Pagar
          </button>

          <button @click="onDelete(dep.id)" class="btn btn-sm btn-danger flex-1 py-2">
            🗑️ Borrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { crmService } from '@/modules/workspace/services/crmService';

const toast = useToast();
const deployments = ref([]);
const loading = ref(true);

const loadDeployments = async () => {
  loading.value = true;
  try {
    const res = await crmService.fetchAllDeployments();
    deployments.value = res.data;
  } catch (error) {
    toast.error('Error al cargar diseños globales.');
  } finally {
    loading.value = false;
  }
};

const onDelete = async (id) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el diseño #${id}? Esta acción es irreversible.`)) {
    try {
      import('@/modules/ecommerce/services/deploymentService').then(async ({ deploymentService }) => {
        await deploymentService.deleteDeployment(id);
        toast.success(`Diseño #${id} eliminado`);
        loadDeployments(); // Recargar la tabla
      });
    } catch (error) {
      toast.error('No se pudo eliminar el diseño.');
    }
  }
};

const onPay = async (dep) => {
  try {
    toast.info('Generando orden de pago...');
    // 1. Crear la orden para este deployment
    const orderData = {
      product: dep.product,
      deployment: dep.id,
      total_amount: "50.00", 
      user: dep.user
    };
    
    const res = await crmService.createOrder(orderData);
    const orderId = res.data.id;
    
    // 2. Generar el link de Stripe
    const successUrl = `${window.location.origin}/workspace/designs?success=true`;
    const cancelUrl = `${window.location.origin}/workspace/designs?cancel=true`;
    
    const checkoutRes = await crmService.createStripeCheckout(orderId, successUrl, cancelUrl);
    const { url } = checkoutRes.data;
    
    // 3. Redirigir
    window.location.href = url;
  } catch (error) {
    toast.error('Error al procesar el pago.');
    console.error(error);
  }
};

onMounted(() => {
  loadDeployments();
});
</script>

<style scoped>
.designs-manager {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
}
.btn-refresh { background: #f1f5f9; color: #475569; }
.btn-sm { font-size: 0.85rem; padding: 0.35rem 0.75rem; margin-right: 0.5rem; }
.btn-outline { border: 1px solid #cbd5e1; background: white; color: #475569; }
.btn-primary { background: #3b82f6; color: white; }
.btn-success { background: #10b981; color: white; }
.btn-danger { background: #ef4444; color: white; }

.data-grid { width: 100%; border-collapse: collapse; }
.data-grid th, .data-grid td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-grid th { background: #f8fafc; color: #64748b; font-weight: 600; }

.badge { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }
.badge.draft { background: #f1f5f9; color: #475569; }
.badge.live { background: #3b82f6; color: white; }
.badge.paid { background: #dcfce7; color: #16a34a; }
.badge.trial { background: #fef3c7; color: #d97706; }
.badge.expired { background: #fee2e2; color: #dc2626; }

.link { color: #3b82f6; text-decoration: underline; }
.text-muted { color: #94a3b8; }
.actions-cell { display: flex; align-items: center; }
</style>
