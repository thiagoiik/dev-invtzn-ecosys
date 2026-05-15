<template>
  <div class="min-h-screen bg-slate-50 relative">
    
    <!-- MARCA DE AGUA SANDBOX -->
    <div v-if="status === 'DRAFT' && !loading && !errorMsg" class="fixed top-0 left-0 w-full bg-error text-error-content text-center py-1 font-bold text-xs tracking-widest z-50 uppercase shadow-md">
      Vista Previa (Modo Sandbox)
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
import { useRoute } from 'vue-router';
import { engineService } from '@/modules/engine/services/engineService';
import EngineCover from '@/modules/engine/components/EngineCover.vue';
import EngineRSVP from '@/modules/engine/components/EngineRSVP.vue';

const route = useRoute();
const loading = ref(true);
const errorMsg = ref('');
const customData = ref({});
const status = ref('');

onMounted(async () => {
  const slug = route.params.slug;
  try {
    const response = await engineService.fetchDeploymentBySlug(slug);
    status.value = response.data.status;
    
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
