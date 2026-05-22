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

        <!-- TABS GRID -->
        <div class="tabs-grid">
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
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'timer' }" 
            @click="activeTab = 'timer'"
          >
            🕰️ Contador
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'timeline' }" 
            @click="activeTab = 'timeline'"
          >
            📅 Cronograma
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'music' }" 
            @click="activeTab = 'music'"
          >
            🎵 Música
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'theme' }" 
            @click="activeTab = 'theme'"
          >
            🎨 Estilos
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'og' }" 
            @click="activeTab = 'og'"
          >
            ⚙️ SEO/OG
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
              <label>Etiqueta Superior</label>
              <input v-model="localConfig.cover.headerLabel" type="text" placeholder="Ej: Nuestra Invitación" />
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

            <div class="form-group">
              <label>Tipo de Letra (Título)</label>
              <select v-model="localConfig.cover.fontFamily" class="select-input">
                <option value="serif">Elegante Serif (Por defecto)</option>
                <option value="'Playfair Display', serif">Playfair Display</option>
                <option value="'Great Vibes', cursive">Great Vibes (Manuscrita)</option>
                <option value="'Montserrat', sans-serif">Montserrat (Moderna)</option>
              </select>
            </div>
          </div>
          
          <!-- TAB RSVP -->
          <div v-if="activeTab === 'rsvp'" class="tab-content fade-in">
            <div class="form-group">
              <label>Título Sección RSVP</label>
              <input v-model="localConfig.rsvp.title" type="text" placeholder="Ej: Confirma tu Asistencia" />
            </div>

            <div class="form-group">
              <label>Subtítulo RSVP</label>
              <input v-model="localConfig.rsvp.subtitle" type="text" placeholder="Ej: Nos encantaría contar con tu presencia." />
            </div>

            <div class="form-group">
              <label>Color Fondo RSVP</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.rsvp.bgColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.rsvp.bgColor }}</span>
              </div>
            </div>
          </div>

          <!-- TAB CONTADOR -->
          <div v-if="activeTab === 'timer'" class="tab-content fade-in">
            <!-- Feature Switch with Lock Option -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  🕰️ Habilitar Contador
                  <span v-if="!allowedFeatures.countdown_timer" class="badge-lock">PRO 👑</span>
                </span>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_timer" 
                  :disabled="!allowedFeatures.countdown_timer"
                  class="switch-input"
                />
              </label>
            </div>

            <!-- Upgrade Block Overlay -->
            <div v-if="!allowedFeatures.countdown_timer" class="upgrade-block-overlay">
              <div class="lock-icon">🔒</div>
              <p class="lock-text">El bloque de Cuenta Regresiva requiere un plan <strong>Standard</strong> o superior.</p>
              <router-link to="/catalog" class="upgrade-btn">Mejorar Plan</router-link>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !localConfig.has_timer || !allowedFeatures.countdown_timer }" class="space-y-4">
              <div class="form-group">
                <label>Título de Cuenta Regresiva</label>
                <input 
                  v-model="localConfig.timer.title" 
                  type="text" 
                  placeholder="Ej: Cuenta Regresiva" 
                  :disabled="!localConfig.has_timer || !allowedFeatures.countdown_timer"
                />
              </div>

              <div class="form-group">
                <label>Fecha y Hora de Destino</label>
                <input 
                  v-model="localConfig.timer.targetDate" 
                  type="datetime-local" 
                  :disabled="!localConfig.has_timer || !allowedFeatures.countdown_timer"
                  class="datetime-input"
                />
              </div>
            </div>
          </div>

          <!-- TAB CRONOGRAMA -->
          <div v-if="activeTab === 'timeline'" class="tab-content fade-in">
            <!-- Feature Switch with Lock Option -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  📅 Habilitar Cronograma
                  <span v-if="!allowedFeatures.timeline" class="badge-lock">PREMIUM 👑</span>
                </span>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_timeline" 
                  :disabled="!allowedFeatures.timeline"
                  class="switch-input"
                />
              </label>
            </div>

            <!-- Upgrade Block Overlay -->
            <div v-if="!allowedFeatures.timeline" class="upgrade-block-overlay">
              <div class="lock-icon">🔒</div>
              <p class="lock-text">El bloque de Itinerario requiere un plan <strong>Premium</strong>.</p>
              <router-link to="/catalog" class="upgrade-btn">Mejorar Plan</router-link>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !localConfig.has_timeline || !allowedFeatures.timeline }" class="space-y-4">
              <div class="form-group">
                <label>Título de la Sección</label>
                <input 
                  v-model="localConfig.timeline.title" 
                  type="text" 
                  placeholder="Ej: Cronograma del Evento" 
                  :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                />
              </div>

              <!-- List of schedule items -->
              <div class="space-y-2">
                <label class="section-subtitle">Eventos del Itinerario</label>
                <div v-for="(item, idx) in localConfig.timeline.schedule" :key="idx" class="schedule-item-card">
                  <div class="schedule-header">
                    <span class="item-number">Evento #{{ idx + 1 }}</span>
                    <button 
                      type="button" 
                      @click="removeScheduleItem(idx)" 
                      class="remove-item-btn"
                      title="Eliminar Evento"
                      :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                    >
                      🗑️
                    </button>
                  </div>
                  <div class="grid grid-cols-2 gap-2">
                    <div class="form-group">
                      <label>Hora</label>
                      <input 
                        v-model="item.time" 
                        type="text" 
                        placeholder="17:00" 
                        :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                        class="compact-input"
                      />
                    </div>
                    <div class="form-group">
                      <label>Icono</label>
                      <input 
                        v-model="item.icon" 
                        type="text" 
                        placeholder="💍" 
                        :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                        class="compact-input text-center"
                      />
                    </div>
                  </div>
                  <div class="form-group mt-2">
                    <label>Título del Evento</label>
                    <input 
                      v-model="item.title" 
                      type="text" 
                      placeholder="Ej: Ceremonia" 
                      :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                      class="compact-input"
                    />
                  </div>
                  <div class="form-group mt-2">
                    <label>Descripción</label>
                    <textarea 
                      v-model="item.description" 
                      placeholder="Breve descripción..." 
                      :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                      class="compact-textarea"
                    ></textarea>
                  </div>
                </div>

                <button 
                  type="button" 
                  @click="addScheduleItem" 
                  class="add-item-btn mt-2"
                  :disabled="!localConfig.has_timeline || !allowedFeatures.timeline"
                >
                  ➕ Añadir Nuevo Evento
                </button>
              </div>
            </div>
          </div>

          <!-- TAB MÚSICA -->
          <div v-if="activeTab === 'music'" class="tab-content fade-in">
            <!-- Feature Switch with Lock Option -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  🎵 Habilitar Música de Fondo
                  <span v-if="!allowedFeatures.background_music" class="badge-lock">STANDARD 👑</span>
                </span>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_music" 
                  :disabled="!allowedFeatures.background_music"
                  class="switch-input"
                  @change="syncMusicFlag"
                />
              </label>
            </div>

            <!-- Upgrade Block Overlay -->
            <div v-if="!allowedFeatures.background_music" class="upgrade-block-overlay">
              <div class="lock-icon">🔒</div>
              <p class="lock-text">La Música de Fondo requiere un plan <strong>Standard</strong> o superior.</p>
              <router-link to="/catalog" class="upgrade-btn">Mejorar Plan</router-link>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !localConfig.has_music || !allowedFeatures.background_music }" class="space-y-4">
              <div class="form-group">
                <label>URL del Archivo de Audio (MP3)</label>
                <input 
                  v-model="localConfig.audioUrl" 
                  type="url" 
                  placeholder="https://..." 
                  :disabled="!localConfig.has_music || !allowedFeatures.background_music"
                  @input="syncAudioUrl"
                />
                <span class="help-text">Ingresa una URL directa a un archivo MP3 público.</span>
              </div>
            </div>
          </div>

          <!-- TAB ESTILO -->
          <div v-if="activeTab === 'theme'" class="tab-content fade-in">
            <!-- Feature Switch with Lock Option -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  🎨 Paleta de Color Premium
                  <span v-if="!allowedFeatures.custom_theme" class="badge-lock">STANDARD 👑</span>
                </span>
              </label>
            </div>

            <!-- Upgrade Block Overlay -->
            <div v-if="!allowedFeatures.custom_theme" class="upgrade-block-overlay">
              <div class="lock-icon">🔒</div>
              <p class="lock-text">La paleta de color personalizada requiere un plan <strong>Standard</strong> o superior.</p>
              <router-link to="/catalog" class="upgrade-btn">Mejorar Plan</router-link>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !allowedFeatures.custom_theme }" class="space-y-4">
              <div class="form-group">
                <label class="flex justify-between">
                  <span>Tono de Color (HUE)</span>
                  <span class="font-bold font-mono">{{ localConfig.theme.hue }}°</span>
                </label>
                <input 
                  type="range" 
                  min="0" 
                  max="360" 
                  v-model.number="localConfig.theme.hue" 
                  :disabled="!allowedFeatures.custom_theme"
                  class="hue-range"
                />
                
                <!-- Color Preview bar -->
                <div class="color-hue-preview-bar"></div>
                
                <!-- Single Color Preview circle -->
                <div class="flex items-center gap-3 mt-2">
                  <div 
                    class="w-8 h-8 rounded-full border border-slate-700 shadow-md"
                    :style="{ backgroundColor: `hsl(${localConfig.theme.hue}, 80%, 50%)` }"
                  ></div>
                  <span class="text-xs text-slate-400">Color principal de botones y detalles</span>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB SEO/OG -->
          <div v-if="activeTab === 'og'" class="tab-content fade-in">
            <!-- Feature Switch with Lock Option -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  ⚙️ Metadatos Open Graph
                  <span v-if="!allowedFeatures.custom_og" class="badge-lock">PREMIUM 👑</span>
                </span>
              </label>
            </div>

            <!-- Upgrade Block Overlay -->
            <div v-if="!allowedFeatures.custom_og" class="upgrade-block-overlay">
              <div class="lock-icon">🔒</div>
              <p class="lock-text">La personalización de metadatos para redes sociales requiere un plan <strong>Premium</strong>.</p>
              <router-link to="/catalog" class="upgrade-btn">Mejorar Plan</router-link>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !allowedFeatures.custom_og }" class="space-y-4">
              <div class="form-group">
                <label>Título para Redes Sociales (og_title)</label>
                <input 
                  v-model="localConfig.og_title" 
                  type="text" 
                  placeholder="Ej: Te invitamos a nuestra boda - Ana & Luis" 
                  :disabled="!allowedFeatures.custom_og"
                />
                <span class="help-text">Título que aparecerá al compartir la invitación por WhatsApp, Facebook, etc.</span>
              </div>

              <div class="form-group">
                <label>Descripción para Redes Sociales (og_description)</label>
                <input 
                  v-model="localConfig.og_description" 
                  type="text" 
                  placeholder="Ej: El 25 de diciembre celebraremos nuestra unión. ¡Mira todos los detalles aquí!" 
                  :disabled="!allowedFeatures.custom_og"
                />
                <span class="help-text">Breve párrafo descriptivo bajo el título en redes.</span>
              </div>

              <div class="form-group">
                <label>URL de Imagen para Redes (og_image)</label>
                <input 
                  v-model="localConfig.og_image" 
                  type="url" 
                  placeholder="https://..." 
                  :disabled="!allowedFeatures.custom_og"
                />
                <span class="help-text">URL de la imagen que se mostrará al compartir. Debe ser cuadrada u horizontal.</span>
              </div>
            </div>
          </div>
        </form>
      </aside>

      <!-- PANEL DERECHO: LIVE PREVIEW -->
      <section class="preview-panel">
        <div class="device-frame">
          <!-- Inyectamos los componentes del Engine en tiempo real -->
          <div v-if="!loading" class="preview-canvas">
            <RenderEngineMaster 
              :status="deploymentStatus" 
              :customData="localConfig" 
              :slug="deploymentSlug" 
              :deploymentId="deploymentId"
            />
          </div>
          <div v-else class="loading-state">
            <div class="loading-spinner"></div>
            Cargando vista previa...
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
import RenderEngineMaster from '@/modules/engine/components/RenderEngineMaster.vue';

