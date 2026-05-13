<template>
  <div class="render-engine">
    <!-- PANTALLA DE CARGA -->
    <div v-if="loading" class="full-screen-center">
      <p>Cargando invitación...</p>
    </div>

    <!-- PANTALLA DE ERROR / EXPIRED -->
    <div v-else-if="errorMsg" class="full-screen-center error">
      <h2>⚠️ Aviso</h2>
      <p>{{ errorMsg }}</p>
    </div>

    <!-- MOTOR DE RENDER -->
    <div v-else class="engine-canvas">
      
      <!-- MARCA DE AGUA SANDBOX -->
      <div v-if="status === 'DRAFT'" class="watermark-draft">
        VISTA PREVIA (MODO SANDBOX)
      </div>

      <!-- INYECCIÓN DINÁMICA DE COMPONENTES -->
      <!-- En el futuro iteraremos sobre custom_data.blocks, por ahora los montamos fijos para la prueba -->
      <EngineCover :config="customData.cover || {}" />
      <EngineRSVP :config="customData.rsvp || {}" />
      
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
.render-engine {
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff;
}
.full-screen-center {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
}
.error {
  background-color: #fef2f2;
  color: #991b1b;
}
.error h2 {
  margin-bottom: 1rem;
}

/* Marca de Agua */
.watermark-draft {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  text-align: center;
  padding: 0.5rem;
  font-weight: bold;
  z-index: 9999;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  letter-spacing: 2px;
}
</style>
