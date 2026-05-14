<template>
  <div v-if="authStore.user" class="dashboard-container">
    <div class="header">
      <h1>Panel B2C</h1>
      <button class="btn-logout" @click="onLogout">Cerrar Sesión</button>
    </div>
    <p>Bienvenido, <strong>{{ authStore.user.username }}</strong></p>

    <div class="deployments-section">
      <h2>Tus Diseños (Deployments)</h2>
      
      <div v-if="loading">Cargando tus invitaciones...</div>
      <div v-else-if="deployments.length === 0">
        <p>Aún no tienes invitaciones.</p>
        <router-link to="/catalog" class="btn btn-primary">Ver Catálogo</router-link>
      </div>
      
      <div v-else class="cards">
        <div class="card" v-for="dep in deployments" :key="dep.id">
          <span class="badge">{{ dep.status }}</span>
          <h3>Diseño #{{ dep.id }}</h3>
          <p>Producto ID: {{ dep.product }}</p>
          <div class="card-actions">
            <router-link :to="'/builder/' + dep.id" class="btn btn-secondary">✏️ Editar Diseño</router-link>
            <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-link">👁️ Ver Previa</a>
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

onMounted(async () => {
  try {
    const res = await deploymentService.fetchMyDeployments();
    deployments.value = res.data;
  } catch (error) {
    toast.error('Error al cargar diseños.');
  } finally {
    loading.value = false;
  }
});

const onLogout = () => {
  authStore.logout();
  router.push({ name: 'login' });
};
</script>

<style scoped>
.dashboard-container { padding: 2rem; max-width: 1000px; margin: 0 auto; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.btn-logout { background: transparent; border: 1px solid #ef4444; color: #ef4444; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; }
.btn-logout:hover { background: #fee2e2; }

.deployments-section { margin-top: 3rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
.card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); position: relative; border: 1px solid #e2e8f0; }
.badge { position: absolute; top: 1rem; right: 1rem; background: #fef3c7; color: #d97706; padding: 0.2rem 0.6rem; border-radius: 99px; font-size: 0.75rem; font-weight: bold; }
.card-actions { margin-top: 1.5rem; display: flex; gap: 0.5rem; }
.btn { padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.9rem; text-align: center; }
.btn-primary { background: #3b82f6; color: white; }
.btn-secondary { background: #f8fafc; color: #475569; border: 1px solid #cbd5e1; flex: 1; }
.btn-secondary:hover { background: #f1f5f9; }
.btn-link { color: #3b82f6; border: 1px solid #bfdbfe; background: transparent; flex: 1; }
.btn-link:hover { background: #eff6ff; }
</style>