const route = useRoute();
const toast = useToast();
const deploymentId = route.params.id;

const loading = ref(true);
const saveStatus = ref('saved'); // 'saved', 'unsaved', 'saving', 'error'
const activeTab = ref('cover'); // 'cover', 'rsvp', 'timer', 'timeline', 'music', 'theme', 'og'

const allowedFeatures = ref({
  background_music: false,
  custom_audio_url: false,
  countdown_timer: false,
  timeline: false,
  custom_theme: false,
  custom_og: false,
});
const deploymentSlug = ref('');
const deploymentStatus = ref('DRAFT');

// Estructura por defecto en caso de que esté vacío
const localConfig = ref({
  cover: {
    title: '',
    subtitle: '',
    date: '',
    coverPhoto: '',
    titleColor: '#ffffff',
    headerLabel: 'Nuestra Invitación',
    fontFamily: 'serif'
  },
  rsvp: {
    bgColor: '#f8fafc',
    btnColor: '#3b82f6',
    title: 'Confirma tu Asistencia',
    subtitle: 'Nos encantaría contar con tu presencia.'
  },
  has_timer: false,
  timer: {
    title: 'Cuenta Regresiva',
    targetDate: '2026-12-25T18:00:00'
  },
  has_timeline: false,
  timeline: {
    title: 'Cronograma del Evento',
    schedule: [
      { time: '17:00', title: 'Ceremonia de Boda', description: 'Bajo el gran árbol del jardín principal.', icon: '💍' },
      { time: '18:30', title: 'Cóctel de Bienvenida', description: 'Bebidas selectas y bocadillos en la terraza.', icon: '🥂' },
      { time: '20:00', title: 'Banquete & Cena', description: 'Cena de gala de 3 tiempos en el salón majestuoso.', icon: '🍽️' },
      { time: '22:00', title: 'Apertura de Pista', description: '¡Baile, diversión y sorpresas hasta el amanecer!', icon: '🕺' }
    ]
  },
  has_music: false,
  audioUrl: '',
  music: {
    audioUrl: '',
    has_music: false
  },
  theme: {
    hue: 38,
    saturation: '80%',
    lightness: '50%'
  },
  og_title: '',
  og_description: '',
  og_image: ''
});

