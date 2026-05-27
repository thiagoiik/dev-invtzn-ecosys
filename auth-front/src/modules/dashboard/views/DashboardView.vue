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
          <div class="flex flex-wrap items-center gap-2 mb-6">
            <span :class="[
              'badge text-[10px] font-bold px-2 py-1 rounded-md border-none uppercase tracking-wider',
              dep.creation_mode === 'CATALOG' ? 'bg-indigo-50 text-indigo-600' : 'bg-pink-50 text-pink-600'
            ]">
              {{ dep.creation_mode === 'CATALOG' ? 'Cliente A (Catálogo)' : 'Cliente B (Canvas)' }}
            </span>
            <span v-if="dep.creation_mode === 'CATALOG' && dep.custom_data?.is_catalog_complete" class="badge text-[10px] font-bold px-2 py-1 rounded-md border-none uppercase tracking-wider bg-emerald-50 text-emerald-600">
              ✓ Listo
            </span>
            <span class="text-xs text-slate-400 font-medium">
              {{ dep.is_paid ? 'Pagado' : 'Pendiente' }}
            </span>
          </div>
          
          <div class="flex flex-col gap-2 pt-6 border-t border-slate-50">
            <div class="grid grid-cols-2 gap-2">
              <!-- Botones diferenciados Cliente A vs Cliente B -->
              <template v-if="dep.creation_mode === 'CATALOG'">
                <router-link :to="'/builder/' + dep.id + '/form'" class="btn btn-ghost bg-slate-50 hover:bg-primary hover:text-white rounded-xl font-bold text-xs flex items-center justify-center gap-1">
                  ✏️ Formulario
                </router-link>
              </template>
              <template v-else>
                <router-link :to="'/builder/' + dep.id" class="btn btn-ghost bg-slate-50 hover:bg-primary hover:text-white rounded-xl font-bold text-xs flex items-center justify-center gap-1">
                  ✏️ Studio
                </router-link>
              </template>

              <a v-if="dep.slug" :href="'/i/' + dep.slug" target="_blank" class="btn btn-ghost bg-slate-50 hover:bg-slate-100 rounded-xl font-bold text-xs flex items-center justify-center gap-1">
                👁️ Ver
              </a>
            </div>
            
            <button v-if="dep.slug" @click="openShareModal(dep)" class="btn btn-primary rounded-xl font-black text-xs shadow-lg shadow-primary/10 w-full py-2.5 flex items-center justify-center gap-1">
              🔗 Compartir
            </button>
          </div>
          
          <button @click="onDelete(dep.id)" class="btn btn-error btn-xs btn-ghost mt-4 w-full text-error/50 hover:text-error opacity-0 group-hover:opacity-100 transition-opacity">
            Eliminar diseño
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Premium de Compartir y Personalización -->
    <div v-if="showShareModal" class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="closeShareModal"></div>
      <div class="relative w-full max-w-lg bg-white/90 backdrop-blur-xl rounded-[2rem] shadow-2xl p-8 border border-slate-100/50 overflow-hidden flex flex-col gap-6">
        <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-primary to-indigo-500"></div>
        
        <div class="flex justify-between items-center">
          <h3 class="text-2xl font-black text-slate-800">Compartir Invitación</h3>
          <button @click="closeShareModal" class="text-slate-400 hover:text-slate-600 font-bold text-xl">✕</button>
        </div>
        
        <div class="space-y-4">
          <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100">
            <span class="text-xs text-slate-400 font-bold uppercase tracking-wider block mb-1">Enlace Actual</span>
            <div class="flex items-center justify-between gap-2 overflow-hidden">
              <span class="text-sm font-mono text-slate-700 truncate select-all">{{ currentInvitationUrl }}</span>
              <button @click="copyLink" class="btn btn-xs btn-outline px-3 py-1.5 rounded-lg border-slate-200 text-slate-600 hover:bg-slate-100 font-bold flex-shrink-0">
                📋 Copiar
              </button>
            </div>
          </div>
          
          <!-- Slug Customizer (Personalizador) -->
          <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-3">
            <span class="text-xs text-slate-400 font-bold uppercase tracking-wider block">Personalizar Enlace (Slug)</span>
            <div class="flex gap-2">
              <input 
                v-model="newSlug" 
                type="text" 
                placeholder="ej-mi-boda" 
                class="input input-bordered w-full h-11 rounded-xl text-sm font-mono px-3 border border-slate-200 bg-white"
                :disabled="savingSlug"
              />
              <button 
                @click="updateSlug" 
                class="btn btn-primary h-11 min-h-0 rounded-xl px-5 font-bold text-sm shadow-sm"
                :disabled="savingSlug"
              >
                {{ savingSlug ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
            <p class="text-[10px] text-slate-400 leading-normal">
              Solo letras minúsculas, números y guiones. Ej: mi-boda-2026.
            </p>
          </div>
        </div>

        <div class="flex flex-col gap-3 pt-2">
          <a :href="whatsappUrl" target="_blank" class="btn bg-emerald-500 hover:bg-emerald-600 text-white w-full py-3.5 rounded-2xl font-black flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 text-center">
            💬 Compartir por WhatsApp
          </a>
          
          <button @click="closeShareModal" class="btn btn-ghost text-slate-400 font-bold uppercase tracking-widest text-[10px] mt-2">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import { useRouter } from 'vue-router';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { useToast } from 'vue-toastification';
import invtznClient from '@/core/api/invtznClient';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const deployments = ref([]);
const loading = ref(true);
const showSuccessAlert = ref(false);

const showShareModal = ref(false);
const selectedDep = ref(null);
const newSlug = ref('');
const savingSlug = ref(false);

const openShareModal = (dep) => {
  selectedDep.value = dep;
  newSlug.value = dep.slug || '';
  showShareModal.value = true;
};

const closeShareModal = () => {
  showShareModal.value = false;
  selectedDep.value = null;
  newSlug.value = '';
};

const currentInvitationUrl = computed(() => {
  if (!selectedDep.value || !selectedDep.value.slug) return '';
  return `${window.location.origin}/i/${selectedDep.value.slug}`;
});

const copyLink = () => {
  if (currentInvitationUrl.value) {
    navigator.clipboard.writeText(currentInvitationUrl.value);
    toast.success('¡Enlace copiado al portapapeles!');
  }
};

const whatsappUrl = computed(() => {
  if (!currentInvitationUrl.value) return '';
  const text = `¡Hola! Queremos invitarte a nuestro evento. Mira todos los detalles y confirma tu asistencia aquí: ${currentInvitationUrl.value}`;
  return `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
});

const updateSlug = async () => {
  if (!newSlug.value) {
    toast.error('El slug no puede estar vacío.');
    return;
  }
  const slugRegex = /^[a-z0-9-]+$/;
  if (!slugRegex.test(newSlug.value)) {
    toast.error('El slug solo puede contener letras minúsculas, números y guiones.');
    return;
  }
  
  savingSlug.value = true;
  try {
    const res = await invtznClient.patch(`deployments/${selectedDep.value.id}/`, {
      slug: newSlug.value
    });
    // Update local state
    selectedDep.value.slug = res.data.slug;
    const idx = deployments.value.findIndex(d => d.id === selectedDep.value.id);
    if (idx !== -1) {
      deployments.value[idx].slug = res.data.slug;
    }
    toast.success('¡Enlace personalizado guardado con éxito!');
  } catch (error) {
    const serverMsg = error.response?.data?.slug?.[0] || 'No se pudo guardar el slug personalizado.';
    toast.error(serverMsg);
  } finally {
    savingSlug.value = false;
  }
};

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