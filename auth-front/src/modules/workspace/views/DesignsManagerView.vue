<template>
  <div class="space-y-6">
    <!-- Header cockpit card -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Línea de Tiempo de Diseños</h2>
        <p class="text-slate-500">Supervisa las invitaciones según la etapa de vida del evento: desde la maquetación hasta el archivo histórico.</p>
      </div>
      <div class="flex items-center gap-2 w-full sm:w-auto">
        <div class="relative flex-1 sm:w-64">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-400">
            🔍
          </span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por ID, Slug o Cliente..." 
            class="input input-bordered w-full pl-9 h-11 rounded-xl text-sm"
          />
        </div>
        <button @click="loadDeployments" class="btn btn-ghost bg-slate-50 hover:bg-slate-100 border border-slate-200 h-11 px-4 rounded-xl flex items-center gap-2" :disabled="loading">
          <span>🔄</span> Actualizar
        </button>
      </div>
    </div>

    <!-- Pestañas Horizontes de Tiempo -->
    <div class="tabs tabs-boxed bg-slate-100 p-1.5 rounded-2xl flex flex-wrap gap-1">
      <button 
        class="tab flex-1 h-11 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all"
        :class="{ 'tab-active bg-white text-primary shadow-sm': activeTab === 'design' }"
        @click="activeTab = 'design'"
      >
        🛠️ En Diseño
        <span class="badge badge-sm" :class="activeTab === 'design' ? 'badge-primary text-white' : 'badge-ghost'">
          {{ filteredGroupedDeployments.design.length }}
        </span>
      </button>
      
      <button 
        class="tab flex-1 h-11 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all"
        :class="{ 'tab-active bg-white text-primary shadow-sm': activeTab === 'active' }"
        @click="activeTab = 'active'"
      >
        🟢 Activas (Pre-Evento)
        <span class="badge badge-sm" :class="activeTab === 'active' ? 'badge-primary text-white' : 'badge-ghost'">
          {{ filteredGroupedDeployments.active.length }}
        </span>
      </button>
      
      <button 
        class="tab flex-1 h-11 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all"
        :class="{ 'tab-active bg-white text-primary shadow-sm': activeTab === 'postEvent' }"
        @click="activeTab = 'postEvent'"
      >
        🌅 Post-Evento
        <span class="badge badge-sm" :class="activeTab === 'postEvent' ? 'badge-primary text-white' : 'badge-ghost'">
          {{ filteredGroupedDeployments.postEvent.length }}
        </span>
      </button>
      
      <button 
        class="tab flex-1 h-11 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all"
        :class="{ 'tab-active bg-white text-primary shadow-sm': activeTab === 'archived' }"
        @click="activeTab = 'archived'"
      >
        📦 Archivadas
        <span class="badge badge-sm" :class="activeTab === 'archived' ? 'badge-primary text-white' : 'badge-ghost'">
          {{ filteredGroupedDeployments.archived.length }}
        </span>
      </button>
    </div>

    <!-- Contenido Principal -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div v-if="loading" class="flex justify-center items-center p-20">
        <span class="loading loading-spinner loading-lg text-primary"></span>
      </div>
      
      <div v-else-if="currentTabList.length === 0" class="p-20 text-center text-slate-400">
        <div class="text-4xl mb-3">📂</div>
        <p class="italic font-medium">No se encontraron diseños en esta fase de la línea de tiempo.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="table w-full table-zebra">
          <thead>
            <tr class="bg-slate-50/75 text-slate-600 font-bold border-b border-slate-200">
              <th class="px-6 py-4">ID</th>
              <th class="px-6 py-4">Cliente / Producto</th>
              <th class="px-6 py-4">Modo de Creación</th>
              <th class="px-6 py-4">Fecha del Evento</th>
              <th class="px-6 py-4">Estado de Pago</th>
              <th class="px-6 py-4">URL Pública</th>
              <th class="px-6 py-4 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dep in currentTabList" :key="dep.id" class="border-b border-slate-100 hover:bg-slate-50/50 transition-colors">
              <td class="px-6 py-4 font-bold text-slate-700">#{{ dep.id }}</td>
              <td class="px-6 py-4">
                <div class="font-bold text-slate-800">Usuario ID: {{ dep.user || 'Anónimo' }}</div>
                <div class="text-xs text-slate-400">Producto ID: {{ dep.product }}</div>
              </td>
              <td class="px-6 py-4 text-xs">
                <span :class="[
                  'badge badge-sm font-bold tracking-wide uppercase',
                  dep.creation_mode === 'CATALOG' ? 'bg-indigo-50 text-indigo-600 border-none' : 'bg-pink-50 text-pink-600 border-none'
                ]">
                  {{ dep.creation_mode === 'CATALOG' ? 'Cliente A (Catálogo)' : 'Cliente B (Canvas)' }}
                </span>
              </td>
              <td class="px-6 py-4 text-xs text-slate-600 font-semibold">
                {{ formatEventDate(dep) }}
              </td>
              <td class="px-6 py-4 text-xs">
                <span v-if="dep.is_paid" class="badge badge-success text-white font-bold gap-1 px-2.5">
                  ✅ PAGADA
                </span>
                <span v-else class="badge badge-warning text-amber-950 font-bold gap-1 px-2.5">
                  🧪 PRUEBA
                </span>
              </td>
              <td class="px-6 py-4">
                <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="link link-primary font-bold text-xs">
                  /i/{{ dep.slug }}
                </a>
                <span v-else class="text-slate-400 italic text-xs">Sin asignar</span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex justify-end gap-1">
                  <!-- Previsualizar -->
                  <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-xs btn-outline btn-square text-base" title="Ver en vivo">
                    👁️
                  </a>
                  
                  <!-- Métricas -->
                  <button @click="onShowMetrics(dep.id)" class="btn btn-xs btn-outline btn-square text-base" title="Ver Métricas">
                    📊
                  </button>
                  
                  <!-- Entrar al Studio / Formulario -->
                  <router-link :to="dep.creation_mode === 'CATALOG' ? '/builder/' + dep.id + '/form' : '/builder/' + dep.id" class="btn btn-xs btn-primary font-black px-3.5" :title="dep.creation_mode === 'CATALOG' ? 'Abrir Formulario' : 'Abrir Studio'">
                    Editar
                  </router-link>
                  
                  <!-- Activar Pago -->
                  <button v-if="!dep.is_paid" @click="onPay(dep)" class="btn btn-xs btn-success text-white font-bold px-3.5" title="Marcar como Pagada">
                    Activar
                  </button>

                  <!-- Eliminar -->
                  <button @click="onDelete(dep.id)" class="btn btn-xs btn-error text-white btn-square text-base" title="Eliminar Diseño">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Drawer de Métricas -->
    <DeploymentMetricsDrawer 
      :isOpen="isMetricsOpen" 
      :deploymentId="selectedDeploymentId" 
      @close="isMetricsOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useToast } from 'vue-toastification';