onMounted(async () => {
  try {
    const res = await builderService.getDeployment(deploymentId);
    if (res.data) {
      deploymentSlug.value = res.data.slug || '';
      deploymentStatus.value = res.data.status || 'DRAFT';
      if (res.data.allowed_features) {
        allowedFeatures.value = res.data.allowed_features;
      }
      
      const custom = res.data.custom_data;
      if (custom && Object.keys(custom).length > 0) {
        // Fusionar datos existentes para no romper la reactividad profunda
        localConfig.value.cover = { ...localConfig.value.cover, ...(custom.cover || {}) };
        localConfig.value.rsvp = { ...localConfig.value.rsvp, ...(custom.rsvp || {}) };
        
        if (custom.timer) {
          localConfig.value.timer = { ...localConfig.value.timer, ...custom.timer };
        }
        if (custom.timeline) {
          localConfig.value.timeline = { ...localConfig.value.timeline, ...custom.timeline };
        }
        if (custom.music) {
          localConfig.value.music = { ...localConfig.value.music, ...custom.music };
        }
        if (custom.theme) {
          localConfig.value.theme = { ...localConfig.value.theme, ...custom.theme };
        }
        
        // Copiar otros campos planos
        localConfig.value.has_timer = custom.has_timer ?? false;
        localConfig.value.has_timeline = custom.has_timeline ?? false;
        localConfig.value.has_music = custom.has_music ?? false;
        localConfig.value.audioUrl = custom.audioUrl ?? '';
        localConfig.value.og_title = custom.og_title ?? '';
        localConfig.value.og_description = custom.og_description ?? '';
        localConfig.value.og_image = custom.og_image ?? '';
      }
    }
  } catch (error) {
    toast.error('Error al cargar la configuración');
  } finally {
    loading.value = false;
  }
});

