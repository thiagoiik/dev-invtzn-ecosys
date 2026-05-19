<template>
  <BuilderLayout>
    <template #actions>
      <div class="save-status-container">
        <span v-if="saveStatus === 'saved'" class="status-indicator text-success">
          ✔ Todos los cambios guardados
        </span>
        <span v-else-if="saveStatus === 'saving'" class="status-indicator text-warning animate-pulse">
          ◌ Guardando cambios de forma segura...
        </span>
        <span v-else-if="saveStatus === 'unsaved'" class="status-indicator text-info">
          ● Cambios sin guardar
        </span>
        <span v-else-if="saveStatus === 'error'" class="status-indicator text-error">
          ❌ Error al guardar en base de datos
        </span>
      </div>
    </template>

    <div class="studio-container">
      <!-- PANEL IZQUIERDO: CONTROLES -->
      <aside class="control-panel">
        <div class="panel-header">
          <h3>Ajustes de Diseño</h3>
        </div>

        <!-- TABS HEADER -->
        <div class="tabs-header">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'cover' }" 
            @click="activeTab = 'cover'"
          >
            🌅 Portada
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'rsvp' }" 
            @click="activeTab = 'rsvp'"
          >
            ✉ RSVP
          </button>
        </div>
        
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          Cargando configuración...
        </div>
        
        <form v-else class="config-form" @submit.prevent>
          <!-- TAB PORTADA -->
          <div v-if="activeTab === 'cover'" class="tab-content fade-in">
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
            
            <div class="form-group">
              <label>Color del Título</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.cover.titleColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.cover.titleColor }}</span>
              </div>
            </div>
          </div>
          
          <!-- TAB RSVP -->
          <div v-if="activeTab === 'rsvp'" class="tab-content fade-in">
            <div class="form-group">
              <label>Color Fondo RSVP</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.rsvp.bgColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.rsvp.bgColor }}</span>
              </div>
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
import { ref, onMounted, watch } from 'vue';
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
const saveStatus = ref('saved'); // 'saved', 'unsaved', 'saving', 'error'
const activeTab = ref('cover'); // 'cover', 'rsvp'

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

// Mecanismo de Auto-guardado reactivo (Debounce 2000ms)
let saveTimeout = null;

watch(localConfig, () => {
  if (loading.value) return; // Evitar disparar auto-guardado en carga inicial
  
  saveStatus.value = 'unsaved';
  
  if (saveTimeout) clearTimeout(saveTimeout);
  
  saveTimeout = setTimeout(async () => {
    saveStatus.value = 'saving';
    try {
      await builderService.saveCustomData(deploymentId, localConfig.value);
      saveStatus.value = 'saved';
    } catch (error) {
      console.error("Auto-save error:", error);
      saveStatus.value = 'error';
    }
  }, 2000);
}, { deep: true });
</script>

<style scoped>
.save-status-container {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  font-weight: bold;
}
.status-indicator {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}
.text-success {
  color: #10b981;
}
.text-warning {
  color: #f59e0b;
}
.text-info {
  color: #38bdf8;
}
.text-error {
  color: #f43f5e;
}

.studio-container {
  display: flex;
  width: 100%;
  height: 100%;
}

/* Panel de Controles */
.control-panel {
  width: 380px;
  background: #1e293b;
  color: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #334155;
  box-shadow: 10px 0 30px -10px rgba(0, 0, 0, 0.3);
  z-index: 10;
}
.panel-header {
  padding: 1.5rem 2rem 0.75rem 2rem;
}
.panel-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #f1f5f9;
}

/* Tabs */
.tabs-header {
  display: flex;
  background: #0f172a;
  padding: 0.25rem;
  border-radius: 10px;
  margin: 0.5rem 1.5rem 1.5rem 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.tab-btn {
  flex: 1;
  padding: 0.6rem 0.75rem;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 800;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}
.tab-btn:hover {
  color: #f1f5f9;
}
.tab-btn.active {
  background: #334155;
  color: #ffffff;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.config-form {
  flex: 1;
  padding: 0 2rem 2rem 2rem;
  overflow-y: auto;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Animaciones */
.fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}
.form-group input[type="text"],
.form-group input[type="url"] {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}
.form-group input:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
}

/* Color Picker Premium */
.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #0f172a;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid #334155;
}
.color-input {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 32px;
  height: 32px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}
.color-input::-webkit-color-swatch {
  border-radius: 50%;
  border: 2px solid #334155;
}
.color-input::-moz-color-swatch {
  border-radius: 50%;
  border: 2px solid #334155;
}
.color-value {
  font-family: monospace;
  font-size: 0.9rem;
  color: #e2e8f0;
  font-weight: bold;
}

/* Loader */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #64748b;
  font-size: 0.9rem;
  gap: 1rem;
}
.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #334155;
  border-top-color: #38bdf8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
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
  background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 0);
  background-size: 24px 24px;
}
.device-frame {
  width: 380px;
  height: 760px;
  background: white;
  border-radius: 40px;
  box-shadow: 0 25px 70px -10px rgba(0, 0, 0, 0.7);
  overflow: hidden;
  position: relative;
  border: 12px solid #334155;
  outline: 1px solid rgba(255, 255, 255, 0.05);
}
.preview-canvas {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}
.preview-canvas::-webkit-scrollbar {
  width: 0px;
}
</style>