import { crmService } from '@/modules/workspace/services/crmService';
import DeploymentMetricsDrawer from '@/modules/workspace/components/DeploymentMetricsDrawer.vue';

const toast = useToast();
const deployments = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const activeTab = ref('design');

const isMetricsOpen = ref(false);
const selectedDeploymentId = ref(null);

const onShowMetrics = (id) => {
  selectedDeploymentId.value = id;
  isMetricsOpen.value = true;
};

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

const parseEventDate = (dep) => {
  const targetDateStr = dep.custom_data?.timer?.targetDate || dep.custom_data?.cover?.date;
  if (!targetDateStr) return null;
  // Si la fecha tiene formato ISO
  const parsed = Date.parse(targetDateStr);
  if (!isNaN(parsed)) return new Date(parsed);
  return null;
};

const formatEventDate = (dep) => {
  const dateObj = parseEventDate(dep);
  if (!dateObj) {
    return dep.custom_data?.cover?.date || 'Sin fecha asignada';
  }
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  return dateObj.toLocaleDateString('es-ES', options).toUpperCase();
};

const groupedDeployments = computed(() => {
  const now = new Date();
  const groups = {
    design: [],
    active: [],
    postEvent: [],
    archived: []
  };

  deployments.value.forEach(dep => {
    const status = dep.status || 'DRAFT';
    if (status === 'EXPIRED') {
      groups.archived.push(dep);
    } else if (status === 'DRAFT') {
      groups.design.push(dep);
    } else if (status === 'LIVE') {
      const eventDate = parseEventDate(dep);
      if (eventDate && eventDate < now) {
        groups.postEvent.push(dep);
      } else {
        groups.active.push(dep);
      }
    } else {
      groups.design.push(dep);
    }
  });

  return groups;
});

const filteredGroupedDeployments = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  const allGroups = groupedDeployments.value;

  if (!query) return allGroups;

  const filterList = (list) => {
    return list.filter(dep => {
      const idMatches = String(dep.id).includes(query);
      const userMatches = String(dep.user || '').includes(query);
      const slugMatches = dep.slug && dep.slug.toLowerCase().includes(query);
      const namesMatches = dep.custom_data?.cover?.title && dep.custom_data.cover.title.toLowerCase().includes(query);
      return idMatches || userMatches || slugMatches || namesMatches;
    });
  };

  return {
    design: filterList(allGroups.design),
    active: filterList(allGroups.active),
    postEvent: filterList(allGroups.postEvent),
    archived: filterList(allGroups.archived)
  };
});

const currentTabList = computed(() => {
  return filteredGroupedDeployments.value[activeTab.value] || [];
});

const onDelete = async (id) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el diseño #${id}? Esta acción es irreversible.`)) {
    try {
      const { deploymentService } = await import('@/modules/ecommerce/services/deploymentService');
      await deploymentService.deleteDeployment(id);
      toast.success(`Diseño #${id} eliminado`);
      loadDeployments();
    } catch (error) {
      toast.error('No se pudo eliminar el diseño.');
    }
  }
};

const onPay = async (dep) => {
  try {
    toast.info('Generando orden de pago...');
    const orderData = {
      product: dep.product,
      deployment: dep.id,
      total_amount: "50.00", 
      user: dep.user
    };
    
    const res = await crmService.createOrder(orderData);
    const orderId = res.data.id;
    
    const successUrl = `${window.location.origin}/workspace/designs?success=true`;
    const cancelUrl = `${window.location.origin}/workspace/designs?cancel=true`;
    
    const checkoutRes = await crmService.createStripeCheckout(orderId, successUrl, cancelUrl);
    const { url } = checkoutRes.data;
    
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