const addScheduleItem = () => {
  if (!localConfig.value.timeline.schedule) {
    localConfig.value.timeline.schedule = [];
  }
  localConfig.value.timeline.schedule.push({
    time: '18:00',
    title: 'Nuevo Evento',
    description: 'Descripción del evento.',
    icon: '✨'
  });
};

const removeScheduleItem = (idx) => {
  localConfig.value.timeline.schedule.splice(idx, 1);
};

const syncMusicFlag = () => {
  if (!localConfig.value.music) {
    localConfig.value.music = {};
  }
  localConfig.value.music.has_music = localConfig.value.has_music;
};

const syncAudioUrl = () => {
  if (!localConfig.value.music) {
    localConfig.value.music = {};
  }
  localConfig.value.music.audioUrl = localConfig.value.audioUrl;
};

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

/* Tabs Grid */
.tabs-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.35rem;
  background: #0f172a;
  padding: 0.35rem;
  border-radius: 10px;
  margin: 0.5rem 1.5rem 1.5rem 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.tab-btn {
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
.form-group input[type="url"],
.form-group input[type="datetime-local"] {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  width: 100%;
}
.form-group input:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
}

/* Select Input */
.select-input {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  width: 100%;
}
.select-input:focus {
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

/* Switch Container */
.switch-container {
  background: #0f172a;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border: 1px solid #334155;
}
.switch-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #94a3b8;
  cursor: pointer;
}
.switch-input {
  appearance: none;
  background-color: #334155;
  width: 36px;
  height: 20px;
  border-radius: 10px;
  position: relative;
  outline: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.switch-input:checked {
  background-color: #38bdf8;
}
.switch-input::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: white;
  top: 2px;
  left: 2px;
  transition: transform 0.2s ease;
}
.switch-input:checked::before {
  transform: translateX(16px);
}
.switch-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Badge Lock */
.badge-lock {
  font-size: 0.65rem;
  font-weight: 900;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  letter-spacing: 0.05em;
  display: inline-flex;
  align-items: center;
}

