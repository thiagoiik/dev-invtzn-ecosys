<template>
  <BuilderLayout>
    <template #actions>
      <div class="save-status-container flex items-center gap-4">
        <span v-if="saveStatus === 'saved'" class="status-indicator text-emerald-400 text-xs font-bold bg-slate-900/60 px-3 py-1.5 rounded-lg border border-white/5">
          ✔ Guardado
        </span>
        <span v-else-if="saveStatus === 'saving'" class="status-indicator text-amber-400 animate-pulse text-xs font-bold bg-slate-900/60 px-3 py-1.5 rounded-lg border border-white/5">
          ◌ Guardando...
        </span>
        <span v-else-if="saveStatus === 'unsaved'" class="status-indicator text-sky-400 text-xs font-bold bg-slate-900/60 px-3 py-1.5 rounded-lg border border-white/5">
          ● Cambios sin guardar
        </span>
        <span v-else-if="saveStatus === 'error'" class="status-indicator text-rose-500 text-xs font-bold bg-slate-900/60 px-3 py-1.5 rounded-lg border border-white/5">
          ❌ Error al guardar
        </span>

        <button 
          v-if="deploymentSlug"
          @click="openLiveDemo" 
          type="button"
          class="btn btn-sm bg-slate-800 hover:bg-slate-700 text-white font-bold px-4 py-2 rounded-xl border border-slate-700/60 shadow-md transition-all flex items-center gap-1.5"
        >
          👀 Vista Previa
        </button>

        <button 
          @click="saveAllData" 
          class="btn btn-sm bg-primary hover:bg-primary-hover text-white font-bold px-4 py-2 rounded-xl shadow-md transition-all"
          :disabled="saveStatus === 'saving'"
        >
          💾 Guardar
        </button>
      </div>
    </template>

    <div class="form-view-container w-full overflow-y-auto px-4 py-8 bg-slate-900 flex justify-center min-h-screen">
      <div class="max-w-[640px] w-full bg-slate-800 text-white rounded-3xl shadow-xl border border-slate-700/60 overflow-hidden flex flex-col">
        <!-- Card Header -->
        <div class="p-6 border-b border-slate-700/60 bg-slate-800/50 flex flex-col gap-2">
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-black tracking-tight text-white">Datos de la Invitación</h2>
            <span :class="[
              'badge text-[10px] font-extrabold px-3 py-1.5 rounded-lg uppercase border-none tracking-wider',
              deploymentStatus === 'LIVE' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'
            ]">
              {{ deploymentStatus === 'LIVE' ? '🟢 En Vivo' : '🧪 Borrador' }}
            </span>
          </div>
          <p class="text-xs text-slate-400">Completa el formulario para actualizar el contenido de tu invitación digital.</p>
        </div>

        <div v-if="loading" class="flex flex-col items-center justify-center p-12 gap-3 text-slate-400">
          <div class="w-8 h-8 border-4 border-slate-700 border-t-sky-400 rounded-full animate-spin"></div>
          Cargando configuración...
        </div>

        <form v-else @submit.prevent="saveAllData" class="p-8 space-y-8">
          
          <!-- SECTION 1: COVER -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">🌅 Portada de la Invitación</h3>
            
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
            
            <div class="grid grid-cols-2 gap-4">
              <div class="form-group">
                <label>Color del Título</label>
                <div class="color-picker-wrapper">
                  <input v-model="localConfig.cover.titleColor" type="color" class="color-input" />
                  <span class="color-value font-mono text-xs">{{ localConfig.cover.titleColor }}</span>
                </div>
              </div>

              <div class="form-group">
                <label>Tipo de Letra</label>
                <select v-model="localConfig.cover.fontFamily" class="select-input">
                  <option value="serif">Serif (Por defecto)</option>
                  <option value="'Playfair Display', serif">Playfair Display</option>
                  <option value="'Great Vibes', cursive">Great Vibes (Manuscrita)</option>
                  <option value="'Montserrat', sans-serif">Montserrat (Moderna)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- SECTION 2: RSVP -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">✉ Confirmación de Asistencia (RSVP)</h3>

            <div class="form-group">
              <label>Título Sección RSVP</label>
              <input v-model="localConfig.rsvp.title" type="text" placeholder="Ej: Confirma tu Asistencia" />
            </div>

            <div class="form-group">
              <label>Subtítulo RSVP</label>
              <input v-model="localConfig.rsvp.subtitle" type="text" placeholder="Ej: Nos encantaría contar con tu presencia." />
            </div>

            <div class="form-group">
              <label>WhatsApp de Confirmación</label>
              <input v-model="localConfig.rsvp.whatsappPhone" type="tel" placeholder="Ej. +5215512345678" />
              <p class="text-[10px] text-slate-400 leading-normal">
                Número de WhatsApp a donde llegarán las confirmaciones directas de asistencia.
              </p>
            </div>
          </div>

          <!-- SECTION 3: COUNTDOWN TIMER (Cuenta Regresiva) -->
          <div v-if="localConfig.has_timer" class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">🕰️ Cuenta Regresiva</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form-group">
                <label>Título de la Cuenta Regresiva</label>
                <input v-model="localConfig.timer.title" type="text" placeholder="Ej: Cuenta Regresiva" />
              </div>
              <div class="form-group">
                <label>Fecha y Hora del Evento</label>
                <input v-model="localConfig.timer.targetDate" type="datetime-local" class="datetime-input" />
              </div>
            </div>
          </div>

          <!-- SECTION 4: TIMELINE (Cronograma / Itinerario) -->
          <div v-if="localConfig.has_timeline" class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">📅 Cronograma (Itinerario)</h3>
            <div class="space-y-4">
              <div class="form-group">
                <label>Título de la Sección</label>
                <input v-model="localConfig.timeline.title" type="text" placeholder="Ej: Cronograma del Evento" />
              </div>

              <div v-for="(item, idx) in localConfig.timeline.schedule" :key="idx" class="p-4 bg-slate-900/60 rounded-2xl border border-slate-700/50 space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-xs font-bold text-sky-400">Evento #{{ idx + 1 }}</span>
                  <button type="button" @click="removeScheduleItem(idx)" class="text-rose-500 hover:text-rose-400 text-xs font-bold">🗑️ Eliminar</button>
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div class="form-group">
                    <label>Hora</label>
                    <input v-model="item.time" type="text" placeholder="Ej: 18:00" class="compact-input" />
                  </div>
                  <div class="form-group">
                    <label>Icono (Emoji)</label>
                    <input v-model="item.icon" type="text" placeholder="💍" class="compact-input text-center" />
                  </div>
                </div>

                <div class="form-group">
                  <label>Título del Evento</label>
                  <input v-model="item.title" type="text" placeholder="Ej: Ceremonia de bodas" class="compact-input" />
                </div>

                <div class="form-group">
                  <label>Descripción</label>
                  <textarea v-model="item.description" placeholder="Ej: En la capilla principal..." class="compact-textarea"></textarea>
                </div>
              </div>

              <button type="button" @click="addScheduleItem" class="w-full py-2.5 border border-dashed border-slate-600 text-slate-400 hover:text-white rounded-xl text-xs font-bold transition-all">
                ➕ Añadir Nuevo Evento
              </button>
            </div>
          </div>

          <!-- SECTION 5: MUSIC (Música de Fondo) -->
          <div v-if="localConfig.has_music" class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">🎵 Música de Fondo</h3>
            <div class="space-y-4">
              <div class="form-group">
                <label>URL del Archivo de Audio (MP3 Directo)</label>
                <input 
                  v-model="localConfig.audioUrl" 
                  type="url" 
                  placeholder="https://..." 
                  @input="syncMusic"
                />
                <span class="text-[10px] text-slate-400">Introduce la dirección URL directa a un archivo de música público en formato .mp3.</span>
              </div>
            </div>
          </div>

          <!-- SECCIÓN NUEVA: UBICACIONES Y MAPAS -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">📍 Ubicaciones del Evento</h3>
            <div class="space-y-4">
              <!-- Ceremonia -->
              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3">
                <span class="text-xs font-bold text-amber-400">⛪ Ceremonia Religiosa / Civil</span>
                <div class="form-group">
                  <label>Nombre del Lugar</label>
                  <input v-model="localConfig.locations.ceremonyName" type="text" placeholder="Ej: Parroquia de Santa María" />
                </div>
                <div class="form-group">
                  <label>Enlace de Google Maps</label>
                  <input v-model="localConfig.locations.ceremonyMapsUrl" type="url" placeholder="https://maps.google.com/..." />
                </div>
              </div>

              <!-- Recepción -->
              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3">
                <span class="text-xs font-bold text-amber-400">🥂 Recepción / Fiesta</span>
                <div class="form-group">
                  <label>Nombre del Salón / Jardín</label>
                  <input v-model="localConfig.locations.receptionName" type="text" placeholder="Ej: Jardín de Eventos Los Pinos" />
                </div>
                <div class="form-group">
                  <label>Enlace de Google Maps</label>
                  <input v-model="localConfig.locations.receptionMapsUrl" type="url" placeholder="https://maps.google.com/..." />
                </div>
              </div>
            </div>
          </div>

          <!-- SECCIÓN NUEVA: MESA DE REGALOS -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">🎁 Mesa de Regalos</h3>
            <div class="space-y-4">
              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3">
                <span class="text-xs font-bold text-amber-400">🏦 Datos de Depósito / Transferencia</span>
                <div class="grid grid-cols-2 gap-3">
                  <div class="form-group">
                    <label>Nombre del Banco</label>
                    <input v-model="localConfig.gifts.bankName" type="text" placeholder="Ej: BBVA" />
                  </div>
                  <div class="form-group">
                    <label>Titular de la Cuenta</label>
                    <input v-model="localConfig.gifts.bankOwner" type="text" placeholder="Ej: Pedro Pérez" />
                  </div>
                </div>
                <div class="form-group">
                  <label>Cuenta CLABE (18 dígitos)</label>
                  <input v-model="localConfig.gifts.clabe" type="text" placeholder="Ej: 012180000000000000" maxlength="18" />
                </div>
              </div>

              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3">
                <span class="text-xs font-bold text-amber-400">🛍️ Enlaces de Mesas Externas</span>
                <div class="form-group">
                  <label>Mesa de Regalos 1 (Amazon, Liverpool, etc.)</label>
                  <input v-model="localConfig.gifts.registryUrl1" type="url" placeholder="https://www.amazon.com.mx/baby-reg/..." />
                </div>
                <div class="form-group">
                  <label>Mesa de Regalos 2 (Opcional)</label>
                  <input v-model="localConfig.gifts.registryUrl2" type="url" placeholder="https://mesaderegalos.liverpool.com.mx/..." />
                </div>
              </div>
            </div>
          </div>

          <!-- SECCIÓN NUEVA: CÓDIGO DE VESTIMENTA -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">👗 Código de Vestimenta (Dress Code)</h3>
            <div class="space-y-4">
              <div class="form-group">
                <label>Tipo de Código de Vestimenta</label>
                <select v-model="localConfig.dressCode.type" class="select-input">
                  <option value="FORMAL">Formal</option>
                  <option value="ETIQUETA">Etiqueta (Gala)</option>
                  <option value="COCKTAIL">Cóctel</option>
                  <option value="GUAYABERA">Guayabera / Clima Cálido</option>
                  <option value="CASUAL">Casual</option>
                  <option value="PLAYA">Playa</option>
                </select>
              </div>
              <div class="form-group">
                <label>Especificaciones / Detalles Adicionales</label>
                <textarea v-model="localConfig.dressCode.details" placeholder="Ej: Traje oscuro caballeros y vestido largo damas..." class="compact-textarea"></textarea>
              </div>
            </div>
          </div>

          <!-- SECTION 6: SEO y Redes Sociales (Open Graph) -->
          <div class="space-y-4">
            <h3 class="text-sm font-black text-sky-400 uppercase tracking-widest border-b border-slate-700/50 pb-2">⚙️ Vista en Redes Sociales (WhatsApp)</h3>
            <div class="space-y-4">
              <div class="form-group">
                <label>Título para Redes Sociales (og_title)</label>
                <input v-model="localConfig.og_title" type="text" placeholder="Ej: ¡Estás invitado a nuestra boda!" />
              </div>

              <div class="form-group">
                <label>Descripción para Redes Sociales (og_description)</label>
                <input v-model="localConfig.og_description" type="text" placeholder="Ej: Acompáñanos este 25 de diciembre..." />
              </div>

              <div class="form-group">
                <label>URL de Imagen para Redes (og_image)</label>
                <input v-model="localConfig.og_image" type="url" placeholder="https://..." />
              </div>
            </div>
          </div>

          <!-- SECTION 8: COMPLETION STATUS (Client A completion checker) -->
          <div class="pt-6 border-t border-slate-700/60 space-y-4">
            <h3 class="text-sm font-black text-emerald-400 uppercase tracking-widest">✓ Finalización de Edición</h3>
            <div class="flex items-start justify-between bg-slate-900/60 p-4 rounded-2xl border border-emerald-500/20 gap-4">
              <div class="space-y-1">
                <span class="text-xs font-bold text-slate-200 block">Marcar como Edición Completada</span>
                <p class="text-[10px] text-slate-400 leading-normal">
                  Al marcar la edición como completada, se removerá el botón de edición en tu panel de control, protegiendo tus datos de modificaciones accidentales. Podrás reactivarlo si es necesario.
                </p>
              </div>
              <input 
                type="checkbox" 
                v-model="localConfig.is_catalog_complete" 
                class="switch-input flex-shrink-0"
              />
            </div>
          </div>

          <!-- Form Actions Footer -->
          <div class="pt-6 border-t border-slate-700/60 flex justify-end gap-3">
            <button 
              type="button" 
              @click="router.push('/dashboard')" 
              class="btn btn-ghost text-slate-400 hover:text-white font-bold rounded-xl px-5 text-sm"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn btn-primary rounded-xl px-8 font-black text-sm shadow-md"
              :disabled="saveStatus === 'saving'"
            >
              {{ saveStatus === 'saving' ? 'Guardando...' : 'Guardar y Salir' }}
            </button>
          </div>

        </form>
      </div>
    </div>

    <!-- Modal de Upgrade (Glassmorphism) -->
    <UpgradeModal 
      v-if="showUpgradeModal" 
      @close="showUpgradeModal = false" 
      @select-tier="handleTierSelection" 
    />
  </BuilderLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import BuilderLayout from '@/layouts/BuilderLayout.vue';
