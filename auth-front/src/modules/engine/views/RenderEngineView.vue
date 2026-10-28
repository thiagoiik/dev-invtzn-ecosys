<template>
  <div class="min-h-screen bg-slate-50 relative">
    
    <!-- NOTE: Redundant watermark markups removed; fully handled inside RenderEngineMaster component -->

    <!-- PANTALLA DE CARGA PREMIUM -->
    <DataLoaderLoader v-if="loading" />
 
    <!-- PANTALLA DE ERROR / EXPIRED / INACTIVE -->
    <div v-else-if="errorMsg || ['EXPIRED', 'INACTIVE'].includes(status)" class="min-h-screen">
      <ExpiredEventScreen v-if="['EXPIRED', 'INACTIVE'].includes(status)" :status="status" />
      
      <div v-else class="min-h-screen flex items-center justify-center p-4">
        <div class="alert alert-error shadow-lg max-w-md rounded-3xl">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <div>
            <h3 class="font-bold text-lg text-white">Invitación no disponible</h3>
            <p class="text-sm text-white/80">{{ errorMsg }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- PANTALLA CREAR DEMO DESDE PLANTILLA ACTIVA (Solo para invitados) -->
    <div v-else-if="showCreateDemo" class="min-h-screen bg-gradient-to-tr from-slate-900 via-indigo-950 to-slate-900 flex items-center justify-center p-6 text-center">
      <div class="max-w-md w-full bg-white rounded-[2.5rem] p-10 shadow-2xl border border-slate-100 space-y-8 animate-scale-in">
        <div class="w-20 h-20 bg-gradient-to-tr from-indigo-50 to-indigo-100/50 rounded-2xl flex items-center justify-center text-4xl mx-auto shadow-inner animate-pulse-slow">
          ✨
        </div>

        <div class="space-y-3">
          <h2 class="text-2xl font-black text-slate-900 leading-tight">
            ¡Personaliza esta plantilla!
          </h2>
          <p class="text-slate-500 font-medium text-sm leading-relaxed">
            Ingresa tus datos para generar una demo interactiva gratuita de esta invitación en 5 segundos.
          </p>
        </div>

        <form @submit.prevent="handleCreateDemoSubmit" class="space-y-5 text-left">
          <div class="form-control">
            <label class="label"><span class="label-text font-black text-slate-500 uppercase tracking-widest text-[9px]">Nombres de los festejados</span></label>
            <input 
              v-model="demoForm.names" 
              type="text" 
              placeholder="Ej: Sofía & Alejandro" 
              class="input input-bordered w-full h-12 rounded-xl focus:border-indigo-500 text-base font-bold bg-slate-50 border-slate-200"
              required
            />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-black text-slate-500 uppercase tracking-widest text-[9px]">Fecha del Evento</span></label>
            <input 
              v-model="demoForm.date" 
              type="date" 
              class="input input-bordered w-full h-12 rounded-xl focus:border-indigo-500 text-base font-bold bg-slate-50 border-slate-200"
              required
            />
          </div>

          <div class="pt-4">
            <button 
              type="submit" 
              class="btn bg-gradient-to-r from-pink-500 to-indigo-600 hover:from-pink-600 hover:to-indigo-700 text-white font-black w-full h-14 rounded-xl shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2 border-none"
              :disabled="creatingDemo"
            >
              <span v-if="creatingDemo" class="loading loading-spinner loading-sm"></span>
              {{ creatingDemo ? 'Generando Demo...' : '✨ Crear Demo Gratis' }}
            </button>
          </div>
        </form>

        <div class="pt-4 border-t border-slate-100 flex items-center justify-center gap-2">
          <span class="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em]">Invitazyon Studio</span>
        </div>
      </div>
    </div>

    <!-- MOTOR DE RENDER INTELIGENTE -->
    <EnvelopeWrapper v-else :type="customData.envelope_type || customData.envelope">
      <RenderEngineMaster 
        :status="status" 
        :customData="customData" 
        :slug="route.params.slug" 
        :deploymentId="deploymentId"
        :tierLevel="tierLevel"
        :ownerId="ownerId"
        @purchase="goToCheckout"
      />
    </EnvelopeWrapper>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { engineService } from '@/modules/engine/services/engineService';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { useAuthStore } from '@/modules/auth/store/auth';
import DataLoaderLoader from '@/modules/engine/components/DataLoaderLoader.vue';
import ExpiredEventScreen from '@/modules/engine/components/ExpiredEventScreen.vue';
import RenderEngineMaster from '@/modules/engine/components/RenderEngineMaster.vue';
import EnvelopeWrapper from '@/modules/engine/components/EnvelopeWrapper.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const loading = ref(true);
const errorMsg = ref('');
const customData = ref({});
const status = ref('');
const deploymentId = ref(null);
const tierLevel = ref('BASIC');
const productId = ref(null);
const ownerId = ref(null);

const authStore = useAuthStore();

const isTeamMember = computed(() => {
  const role = authStore?.role || null;
  return ['ADMIN', 'DESIGNER', 'VENDOR', 'FRANCHISEE'].includes(role);
});

const showCreateDemo = computed(() => {
  return status.value === 'ACTIVE' && !isTeamMember.value;
});

const demoForm = ref({
  names: '',
  date: ''
});
const creatingDemo = ref(false);

const handleCreateDemoSubmit = async () => {
  if (!demoForm.value.names || !demoForm.value.date) {
    toast.error('Por favor, ingresa los nombres y la fecha del evento.');
    return;
  }
  
  creatingDemo.value = true;
  try {
    const formattedDate = formatDate(demoForm.value.date);
    const customDataPayload = {
      cover: {
        title: demoForm.value.names,
        date: formattedDate
      },
      rsvp: {
        eventTitle: demoForm.value.names,
        eventDate: formattedDate
      }
    };
    
    const res = await deploymentService.createSandbox(productId.value, customDataPayload);
    toast.success('¡Tu demo personalizada está lista!');
    
    localStorage.setItem('pending_sandbox_id', res.data.id);
    
    // Redirigir en la misma pestaña a su nueva demo
    window.location.href = `/i/${res.data.slug}`;
  } catch (error) {
    console.error(error);
    toast.error('Error al crear la demo de la plantilla.');
  } finally {
    creatingDemo.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const dateObj = new Date(dateString + 'T00:00:00');
  const options = { day: 'numeric', month: 'long', year: 'numeric' };
  return dateObj.toLocaleDateString('es-ES', options).toUpperCase();
};

const goToCheckout = () => {
  if (deploymentId.value) {
    localStorage.setItem('pending_sandbox_id', deploymentId.value);
  }
  
  const targetProductId = productId.value || 1;
  
  if (authStore.isAuthenticated) {
    router.push({ name: 'checkout', params: { id: targetProductId } });
  } else {
    router.push({ 
      name: 'register', 
      query: { redirect: `/checkout/${targetProductId}` } 
    });
  }
};

onMounted(async () => {
  const slug = route.params.slug;
  try {
    const response = await engineService.fetchDeploymentBySlug(slug);
    status.value = response.data.status;
    deploymentId.value = response.data.id;
    tierLevel.value = response.data.tier_level || 'BASIC';
    productId.value = response.data.product_id || null;
    ownerId.value = response.data.user_id || null;
    
    if (['EXPIRED', 'INACTIVE'].includes(status.value)) {
      return;
    }

    customData.value = response.data.custom_data || {};
    
    try {
      engineService.submitMetric(slug, 'VISIT').catch(() => {});
    } catch (err) {}
  } catch (err) {
    errorMsg.value = 'No se encontró la invitación (URL inválida).';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.animate-pulse-slow {
  animation: pulseSlow 3s infinite ease-in-out;
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulseSlow {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(99, 102, 241, 0)); }
  50% { transform: scale(1.05); filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.2)); }
}
</style>
