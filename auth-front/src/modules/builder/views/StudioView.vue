<template>
  <BuilderLayout>
    <template #title>
      <div class="flex items-center gap-2 text-white max-w-full">
        <span v-if="!isEditingSlug" class="font-semibold text-xs sm:text-sm md:text-base truncate max-w-[150px] md:max-w-xs cursor-pointer select-none" @dblclick="startEditingSlug" title="Doble clic para cambiar slug">
          🔗 {{ deploymentSlug }}
        </span>
        <input 
          v-else 
          v-model="editableSlug" 
          @blur="saveSlug" 
          @keyup.enter="saveSlug"
          type="text" 
          class="bg-slate-800 text-white text-[10px] sm:text-xs px-2 py-1 rounded border border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500 max-w-[120px] md:max-w-xs"
          placeholder="slug-de-la-plantilla" 
          autofocus
        />
        <button v-if="!isEditingSlug" @click="startEditingSlug" class="text-xs text-slate-400 hover:text-white transition-all" title="Editar slug">
          ✏️
        </button>
      </div>
    </template>

    <template #actions>
        <div class="save-status-container flex items-center gap-1.5 sm:gap-3">
          <!-- Badge de Estado de la Invitación -->
          <span v-if="deploymentStatus === 'LIVE'" class="badge bg-emerald-500 text-white font-bold text-[10px] sm:text-xs uppercase px-2 py-1 sm:px-3 sm:py-1.5 rounded-lg flex items-center gap-1 shadow-sm">
            🟢<span class="hidden sm:inline"> En Vivo</span>
          </span>
          <span v-else class="badge bg-amber-500 text-white font-bold text-[10px] sm:text-xs uppercase px-2 py-1 sm:px-3 sm:py-1.5 rounded-lg flex items-center gap-1 shadow-sm">
            🧪<span class="hidden sm:inline"> Borrador</span>
          </span>

          <span v-if="saveStatus === 'saved'" class="status-indicator text-success text-[10px] sm:text-xs flex items-center gap-1">
            ✔<span class="hidden md:inline"> Guardado</span>
          </span>
          <span v-else-if="saveStatus === 'saving'" class="status-indicator text-warning animate-pulse text-[10px] sm:text-xs flex items-center gap-1">
            ◌<span class="hidden md:inline"> Guardando...</span>
          </span>
          <span v-else-if="saveStatus === 'unsaved'" class="status-indicator text-info text-[10px] sm:text-xs flex items-center gap-1">
            ●<span class="hidden md:inline"> Sin guardar</span>
          </span>
          <span v-else-if="saveStatus === 'error'" class="status-indicator text-error text-[10px] sm:text-xs flex items-center gap-1">
            ❌<span class="hidden md:inline"> Error</span>
          </span>
        </div>
        
        <!-- Botón de publicar dinámico -->
        <button 
          v-if="deploymentStatus !== 'LIVE'"
          @click="handlePublishClick"
          class="btn btn-sm bg-gradient-to-r from-pink-500 to-indigo-600 hover:from-pink-600 hover:to-indigo-700 text-white font-black px-2.5 py-1.5 sm:px-4 sm:py-2 rounded-xl shadow-md transition-all flex items-center gap-1 text-[10px] sm:text-xs"
        >
          ✨<span class="hidden sm:inline"> Publicar</span>
        </button>

        <button 
          v-else-if="deploymentStatus === 'LIVE' && authStore?.role !== 'ADMIN' && authStore?.role !== 'DESIGNER'"
          @click="pauseInvitation"
          class="btn btn-sm bg-rose-600 hover:bg-rose-700 text-white font-black px-2.5 py-1.5 sm:px-4 sm:py-2 rounded-xl shadow-md transition-all flex items-center gap-1 text-[10px] sm:text-xs"
        >
          ⏸️<span class="hidden sm:inline"> Pausar</span>
        </button>

        <button 
          v-if="deploymentSlug" 
          @click="openLiveDemo" 
          class="btn btn-outline-primary px-2.5 py-1.5 sm:px-4 sm:py-2 text-[10px] sm:text-xs flex items-center gap-1"
        >
          👀<span class="hidden sm:inline"> Ver en Vivo</span><span class="inline sm:hidden"> Ver</span>
        </button>
    </template>


    <div class="studio-container relative">
      <!-- Botón Flotante para Móviles -->
      <button 
        class="mobile-preview-toggle md:hidden fixed bottom-6 right-6 z-[100] btn btn-primary shadow-2xl shadow-primary/30 rounded-full px-6 font-bold"
        @click="showMobilePreview = !showMobilePreview"
      >
        {{ showMobilePreview ? '✏️ Seguir Editando' : '👁️ Ver Vista Previa' }}
      </button>

      <!-- PANEL IZQUIERDO: CONTROLES -->
      <aside class="control-panel" :class="{ 'is-hidden-mobile': showMobilePreview }">
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
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'envelope' }" 
            @click="activeTab = 'envelope'"
          >
            ✉️ Sobre 3D
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

            <div class="form-group">
              <label>WhatsApp de Confirmación</label>
              <input v-model="localConfig.rsvp.whatsappPhone" type="tel" placeholder="Ej. +5215512345678" />
              <p class="text-[10px] text-slate-400 mt-1">Los invitados del plan básico enviarán confirmaciones directas a este número de WhatsApp.</p>
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
              <button @click="showUpgradeModal = true" class="upgrade-btn">🔓 Desbloquear con Pase Standard</button>
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
              <button @click="showUpgradeModal = true" class="upgrade-btn">🔓 Desbloquear con Pase Premium</button>
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
              <button @click="showUpgradeModal = true" class="upgrade-btn">🔓 Desbloquear con Pase Standard</button>
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
              <button @click="showUpgradeModal = true" class="upgrade-btn">🔓 Desbloquear con Pase Standard</button>
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
              <button @click="showUpgradeModal = true" class="upgrade-btn">🔓 Desbloquear con Pase Premium</button>
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

          <!-- TAB SOBRE 3D -->
          <div v-if="activeTab === 'envelope'" class="tab-content fade-in">
            <div class="form-group">
              <label>Tipo de Apertura (Sobre 3D)</label>
              <select v-model="localConfig.envelope_type" class="select-input">
                <option :value="null">Sin sobre (Apertura directa)</option>
                <option value="1">Sobre Clásico y Lacre</option>
                <option value="2">Tríptico Imperial</option>
                <option value="3">Pliegue Cruzado Origami</option>
                <option value="4">Comuerta Cyber-Neon</option>
                <option value="5">Telón de Seda Mágico</option>
              </select>
              <span class="help-text">Elige la animación de apertura que verán tus invitados al abrir la invitación digital.</span>
            </div>

            <!-- Envelope preview info -->
            <div class="envelope-info-card mt-2">
              <div class="info-icon">💡</div>
              <p class="info-text">
                Haz clic en el lacre o en la pantalla de la vista previa para interactuar con la animación del sobre. 
                Si cambias de sobre, la vista previa se reiniciará automáticamente.
              </p>
            </div>
          </div>
        </form>
      </aside>

      <!-- PANEL DERECHO: LIVE PREVIEW -->
      <section class="preview-panel" :class="{ 'is-hidden-mobile': !showMobilePreview }">
        <div class="simulator-scale-wrapper" :style="scaleStyle">
          <!-- Sombra tridimensional posterior del celular -->
          <div class="device-shadow-3d"></div>
          
          <div class="device-frame">
            <!-- Cristal frontal con reflejo sutil (detrás del bisel pero encima del canvas) -->
            <div class="device-glass-reflection"></div>
            
            <!-- Bisel físico / Marco frontal 3D con isla dinámica -->
            <div class="device-bezel-frame">
              <div class="device-island-notch">
                <div class="device-camera-lens"></div>
                <div class="device-sensor-dot"></div>
              </div>
            </div>

            <!-- Inyectamos los componentes del Engine en tiempo real -->
            <div v-if="!loading" class="preview-canvas">
              <EnvelopeWrapper v-if="activeTab === 'envelope'" :type="localConfig.envelope_type || localConfig.envelope">
                <RenderEngineMaster 
                  :status="deploymentStatus" 
                  :customData="localConfig" 
                  :slug="deploymentSlug" 
                  :deploymentId="deploymentId"
                  :isStudioMode="true"
                  @purchase="showUpgradeModal = true"
                />
              </EnvelopeWrapper>
              <RenderEngineMaster 
                v-else
                :status="deploymentStatus" 
                :customData="localConfig" 
                :slug="deploymentSlug" 
                :deploymentId="deploymentId"
                :isStudioMode="true"
                @purchase="showUpgradeModal = true"
              />
            </div>
            <div v-else class="loading-state">
              <div class="loading-spinner"></div>
              Cargando vista previa...
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Modal de Upgrade (Glassmorphism) -->
    <UpgradeModal 
      v-if="showUpgradeModal" 
      @close="showUpgradeModal = false" 
      @select-tier="handleTierSelection" 
    />

    <!-- Modal de Celebración de Pago Exitoso (Success Modal) -->
    <div v-if="showSuccessModal" class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="showSuccessModal = false"></div>
      <div class="relative w-full max-w-lg bg-white rounded-[2rem] shadow-2xl p-8 text-center overflow-hidden flex flex-col gap-6 border border-slate-100">
        <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-400 to-teal-500"></div>
        
        <div class="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center text-4xl mx-auto shadow-sm">
          🎉
        </div>
        
        <div class="space-y-2">
          <h3 class="text-2xl font-black text-slate-800">¡Tu invitación está en Vivo! ✨</h3>
          <p class="text-slate-500 text-sm">
            Hemos procesado tu pago exitosamente. Las marcas de agua han sido removidas y todas tus características premium están desbloqueadas.
          </p>
        </div>

        <!-- Acciones -->
        <div class="flex flex-col gap-3">
          <button @click="copyInvitationLink" class="btn btn-outline border-slate-200 text-slate-700 hover:bg-slate-50 w-full py-3 rounded-xl font-bold flex items-center justify-center gap-2">
            🔗 Copiar Enlace
          </button>
          
          <a :href="whatsappShareUrl" target="_blank" class="btn bg-emerald-500 hover:bg-emerald-600 text-white w-full py-3 rounded-xl font-black flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 text-center">
            💬 Enviar por WhatsApp
          </a>
          
          <button @click="showSuccessModal = false" class="btn btn-ghost text-slate-400 font-bold uppercase tracking-widest text-[10px] mt-2">
            Seguir Editando
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Reseña para Activación de Plan Básico -->
    <div v-if="showReviewModal" class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="showReviewModal = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 md:p-8 flex flex-col gap-6 border border-slate-100 overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-sky-400 to-indigo-500"></div>
        
        <div class="text-center space-y-2">
          <span class="text-3xl">✨</span>
          <h3 class="text-xl font-black text-slate-800">Activa tu Invitación Gratis</h3>
          <p class="text-slate-500 text-xs sm:text-sm">
            Para publicar tu invitación en el plan básico, cuéntanos qué te ha parecido nuestra plataforma.
          </p>
        </div>

        <form @submit.prevent="submitReviewAndActivate" class="space-y-4">
          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Tu Nombre</label>
            <input 
              v-model="reviewForm.reviewer_name" 
              type="text" 
              placeholder="Ej: Sofía Martínez" 
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-slate-700 text-sm"
              required 
            />
          </div>

          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Calificación</label>
            <div class="flex items-center gap-1">
              <button 
                v-for="star in 5" 
                :key="star" 
                type="button"
                @click="reviewForm.rating = star"
                class="text-2xl transition-all"
              >
                <span v-if="star <= reviewForm.rating" class="text-amber-400">★</span>
                <span v-else class="text-slate-200">★</span>
              </button>
            </div>
          </div>

          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Tu Testimonio / Opinión</label>
            <textarea 
              v-model="reviewForm.comment" 
              rows="3"
              placeholder="Ej: La plataforma es super intuitiva y rápida de usar. ¡Me encantó el sobre animado!" 
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-slate-700 text-sm resize-none"
              required
            ></textarea>
          </div>

          <div class="flex gap-3 pt-2">
            <button 
              type="button" 
              @click="showReviewModal = false" 
              class="btn btn-outline border-slate-200 text-slate-500 hover:bg-slate-50 flex-1 py-2.5 rounded-xl font-bold text-sm"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn bg-indigo-600 hover:bg-indigo-700 text-white flex-1 py-2.5 rounded-xl font-bold text-sm shadow-md"
            >
              Publicar Ahora 🚀
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Publicación del Administrador como Producto Comercial -->
    <div v-if="showAdminPublishModal" class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="showAdminPublishModal = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 md:p-8 flex flex-col gap-6 border border-slate-100 overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-pink-500 to-indigo-600"></div>
        
        <div class="text-center space-y-2">
          <span class="text-3xl">🛍️</span>
          <h3 class="text-xl font-black text-slate-800">Publicar como Producto</h3>
          <p class="text-slate-500 text-xs sm:text-sm">
            Convierte esta plantilla de diseño en un producto comercial del catálogo general.
          </p>
        </div>

        <form @submit.prevent="submitAdminPublish" class="space-y-4">
          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Nombre del Producto</label>
            <input 
              v-model="adminPublishForm.name" 
              type="text" 
              placeholder="Ej: Invitación Boda Clásica Oro" 
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-slate-700 text-sm"
              required 
            />
          </div>

          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Slug de la Plantilla (Único)</label>
            <input 
              v-model="adminPublishForm.slug" 
              type="text" 
              placeholder="ej-invitacion-boda-oro" 
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-slate-700 text-sm"
              required 
            />
          </div>

          <div class="form-group flex flex-col gap-1.5 text-left">
            <label class="text-xs font-bold text-slate-600">Asociar a Sucursal / Tienda (Opcional)</label>
            <select 
              v-model="adminPublishForm.store_id"
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-slate-700 text-sm"
            >
              <option :value="null">Ninguna (Catálogo Global B2C)</option>
              <option v-for="store in storesList" :key="store.id" :value="store.id">
                {{ store.name }} ({{ store.city || 'Sin ciudad' }})
              </option>
            </select>
          </div>

          <div class="flex gap-3 pt-2">
            <button 
              type="button" 
              @click="showAdminPublishModal = false" 
              class="btn btn-outline border-slate-200 text-slate-500 hover:bg-slate-50 flex-1 py-2.5 rounded-xl font-bold text-sm"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn bg-indigo-600 hover:bg-indigo-700 text-white flex-1 py-2.5 rounded-xl font-bold text-sm shadow-md"
            >
              Crear Producto 🛒
            </button>
          </div>
        </form>
      </div>
    </div>
  </BuilderLayout>