import { builderService } from '@/modules/builder/services/builderService';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const deploymentId = route.params.id;

const loading = ref(true);
const saveStatus = ref('saved'); // 'saved', 'unsaved', 'saving', 'error'
const showUpgradeModal = ref(false);

const deploymentStatus = ref('DRAFT');
const deploymentSlug = ref('');

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
    subtitle: 'Nos encantaría contar con tu presencia.',
    whatsappPhone: ''
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
      { time: '18:30', title: 'Cóctel de Bienvenida', description: 'Bebidas selectas y bocadillos en la terraza.', icon: '🥂' }
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
  og_image: '',
  envelope_type: null,
  envelope: null,
  is_catalog_complete: false,
  
  // Estructuras de datos para bodas
  locations: {
    ceremonyName: '',
    ceremonyMapsUrl: '',
    receptionName: '',
    receptionMapsUrl: ''
  },
  gifts: {
    bankName: '',
    bankOwner: '',
    clabe: '',
    registryUrl1: '',
    registryUrl2: ''
  },
  dressCode: {
    type: 'FORMAL',
    details: ''
  }
});

// Acciones removidas ya que no hay modales de upgrade en el formulario del cliente final

const syncMusic = () => {
  if (!localConfig.value.music) {
    localConfig.value.music = {};
  }
  localConfig.value.music.has_music = localConfig.value.has_music;
  localConfig.value.music.audioUrl = localConfig.value.audioUrl;
};

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
  saveStatus.value = 'unsaved';
};

