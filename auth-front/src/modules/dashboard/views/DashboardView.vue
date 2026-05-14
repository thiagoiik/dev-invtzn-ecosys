<template>
  <div v-if="authStore.user" class="space-y-8">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-slate-800">Panel B2C</h1>
        <p class="text-slate-500 mt-1">Bienvenido de vuelta, <strong class="text-slate-700">{{ authStore.user.username }}</strong></p>
      </div>
      <router-link to="/catalog" class="btn btn-primary">Explorar Catálogo</router-link>
    </div>

    <div>
      <h2 class="text-xl font-bold text-slate-800 border-b border-slate-200 pb-2 mb-6">Tus Diseños (Deployments)</h2>
      
      <div v-if="loading" class="flex justify-center py-12">
        <span class="loading loading-spinner loading-lg text-primary"></span>
      </div>
      
      <div v-else-if="deployments.length === 0" class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 text-center">
        <div class="text-4xl mb-4">🎨</div>
        <h3 class="text-lg font-bold text-slate-800">Aún no tienes diseños</h3>
        <p class="text-slate-500 mt-2 mb-6">Visita el catálogo para empezar a crear tus invitaciones.</p>
        <router-link to="/catalog" class="btn btn-primary">Ir al Catálogo</router-link>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="card bg-white shadow-xl border border-slate-100 transition-all hover:-translate-y-1 hover:shadow-2xl" v-for="dep in deployments" :key="dep.id">
          <div class="card-body">
            <div class="flex justify-between items-start mb-2">
              <h3 class="card-title text-lg">Diseño #{{ dep.id }}</h3>
              <div class="badge badge-warning badge-sm font-bold">{{ dep.status }}</div>
            </div>
            
            <p class="text-sm text-slate-500">Producto Base ID: {{ dep.product }}</p>
            
            <div class="card-actions justify-end mt-6 pt-4 border-t border-slate-100 flex-nowrap">
              <router-link :to="'/builder/' + dep.id" class="btn btn-sm btn-outline btn-primary flex-1">✏️ Editar</router-link>
              <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-sm btn-outline flex-1">👁️ Previa</a>
              <button @click="onDelete(dep.id)" class="btn btn-sm btn-error btn-square text-white tooltip tooltip-top" data-tip="Eliminar">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useRouter } from 'vue-router';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const deployments = ref([]);
const loading = ref(true);

const fetchDeployments = async () => {
  loading.value = true;
  try {
    const res = await deploymentService.fetchMyDeployments();
    deployments.value = res.data;
  } catch (error) {
    toast.error('Error al cargar diseños.');
  } finally {
    loading.value = false;
  }
};

const onDelete = async (id) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el diseño #${id}? Esta acción es irreversible.`)) {
    try {
      await deploymentService.deleteDeployment(id);
      toast.success(`Diseño #${id} eliminado`);
      fetchDeployments(); // Recargar la lista
    } catch (error) {
      toast.error('No se pudo eliminar el diseño.');
    }
  }
};

onMounted(() => {
  fetchDeployments();
});

<style scoped>
/* Eliminated old manual CSS. Handled by Tailwind. */
</style>