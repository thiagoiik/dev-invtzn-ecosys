<template>
  <div v-if="authStore.user" class="space-y-8">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">Mis Diseños</h1>
        <p class="text-slate-500 mt-1">Bienvenido, <strong class="text-primary">{{ authStore.user.username }}</strong>. Gestiona tus invitaciones aquí.</p>
      </div>
      <router-link to="/catalog" class="btn btn-primary rounded-2xl shadow-lg shadow-primary/20 px-8 h-14">
        ✨ Nuevo Diseño
      </router-link>
    </div>

    <!-- Mensaje de Éxito de Pago -->
    <div v-if="showSuccessAlert" class="alert alert-success shadow-2xl shadow-success/20 rounded-[2rem] p-6 border-none animate-bounce">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">🎉</div>
        <div>
          <h3 class="font-black text-white text-lg">¡Pago Confirmado!</h3>
          <p class="text-white/80 text-sm">Tu diseño ha sido activado. Ya puedes compartirlo con tus invitados sin marca de agua.</p>
        </div>
      </div>
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
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="group bg-white rounded-[2.5rem] p-8 shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all duration-500 border border-slate-100" v-for="dep in deployments" :key="dep.id">
          <div class="flex justify-between items-start mb-6">
            <div class="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-2xl group-hover:bg-primary/10 transition-colors">
              💎
            </div>
            <div :class="[
              'badge font-black text-[10px] tracking-widest px-3 py-2 rounded-lg border-none uppercase',
              dep.status === 'LIVE' ? 'bg-success/10 text-success' : 'bg-warning/10 text-warning'
            ]">
              {{ dep.status }}
            </div>
          </div>
          
          <h3 class="text-xl font-black text-slate-900 mb-2">Diseño #{{ dep.id }}</h3>
          <p class="text-sm text-slate-400 font-medium mb-8">Estado: {{ dep.is_paid ? 'Pagado' : 'Pendiente de Pago' }}</p>
          
          <div class="grid grid-cols-2 gap-4 pt-6 border-t border-slate-50">
            <router-link :to="'/builder/' + dep.id" class="btn btn-ghost bg-slate-50 hover:bg-primary hover:text-white rounded-xl font-bold">
              ✏️ Editar
            </router-link>
            <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-primary rounded-xl font-black shadow-lg shadow-primary/10">
              👁️ Ver
            </a>
          </div>
          <button @click="onDelete(dep.id)" class="btn btn-error btn-xs btn-ghost mt-4 w-full text-error/50 hover:text-error opacity-0 group-hover:opacity-100 transition-opacity">
            Eliminar diseño
          </button>
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
const showSuccessAlert = ref(false);

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
  
  // Revisar si venimos de un pago exitoso
  if (router.currentRoute.value.query.payment === 'success') {
    showSuccessAlert.value = true;
    toast.success('¡Gracias por tu compra!');
    
    // Limpiar el parámetro de la URL después de unos segundos
    setTimeout(() => {
      router.replace({ query: {} });
    }, 5000);
  }
});

</script>

<style scoped>
/* Eliminated old manual CSS. Handled by Tailwind. */
</style>