const removeScheduleItem = (idx) => {
  localConfig.value.timeline.schedule.splice(idx, 1);
  saveStatus.value = 'unsaved';
};

const loadData = async () => {
  loading.value = true;
  try {
    const res = await builderService.getDeployment(deploymentId);
    if (res.data) {
      deploymentStatus.value = res.data.status || 'DRAFT';
      deploymentSlug.value = res.data.slug || '';
      
      const custom = res.data.custom_data;
      if (custom && Object.keys(custom).length > 0) {
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
        if (custom.locations) {
          localConfig.value.locations = { ...localConfig.value.locations, ...custom.locations };
        }
        if (custom.gifts) {
          localConfig.value.gifts = { ...localConfig.value.gifts, ...custom.gifts };
        }
        if (custom.dressCode) {
          localConfig.value.dressCode = { ...localConfig.value.dressCode, ...custom.dressCode };
        }
        
        localConfig.value.has_timer = custom.has_timer ?? false;
        localConfig.value.has_timeline = custom.has_timeline ?? false;
        localConfig.value.has_music = custom.has_music ?? false;
        localConfig.value.audioUrl = custom.audioUrl ?? '';
        localConfig.value.og_title = custom.og_title ?? '';
        localConfig.value.og_description = custom.og_description ?? '';
        localConfig.value.og_image = custom.og_image ?? '';
        localConfig.value.envelope_type = custom.envelope_type ?? null;
        localConfig.value.is_catalog_complete = custom.is_catalog_complete ?? false;
      }
    }
  } catch (error) {
    toast.error('Error al cargar la invitación');
  } finally {
    loading.value = false;
  }
};

