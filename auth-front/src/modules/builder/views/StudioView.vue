<template>
  <BuilderLayout>
    <template #actions>
      <button class="btn-save" @click="saveDesign" :disabled="saving">
        {{ saving ? 'Guardando...' : '💾 Guardar Diseño' }}
      </button>
    </template>

    <div class="studio-container">
      <!-- PANEL IZQUIERDO: CONTROLES -->
      <aside class="control-panel">
        <h3>Ajustes de Diseño</h3>
        
        <div v-if="loading" class="loading-state">
          Cargando configuración...
        </div>
        
        <form v-else class="config-form" @submit.prevent>
          <div class="form-group">
            <label>Título de la Invitación</label>
            <input v-model="localConfig.cover.title" type="text" placeholder="Ej: Boda de Ana y Juan" />
          </div>
          
          <div class="form-group">
            <label>Subtítulo</label>
            <input v-model="localConfig.cover.subtitle" type="text" placeholder="Ej: ¡Te invitamos a celebrar!" />
          </div>
          
          <div class="form-group">
            <label>Fecha del Evento</label>
            <input v-model="localConfig.cover.date" type="text" placeholder="Ej: 25 de Diciembre 2026" />
          </div>

          <div class="form-group">
            <label>URL de Imagen de Fondo</label>
            <input v-model="localConfig.cover.coverPhoto" type="url" placeholder="https://..." />
          </div>
          
          <div class="color-pickers">
            <div class="form-group">
              <label>Color Título</label>
              <input v-model="localConfig.cover.titleColor" type="color" />
            </div>
            <div class="form-group">
              <label>Color Fondo RSVP</label>
              <input v-model="localConfig.rsvp.bgColor" type="color" />
            </div>
          </div>
        </form>
      </aside>

      <!-- PANEL DERECHO: LIVE PREVIEW -->
      <section class="preview-panel">
        <div class="device-frame">
          <!-- Inyectamos los componentes del Engine en tiempo real -->
          <div class="preview-canvas">
            <EngineCover :config="localConfig.cover || {}" />
            <EngineRSVP :config="localConfig.rsvp || {}" />
          </div>
        </div>
      </section>
    </div>
  </BuilderLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import BuilderLayout from '@/layouts/BuilderLayout.vue';
import { builderService } from '@/modules/builder/services/builderService';
import EngineCover from '@/modules/engine/components/EngineCover.vue';
import EngineRSVP from '@/modules/engine/components/EngineRSVP.vue';

const route = useRoute();
const toast = useToast();
const deploymentId = route.params.id;

const loading = ref(true);
const saving = ref(false);

// Estructura por defecto en caso de que esté vacío
const localConfig = ref({
  cover: {
    title: '',
    subtitle: '',
    date: '',
    coverPhoto: '',
    titleColor: '#ffffff'
  },
  rsvp: {
    bgColor: '#f8fafc',
    btnColor: '#3b82f6'
  }
});

onMounted(async () => {
  try {
    const res = await builderService.getDeployment(deploymentId);
    if (res.data.custom_data && Object.keys(res.data.custom_data).length > 0) {
      // Fusionar datos existentes para no romper la reactividad profunda
      localConfig.value = { ...localConfig.value, ...res.data.custom_data };
    }
  } catch (error) {
    toast.error('Error al cargar la configuración');
  } finally {
    loading.value = false;
  }
});

const saveDesign = async () => {
  saving.value = true;
  try {
    await builderService.saveCustomData(deploymentId, localConfig.value);
    toast.success('¡Diseño guardado exitosamente!');
  } catch (error) {
    toast.error('No se pudo guardar el diseño');
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
.btn-save {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}
.btn-save:hover:not(:disabled) {
  background: #059669;
}
.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.studio-container {
  display: flex;
  width: 100%;
  height: 100%;
}

/* Panel de Controles */
.control-panel {
  width: 350px;
  background: #334155;
  color: white;
  padding: 2rem;
  overflow-y: auto;
  border-right: 1px solid #1e293b;
}
.control-panel h3 {
  margin-bottom: 2rem;
  color: #e2e8f0;
}
.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}
.form-group label {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: #94a3b8;
}
.form-group input[type="text"],
.form-group input[type="url"] {
  background: #1e293b;
  border: 1px solid #475569;
  color: white;
  padding: 0.75rem;
  border-radius: 6px;
}
.form-group input:focus {
  outline: none;
  border-color: #38bdf8;
}
.color-pickers {
  display: flex;
  gap: 1rem;
}

/* Panel de Preview */
.preview-panel {
  flex: 1;
  background: #0f172a;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  overflow-y: auto;
}
.device-frame {
  width: 400px;
  height: 800px;
  background: white;
  border-radius: 30px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  position: relative;
  border: 10px solid #1e293b;
}
.preview-canvas {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}
/* Ocultar barra de desplazamiento en preview */
.preview-canvas::-webkit-scrollbar {
  width: 0px;
}
</style>