/* Upgrade Block Overlay */
.upgrade-block-overlay {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.lock-icon {
  font-size: 2rem;
}
.lock-text {
  font-size: 0.85rem;
  color: #cbd5e1;
  line-height: 1.4;
  margin: 0;
}
.lock-text strong {
  color: #f59e0b;
}
.upgrade-btn {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  font-weight: 800;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.85rem;
  transition: all 0.2s ease;
  text-decoration: none;
  box-shadow: 0 4px 6px rgba(217, 119, 6, 0.2);
}
.upgrade-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 10px rgba(217, 119, 6, 0.3);
}

/* Schedule Items styling */
.section-subtitle {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #94a3b8;
  display: block;
  margin-bottom: 0.5rem;
}
.schedule-item-card {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
}
.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.item-number {
  font-size: 0.75rem;
  font-weight: 800;
  color: #38bdf8;
  text-transform: uppercase;
}
.remove-item-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.2rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}
.remove-item-btn:hover:not(:disabled) {
  background-color: rgba(244, 63, 94, 0.1);
}
.compact-input {
  background: #1e293b;
  border: 1px solid #334155 !important;
  color: white;
  padding: 0.5rem 0.75rem !important;
  border-radius: 6px !important;
  font-size: 0.85rem !important;
  width: 100%;
}
.compact-textarea {
  background: #1e293b;
  border: 1px solid #334155;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  width: 100%;
  height: 60px;
  resize: vertical;
}
.compact-input:focus,
.compact-textarea:focus {
  outline: none;
  border-color: #38bdf8;
}
.add-item-btn {
  width: 100%;
  background: transparent;
  border: 1px dashed #334155;
  color: #94a3b8;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.add-item-btn:hover:not(:disabled) {
  border-color: #38bdf8;
  color: white;
  background-color: rgba(56, 189, 248, 0.05);
}

/* Hue Range and Preview bar */
.hue-range {
  width: 100%;
  cursor: pointer;
  height: 6px;
  background: #334155;
  border-radius: 3px;
  outline: none;
}
.color-hue-preview-bar {
  height: 10px;
  border-radius: 5px;
  margin-top: 0.5rem;
  background: linear-gradient(to right, 
    hsl(0, 80%, 50%), 
    hsl(60, 80%, 50%), 
    hsl(120, 80%, 50%), 
    hsl(180, 80%, 50%), 
    hsl(240, 80%, 50%), 
    hsl(300, 80%, 50%), 
    hsl(360, 80%, 50%)
  );
}

.help-text {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: -0.25rem;
  line-height: 1.2;
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