const saveAllData = async () => {
  saveStatus.value = 'saving';
  try {
    await builderService.saveCustomData(deploymentId, localConfig.value);
    saveStatus.value = 'saved';
    toast.success('¡Cambios guardados con éxito!');
  } catch (error) {
    saveStatus.value = 'error';
    toast.error('No se pudieron guardar los cambios.');
  }
};

const openLiveDemo = () => {
  if (deploymentSlug.value) {
    window.open(`/i/${deploymentSlug.value}`, '_blank');
  }
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.form-group label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}
.form-group input[type="text"],
.form-group input[type="url"],
.form-group input[type="tel"],
.form-group input[type="datetime-local"] {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  width: 100%;
}
.form-group input:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15);
}

.select-input {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  width: 100%;
}
.select-input:focus {
  outline: none;
  border-color: #38bdf8;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #0f172a;
  padding: 0.5rem 0.75rem;
  border-radius: 12px;
  border: 1px solid #334155;
}
.color-input {
  -webkit-appearance: none;
  appearance: none;
  width: 28px;
  height: 28px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}
.color-input::-webkit-color-swatch {
  border-radius: 50%;
  border: 2px solid #334155;
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

.hue-range {
  width: 100%;
  cursor: pointer;
  height: 6px;
  background: #334155;
  border-radius: 3px;
  outline: none;
}
.color-hue-preview-bar {
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

.compact-input {
  background: #0f172a;
  border: 1px solid #334155 !important;
  color: white;
  padding: 0.6rem 0.85rem !important;
  border-radius: 10px !important;
  font-size: 0.85rem !important;
  width: 100%;
}
.compact-textarea {
  background: #0f172a;
  border: 1px solid #334155;
  color: white;
  padding: 0.6rem 0.85rem;
  border-radius: 10px;
  font-size: 0.85rem;
  width: 100%;
  height: 64px;
  resize: vertical;
}
.compact-input:focus,
.compact-textarea:focus {
  outline: none;
  border-color: #38bdf8;
}
</style>
