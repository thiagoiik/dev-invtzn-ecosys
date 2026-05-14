<template>
  <div class="designs-manager">
    <div class="header">
      <h3>Gestión de Diseños (Deployments)</h3>
      <button @click="loadDeployments" class="btn btn-refresh">🔄 Actualizar</button>
    </div>

    <div v-if="loading" class="loading">Cargando diseños globales...</div>
    
    <table v-else class="data-grid">
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente (ID)</th>
          <th>Producto</th>
          <th>Estado</th>
          <th>URL Pública</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dep in deployments" :key="dep.id">
          <td>#{{ dep.id }}</td>
          <td>Usuario {{ dep.user }}</td>
          <td>Prod #{{ dep.product }}</td>
          <td>
            <span :class="['badge', dep.status.toLowerCase()]">{{ dep.status }}</span>
          </td>
          <td>
            <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="link">/i/{{ dep.slug }}</a>
            <span v-else class="text-muted">Sin asignar</span>
          </td>
          <td class="actions-cell">
            <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-sm btn-outline">👁️ Previa</a>
            
            <!-- Vendedores no verán este botón, pero por ahora lo ocultaremos dinámicamente si sabemos su rol. 
                 Como protección real, el Backend ya prohíbe el guardado si entra. -->
            <router-link :to="'/builder/' + dep.id" class="btn btn-sm btn-primary">
              🛠️ Editor
            </router-link>
            
            <button @click="onDelete(dep.id)" class="btn btn-sm btn-danger" style="margin-left: 0.5rem;">
              🗑️
            </button>
          </td>
        </tr>
      </tbody>
    </table>
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
.btn-danger { background: #ef4444; color: white; }

.data-grid { width: 100%; border-collapse: collapse; }
.data-grid th, .data-grid td { padding: 1rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
.data-grid th { background: #f8fafc; color: #64748b; font-weight: 600; }

.badge { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }
.badge.draft { background: #fef3c7; color: #d97706; }
.badge.live { background: #dcfce7; color: #16a34a; }
.badge.expired { background: #fee2e2; color: #dc2626; }

.link { color: #3b82f6; text-decoration: underline; }
.text-muted { color: #94a3b8; }
.actions-cell { display: flex; align-items: center; }
</style>