</template>

<script setup>
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/modules/auth/store/auth';
import BuilderLayout from '@/layouts/BuilderLayout.vue';
import { builderService } from '@/modules/builder/services/builderService';
import { crmService } from '@/modules/workspace/services/crmService';
import RenderEngineMaster from '@/modules/engine/components/RenderEngineMaster.vue';
import EnvelopeWrapper from '@/modules/engine/components/EnvelopeWrapper.vue';
import UpgradeModal from '@/modules/builder/components/UpgradeModal.vue';

// Variables de estado adicionales v0.8.4
const productTier = ref('BASIC');
const deploymentIsPaid = ref(false);
const isEditingSlug = ref(false);
const editableSlug = ref('');
const showReviewModal = ref(false);
const showAdminPublishModal = ref(false);
const storesList = ref([]);

const reviewForm = ref({
  reviewer_name: '',
  comment: '',
  rating: 5
});

const adminPublishForm = ref({
  name: '',
  slug: '',
  store_id: null
});


const route = useRoute();
const router = useRouter();
let authStore = null;
try {
  authStore = useAuthStore();
} catch (e) {
  // Silent fallback for unit testing environments without active Pinia
}
const toast = useToast();
const deploymentId = route.params.id;

const loading = ref(true);
const saveStatus = ref('saved'); // 'saved', 'unsaved', 'saving', 'error'
const activeTab = ref('cover'); // 'cover', 'rsvp', 'timer', 'timeline', 'music', 'theme', 'og', 'envelope'
const showMobilePreview = ref(false);
const showUpgradeModal = ref(false);
const showSuccessModal = ref(false);

