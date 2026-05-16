<template>
  <div class="min-h-screen bg-slate-50 relative">
    
    <!-- MARCA DE AGUA PREMIUM SANDBOX -->
    <div v-if="status === 'DRAFT' && !loading && !errorMsg" class="fixed top-0 left-0 w-full z-50">
      <div class="bg-gradient-to-r from-amber-600 via-amber-500 to-amber-600 text-white text-center py-2 font-black text-[10px] tracking-[0.3em] uppercase shadow-2xl border-b border-amber-400/30">
        ✨ MODO VISTA PREVIA - INVITAZYON DIGITAL ✨
      </div>
    </div>

    <!-- BOTÓN FLOTANTE DE COMPRA -->
    <div v-if="status === 'DRAFT' && !loading && !errorMsg" class="fixed bottom-8 right-8 z-50 animate-bounce">
      <button @click="goToCheckout" class="btn btn-primary rounded-2xl shadow-2xl shadow-primary/40 border-2 border-white/20 px-6 h-14 font-black">
        🛒 Eliminar Marca de Agua
      </button>
    </div>

    <!-- PANTALLA DE CARGA -->
    <div v-if="loading" class="min-h-screen flex flex-col items-center justify-center">
      <span class="loading loading-infinity w-16 text-primary"></span>
      <p class="mt-4 text-slate-500 font-medium">Preparando tu invitación...</p>
    </div>

    <!-- PANTALLA DE ERROR / EXPIRED -->
    <div v-else-if="errorMsg" class="min-h-screen flex items-center justify-center p-4">
      <div class="alert alert-error shadow-lg max-w-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <div>
          <h3 class="font-bold text-lg">Aviso importante</h3>
          <p class="text-sm">{{ errorMsg }}</p>
        </div>
      </div>
    </div>

    <!-- MOTOR DE RENDER -->
    <div v-else class="engine-canvas" :class="{ 'pt-6': status === 'DRAFT' }">
      
      <!-- INYECCIÓN DINÁMICA DE COMPONENTES -->
      <EngineCover :config="customData.cover || {}" />
      <EngineRSVP :slug="route.params.slug" :config="customData.rsvp || {}" />
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { engineService } from '@/modules/engine/services/engineService';
import EngineCover from '@/modules/engine/components/EngineCover.vue';
import EngineRSVP from '@/modules/engine/components/EngineRSVP.vue';

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const errorMsg = ref('');
const customData = ref({});
const status = ref('');
const deploymentId = ref(null);

const goToCheckout = () => {
  // Guardamos en localStorage que venimos de este sandbox para que el registro sepa qué reclamar
  if (deploymentId.value) {
    localStorage.setItem('claimed_deployment_id', deploymentId.value);
  }
  // Redirigimos al catálogo o directamente al checkout si tenemos el producto
  // Por ahora al catálogo para que elija bien, o al login si no tiene sesión
  router.push('/catalog');
};

onMounted(async () => {
  const slug = route.params.slug;
  try {
    const response = await engineService.fetchDeploymentBySlug(slug);
    status.value = response.data.status;
    deploymentId.value = response.data.id;
    
    if (status.value === 'EXPIRED') {
      errorMsg.value = 'Esta invitación ha expirado o ya no se encuentra activa.';
      return;
    }

    customData.value = response.data.custom_data || {};
  } catch (err) {
    errorMsg.value = 'No se encontró la invitación (URL inválida).';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Tailwind handles the layout */
</style>