const handleTierSelection = (productId) => {
  if (deploymentId) {
    localStorage.setItem('pending_sandbox_id', deploymentId);
  }
  showUpgradeModal.value = false;
  router.push(`/checkout/${productId}`);
};

const copyInvitationLink = () => {
  const url = `${window.location.origin}/i/${deploymentSlug.value}`;
  navigator.clipboard.writeText(url);
  toast.success('¡Enlace copiado al portapapeles!');
};

const whatsappShareUrl = computed(() => {
  const url = `${window.location.origin}/i/${deploymentSlug.value}`;
  const text = `¡Hola! Queremos invitarte a nuestro evento. Mira todos los detalles y confirma tu asistencia aquí: ${url}`;
  return `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
});

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
  og_image: '',
  envelope_type: null,
  envelope: null
});

onMounted(async () => {
  if (route.query.payment === 'success') {
    showSuccessModal.value = true;
    router.replace({ query: {} });
  }
  try {
    const res = await builderService.getDeployment(deploymentId);
    if (res.data) {
      deploymentSlug.value = res.data.slug || '';
      deploymentStatus.value = res.data.status || 'DRAFT';
      deploymentIsPaid.value = res.data.is_paid || false;
      productTier.value = res.data.product_tier || 'BASIC';
      editableSlug.value = res.data.slug || '';
      
      const isAdminOrDesigner = authStore?.role === 'ADMIN' || authStore?.role === 'DESIGNER';
      if (authStore?.role === 'ADMIN') {
        try {
          const storesRes = await crmService.fetchAllStores();
          storesList.value = storesRes.data || [];
        } catch (e) {
          console.error("Error al cargar tiendas:", e);
        }
      }
      
      if (isAdminOrDesigner) {
        allowedFeatures.value = {
          background_music: true,
          custom_audio_url: true,
          countdown_timer: true,
          timeline: true,
          custom_theme: true,
          custom_og: true,
        };
      } else if (res.data.allowed_features) {
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
        localConfig.value.envelope_type = custom.envelope_type ?? custom.envelope ?? null;
        localConfig.value.envelope = custom.envelope_type ?? custom.envelope ?? null;
      }
    }
  } catch (error) {
    toast.error('Error al cargar la configuración');
  } finally {
    loading.value = false;
  }
  updateScaleFactor();
  window.addEventListener('resize', updateScaleFactor);
});

const openLiveDemo = () => {
  if (deploymentSlug.value) {
    window.open(`/i/${deploymentSlug.value}`, '_blank');
  }
};

const startEditingSlug = () => {
  editableSlug.value = deploymentSlug.value;
  isEditingSlug.value = true;
};

const saveSlug = async () => {
  if (!editableSlug.value || editableSlug.value.trim() === '') {
    toast.error('El slug no puede estar vacío.');
    isEditingSlug.value = false;
    return;
  }
  
  const slugRegex = /^[a-z0-9-]+$/;
  if (!slugRegex.test(editableSlug.value)) {
    toast.error('El slug solo puede contener letras minúsculas, números y guiones.');
    return;
  }
  
  try {
    await builderService.updateDeployment(deploymentId, { slug: editableSlug.value.trim() });
    deploymentSlug.value = editableSlug.value.trim();
    toast.success('Slug actualizado correctamente.');
    isEditingSlug.value = false;
  } catch (error) {
    const errMsg = error.response?.data?.error || error.response?.data?.slug?.[0] || 'Error al actualizar el slug';
    toast.error(errMsg);
  }
};

const handlePublishClick = () => {
  const role = authStore?.role;
  if (role === 'ADMIN') {
    adminPublishForm.value.name = localConfig.value.cover.title || '';
    adminPublishForm.value.slug = deploymentSlug.value || '';
    adminPublishForm.value.store_id = null;
    showAdminPublishModal.value = true;
  } else if (role === 'DESIGNER') {
    toast.info('Los cambios del diseño se guardaron en tu biblioteca.');
  } else {
    if (productTier.value === 'BASIC') {
      reviewForm.value.reviewer_name = '';
      reviewForm.value.comment = '';
      reviewForm.value.rating = 5;
      showReviewModal.value = true;
    } else {
      if (deploymentIsPaid.value) {
        confirmPublishPaid();
      } else {
        showUpgradeModal.value = true;
      }
    }
  }
};

const confirmPublishPaid = async () => {
  if (confirm('¿Estás seguro de que deseas poner tu invitación en vivo?')) {
    try {
      await builderService.updateDeployment(deploymentId, { status: 'LIVE' });
      deploymentStatus.value = 'LIVE';
      toast.success('¡Tu invitación está En Vivo!');
    } catch (e) {
      toast.error('Error al publicar la invitación.');
    }
  }
};

const pauseInvitation = async () => {
  if (confirm('¿Estás seguro de que deseas pausar tu invitación? Esto desactivará el acceso público temporalmente.')) {
    try {
      await builderService.updateDeployment(deploymentId, { status: 'DRAFT' });
      deploymentStatus.value = 'DRAFT';
      toast.info('Invitación pausada correctamente.');
    } catch (e) {
      toast.error('Error al pausar la invitación.');
    }
  }
};

const submitReviewAndActivate = async () => {
  if (!reviewForm.value.reviewer_name || !reviewForm.value.comment) {
    toast.error('Por favor, ingresa tu nombre y tu comentario.');
    return;
  }
  try {
    const res = await builderService.activateBasic(deploymentId, reviewForm.value);
    deploymentStatus.value = res.data.status || 'LIVE';
    deploymentIsPaid.value = true;
    toast.success('¡Plan básico activado y publicado exitosamente!');
    showReviewModal.value = false;
    showSuccessModal.value = true;
  } catch (e) {
    const errMsg = e.response?.data?.error || 'Error al activar tu plan básico.';
    toast.error(errMsg);
  }
};

const submitAdminPublish = async () => {
  if (!adminPublishForm.value.name || !adminPublishForm.value.slug) {
    toast.error('El nombre y el slug son requeridos.');
    return;
  }
  try {
    const res = await builderService.publishProduct(deploymentId, adminPublishForm.value);
    toast.success('¡Producto comercial creado exitosamente!');
    showAdminPublishModal.value = false;
  } catch (e) {
    const errMsg = e.response?.data?.error || 'Error al publicar como producto.';
    toast.error(errMsg);
  }
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

// Sincronizar el envelope heredado
watch(() => localConfig.value.envelope_type, (newVal) => {
  localConfig.value.envelope = newVal;
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

const scaleFactor = ref(1);

const updateScaleFactor = () => {
  const containerHeight = window.innerHeight - 150;
  const targetHeight = 800;
  if (containerHeight < targetHeight) {
    scaleFactor.value = Math.max(0.4, containerHeight / targetHeight);
  } else {
    scaleFactor.value = 1;
  }
};

const scaleStyle = computed(() => {
  if (typeof window !== 'undefined' && window.innerWidth < 768) {
    return {};
  }
  return {
    transform: `scale(${scaleFactor.value})`,
    transformOrigin: 'center center',
    transition: 'transform 0.2s ease-out'
  };
});

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateScaleFactor);
  }
});
</script>

<style scoped>
.save-status-container {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  font-weight: bold;
}
.status-indicator {
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}
@media (min-width: 640px) {
  .status-indicator {
    padding: 0.4rem 0.8rem;
  }
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
  background: #020617;
}

/* Panel de Controles */
.control-panel {
  width: 380px;
  background: #0b0f19;
  color: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.5);
  z-index: 10;
}
.panel-header {
  padding: 1.5rem 2rem 0.75rem 2rem;
}
.panel-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 900;
  letter-spacing: -0.025em;
  color: #ffffff;
}

/* Tabs Grid */
.tabs-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.35rem;
  background: #020617;
  padding: 0.35rem;
  border-radius: 12px;
  margin: 0.5rem 1.5rem 1.5rem 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.tab-btn {
  padding: 0.6rem 0.75rem;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 0.8rem;
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
  color: #38bdf8;
}
.tab-btn.active {
  background: rgba(56, 189, 248, 0.15);
  border: 1px solid rgba(56, 189, 248, 0.3);
  color: #38bdf8;
  box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1);
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
  background: #020617;
  border: 1px solid #1e293b;
  color: white;
  padding: 0.85rem 1rem;
  border-radius: 10px;
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
  background: #020617;
  border: 1px solid #1e293b;
  color: white;
  padding: 0.85rem 1rem;
  border-radius: 10px;
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
  background: #020617;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  border: 1px solid #1e293b;
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
  background: #020617;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  border: 1px solid #1e293b;
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

/* Envelope Info Card */
.envelope-info-card {
  background: #0f172a;
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}
.info-icon {
  font-size: 1.25rem;
}
.info-text {
  font-size: 0.8rem;
  color: #cbd5e1;
  line-height: 1.4;
  margin: 0;
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
  background: #020617;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  overflow: hidden;
  background-image: radial-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 0);
  background-size: 24px 24px;
}
.simulator-scale-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 380px;
  height: 800px;
  position: relative;
}
.device-shadow-3d {
  position: absolute;
  width: 380px;
  height: 800px;
  border-radius: 40px;
  background: rgba(0, 0, 0, 0.6);
  filter: blur(25px);
  transform: translateY(18px) scale(0.98);
  z-index: 0;
}

.device-frame {
  width: 380px;
  height: 800px;
  border-radius: 40px;
  overflow: hidden;
  position: relative;
  background: #020617;
  border: 1px solid rgba(255, 255, 255, 0.08);
  z-index: 2;
  transform-style: preserve-3d;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.device-bezel-frame {
  position: absolute;
  inset: 0;
  border: 12px solid #0f172a;
  border-radius: 40px;
  pointer-events: none;
  z-index: 10;
  box-shadow: inset 0 0 8px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,255,255,0.05);
  display: flex;
  justify-content: center;
}

.device-island-notch {
  position: absolute;
  top: 8px;
  width: 100px;
  height: 24px;
  background: #000000;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  z-index: 11;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px 0 12px;
}

.device-camera-lens {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #1e1b4b, #000 70%);
  border: 1px solid #312e81;
}

.device-sensor-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #111;
}

.device-glass-reflection {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0) 45%, rgba(255, 255, 255, 0) 100%);
  border-radius: 40px;
  pointer-events: none;
  z-index: 9;
}

@media (max-width: 767px) {
  .studio-container {
    height: 100vh; /* Ocupar toda la pantalla en móvil */
    overflow: hidden;
  }
  .control-panel {
    width: 100%;
    height: 100%;
  }
  .preview-panel {
    padding: 0;
    height: 100%;
  }
  .device-frame {
    width: 100%;
    height: 100%;
    border-radius: 0;
    border: none;
    box-shadow: none;
  }
  .device-bezel-frame,
  .device-island-notch,
  .device-glass-reflection,
  .device-shadow-3d {
    display: none !important;
  }
  .is-hidden-mobile {
    display: none !important;
  }
}

.preview-canvas {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  z-index: 1;
}

.preview-canvas::-webkit-scrollbar {
  width: 0px;
}
</style>
