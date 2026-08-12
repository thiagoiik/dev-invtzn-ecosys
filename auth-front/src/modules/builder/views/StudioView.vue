<template>
  <BuilderLayout>
    <template #title>
      <div class="flex items-center gap-2 text-white max-w-full">
        <!-- Si es Admin o Designer, permitimos la edición con doble clic/botón -->
        <template v-if="isAdminOrDesigner">
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
        </template>
        <!-- Para otros roles (clientes): solo texto de lectura -->
        <template v-else>
          <span class="font-semibold text-xs sm:text-sm md:text-base truncate max-w-[150px] md:max-w-xs select-none">
            🔗 {{ deploymentSlug }}
          </span>
        </template>
      </div>
    </template>

    <template #actions>
        <div class="save-status-container flex items-center gap-1.5 sm:gap-3">
          <!-- Badge de Estado de la Invitación -->
          <span v-if="deploymentStatus === 'LIVE'" class="badge bg-emerald-500 text-white font-bold text-[10px] sm:text-xs uppercase px-2 py-1 sm:px-3 sm:py-1.5 rounded-lg flex items-center gap-1 shadow-sm">
            🟢<span class="hidden sm:inline"> En Vivo</span>
          </span>
          <span v-else-if="deploymentStatus === 'ACTIVE'" class="badge bg-indigo-600 text-white font-bold text-[10px] sm:text-xs uppercase px-2 py-1 sm:px-3 sm:py-1.5 rounded-lg flex items-center gap-1 shadow-sm">
            🎨<span class="hidden sm:inline"> Plantilla</span>
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
          v-if="deploymentStatus !== 'LIVE' && deploymentStatus !== 'ACTIVE'"
          @click="handlePublishClick"
          class="btn btn-sm bg-gradient-to-r from-pink-500 to-indigo-600 hover:from-pink-600 hover:to-indigo-700 text-white font-black px-2.5 py-1.5 sm:px-4 sm:py-2 rounded-xl shadow-md transition-all flex items-center gap-1 text-[10px] sm:text-xs"
        >
          ✨<span class="hidden sm:inline"> {{ authStore?.role === 'DESIGNER' ? 'Enviar a revisión' : 'Publicar' }}</span>
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
      <!-- Bottom Navigation Bar para Móviles -->
      <div class="mobile-bottom-bar md:hidden fixed bottom-0 left-0 right-0 z-[100] bg-slate-900 border-t border-slate-800 flex shadow-[0_-10px_40px_rgba(0,0,0,0.5)] pb-safe">
        <button 
          class="flex-1 py-3 text-xs font-bold flex flex-col items-center gap-1 transition-colors"
          :class="!showMobilePreview ? 'text-primary bg-slate-800/50' : 'text-slate-400 hover:text-slate-200'"
          @click="showMobilePreview = false"
        >
          <span class="text-lg">🛠️</span>
          <span>Herramientas</span>
        </button>
        <button 
          class="flex-1 py-3 text-xs font-bold flex flex-col items-center gap-1 transition-colors"
          :class="showMobilePreview ? 'text-primary bg-slate-800/50' : 'text-slate-400 hover:text-slate-200'"
          @click="showMobilePreview = true"
        >
          <span class="text-lg">📱</span>
          <span>Vista Previa</span>
        </button>
      </div>

      <!-- PANEL IZQUIERDO: CONTROLES -->
      <aside class="control-panel" :class="{ 'is-hidden-mobile': showMobilePreview }">
        <!-- HEADER Y SELECTOR DE SECCIONES -->
        <div class="border-b border-slate-800/50 bg-slate-900/50 flex flex-col">
          <div class="px-4 md:px-6 pt-4 md:pt-6 pb-2">
            <label class="text-[10px] uppercase font-extrabold text-slate-500 block tracking-wider">Editando Sección:</label>
          </div>
          <!-- Horizontal Scrollable Tabs -->
          <div class="horizontal-tabs-container w-full overflow-x-auto whitespace-nowrap px-4 md:px-6 pb-4">
            <div class="flex gap-2 w-max">
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'cover' }" @click="activeTab = 'cover'">
                <span class="text-lg">🌅</span><span class="text-xs font-bold">Portada</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'rsvp' }" @click="activeTab = 'rsvp'">
                <span class="text-lg">✉️</span><span class="text-xs font-bold">RSVP</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'location' }" @click="activeTab = 'location'">
                <span class="text-lg">📍</span><span class="text-xs font-bold">Ubicación</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'timer' }" @click="activeTab = 'timer'">
                <span class="text-lg">🕰️</span><span class="text-xs font-bold">Contador</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'timeline' }" @click="activeTab = 'timeline'">
                <span class="text-lg">📅</span><span class="text-xs font-bold">Itinerario</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'music' }" @click="activeTab = 'music'">
                <span class="text-lg">🎵</span><span class="text-xs font-bold">Música</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'theme' }" @click="activeTab = 'theme'">
                <span class="text-lg">🎨</span><span class="text-xs font-bold">Estilos</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'og' }" @click="activeTab = 'og'">
                <span class="text-lg">⚙️</span><span class="text-xs font-bold">SEO/OG</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'dress_code' }" @click="activeTab = 'dress_code'">
                <span class="text-lg">👗</span><span class="text-xs font-bold">Dress Code</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'envelope' }" @click="activeTab = 'envelope'">
                <span class="text-lg">✉️</span><span class="text-xs font-bold">Sobre</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'sections' }" @click="activeTab = 'sections'">
                <span class="text-lg">⚙️</span><span class="text-xs font-bold">Estructura</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'gift' }" @click="activeTab = 'gift'">
                <span class="text-lg">🎁</span><span class="text-xs font-bold">Regalos</span>
              </button>
              <button type="button" class="h-tab-btn" :class="{ 'active': activeTab === 'gallery' }" @click="activeTab = 'gallery'">
                <span class="text-lg">📸</span><span class="text-xs font-bold">Galería</span>
              </button>
              <button v-for="b in protocolBlocks" :key="'p_'+b.id" type="button" class="h-tab-btn" :class="{ 'active': activeTab === b.id }" @click="activeTab = b.id">
                <span class="text-lg">🧩</span><span class="text-xs font-bold truncate max-w-[80px]">{{ b.name }}</span>
              </button>
              <button v-for="b in thoughtsBlocks" :key="'t_'+b.id" type="button" class="h-tab-btn" :class="{ 'active': activeTab === b.id }" @click="activeTab = b.id">
                <span class="text-lg">💭</span><span class="text-xs font-bold truncate max-w-[80px]">{{ b.name }}</span>
              </button>
            </div>
          </div>
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
              <div class="flex gap-2">
                <input v-model="localConfig.cover.coverPhoto" type="url" placeholder="https://..." class="flex-grow" />
                <button type="button" @click="isGalleryOpen = true" class="btn btn-sm btn-outline text-xs h-[42px] px-3 bg-white/5 border-white/10 text-amber-400 hover:bg-white/10 shrink-0">
                  ✨ Galería
                </button>
              </div>
            </div>

            <!-- Ajuste de posición de la foto (Enfoque) -->
            <div class="space-y-4" v-if="localConfig.cover.coverPhoto">
              <!-- Posición Horizontal -->
              <div class="form-group">
                <label class="flex justify-between">
                  <span>Enfoque Horizontal (X)</span>
                  <span class="font-bold font-mono">{{ (localConfig.cover.backgroundPositionX !== undefined && localConfig.cover.backgroundPositionX !== null) ? localConfig.cover.backgroundPositionX : 50 }}%</span>
                </label>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  v-model.number="localConfig.cover.backgroundPositionX" 
                  class="hue-range"
                />
                <span class="help-text text-xs text-slate-400 mt-1 block">Desplaza la foto a la izquierda (0%) o derecha (100%). Útil para fotos horizontales en celulares.</span>
              </div>

              <!-- Posición Vertical -->
              <div class="form-group">
                <label class="flex justify-between">
                  <span>Enfoque Vertical (Y)</span>
                  <span class="font-bold font-mono">{{ (localConfig.cover.backgroundPositionY !== undefined && localConfig.cover.backgroundPositionY !== null) ? localConfig.cover.backgroundPositionY : 50 }}%</span>
                </label>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  v-model.number="localConfig.cover.backgroundPositionY" 
                  class="hue-range"
                />
                <span class="help-text text-xs text-slate-400 mt-1 block">Desplaza la foto hacia arriba (0%) o abajo (100%). Útil para fotos verticales en monitores.</span>
              </div>
            </div>

            <div class="form-group" v-if="localConfig.cover.frame_overlay">
              <label>Marco Decorativo Activo</label>
              <div class="flex items-center justify-between p-2 rounded bg-white/5 border border-white/10 text-xs">
                <span class="truncate max-w-[180px]">{{ localConfig.cover.frame_overlay.split('/').pop().replace('.svg', '').replace('frame_', '').replace('_', ' ') }}</span>
                <button type="button" @click="localConfig.cover.frame_overlay = null" class="text-red-400 hover:text-red-300">Quitar</button>
              </div>
            </div>
            
            <div class="form-group">
              <label>Color del Título</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.cover.titleColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.cover.titleColor }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Color del Subtítulo</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.cover.subtitleColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.cover.subtitleColor }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Color de Etiqueta Superior</label>
              <div class="color-picker-wrapper">
                <input v-model="localConfig.cover.headerLabelColor" type="color" class="color-input" />
                <span class="color-value">{{ localConfig.cover.headerLabelColor }}</span>
              </div>
            </div>

            <div class="form-group">
              <label class="flex justify-between">
                <span>Tamaño del Título</span>
                <span class="font-bold font-mono">{{ localConfig.cover.titleSize || 4.5 }}rem</span>
              </label>
              <input 
                type="range" 
                min="2" 
                max="7" 
                step="0.1"
                v-model.number="localConfig.cover.titleSize" 
                class="hue-range"
              />
            </div>

            <div class="form-group">
              <label class="flex justify-between">
                <span>Opacidad de la Capa Oscura</span>
                <span class="font-bold font-mono">{{ localConfig.cover.overlayOpacity }}%</span>
              </label>
              <input 
                type="range" 
                min="10" 
                max="95" 
                step="5"
                v-model.number="localConfig.cover.overlayOpacity" 
                class="hue-range"
              />
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
            <!-- Simular Nivel RSVP (Sólo Admin/Diseñador) -->
            <div v-if="isAdminOrDesigner" class="form-group mb-4">
              <label class="block text-xs font-black text-amber-600 uppercase tracking-widest pl-1 mb-2">Nivel RSVP</label>
              <select v-model="localConfig.rsvp.tier" class="select-input w-full">
                <option value="BASIC">Básico (Confirmación a WhatsApp)</option>
                <option value="STANDARD">Estándar (Base de datos + Acompañantes)</option>
                <option value="PREMIUM">Premium (Base de datos + Menú + Alergias)</option>
              </select>
              <p class="text-[10px] text-slate-450 mt-1">Permite seleccionar el tipo de RSVP.</p>
            </div>

            <div class="form-group">
              <label>Título Sección RSVP</label>
              <input v-model="localConfig.rsvp.title" type="text" placeholder="Ej: Confirma tu Asistencia" />
            </div>

            <div class="form-group">
              <label class="flex justify-between items-center mb-1.5">
                <span>Icono de Sección</span>
                <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
              </label>
              <div class="dropdown dropdown-top dropdown-end w-full">
                <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                  <span class="flex items-center gap-2">
                    <img v-if="localConfig.rsvp.icon && isUrl(localConfig.rsvp.icon)" :src="localConfig.rsvp.icon" class="w-6 h-6 object-contain" />
                    <span v-else class="text-lg">{{ localConfig.rsvp.icon || '✉️' }}</span>
                    <span class="text-xs text-slate-400">Seleccionar...</span>
                  </span>
                  <span class="text-xs">▼</span>
                </div>
                <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                  <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                  <div class="grid grid-cols-5 gap-2 text-center text-xl">
                    <button 
                      v-for="emoji in ['✉️', '💍', '🥂', '👗', '📍', '🎁', '🕰️', '📅', '📸', '🎵', '⛪', '🕊️', '📜', '✨', '🍽️']" 
                      :key="emoji"
                      type="button"
                      class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                      @click="localConfig.rsvp.icon = emoji"
                    >
                      {{ emoji }}
                    </button>
                  </div>
                  <div class="border-t border-white/5 my-1"></div>
                  <div class="space-y-1.5">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                    <input 
                      v-model="localConfig.rsvp.icon" 
                      type="text" 
                      placeholder="Pegar Emoji o URL SVG/PNG" 
                      class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                    />
                  </div>
                </div>
              </div>
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

            <div v-if="localConfig.rsvp.tier === 'BASIC'" class="form-group">
              <label>WhatsApp de Confirmación</label>
              <input v-model="localConfig.rsvp.whatsappPhone" type="tel" placeholder="Ej. +5215512345678" />
              <p class="text-[10px] text-slate-400 mt-1">Los invitados del plan básico enviarán confirmaciones directas a este número de WhatsApp.</p>
            </div>

            <!-- Tarjeta de Estatus de Plan y Upgrade (Coherente y Oscura) -->
            <div v-if="productTier !== 'PREMIUM' && !isAdminOrDesigner" class="schedule-item-card mt-6 border border-amber-500/10">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold text-amber-500 uppercase tracking-wider">Upgrade de Plan RSVP</span>
                <span class="badge badge-sm font-black text-white bg-slate-700 border-slate-600">{{ productTier }}</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mb-3">
                <span v-if="productTier === 'BASIC'">
                  Desbloquea el guardado automático de invitados en la Base de Datos, conteo de acompañantes, menús y alergias con un Pase superior.
                </span>
                <span v-else-if="productTier === 'STANDARD'">
                  Permite a tus invitados seleccionar su tipo de menú y reportar alergias o restricciones de alimentos con el Pase Premium.
                </span>
              </p>
              <button @click="showUpgradeModal = true" class="upgrade-btn w-full">
                🔓 Desbloquear RSVP {{ productTier === 'BASIC' ? 'Standard / Premium' : 'Premium' }}
              </button>
            </div>
          </div>

          <!-- TAB UBICACIÓN -->
          <div v-if="activeTab === 'location'" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Ubicación del Evento</h3>
            </div>
            <p class="text-xs text-slate-400">Configura la ubicación física y el mapa interactivo del evento para tus invitados.</p>

            <!-- Feature Switch -->
            <div class="switch-container">
              <label class="switch-label">
                <span class="flex items-center gap-2">
                  📍 Habilitar Ubicación
                </span>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_location" 
                  class="switch-input"
                />
              </label>
            </div>

            <!-- Fields wrapper -->
            <div :class="{ 'opacity-40 pointer-events-none': !localConfig.has_location }" class="space-y-6">
              <div class="form-group flex flex-col gap-2">
                <label>Título de la Sección</label>
                <input 
                  v-model="localConfig.location.title" 
                  type="text" 
                  placeholder="Ej: Ubicación del Evento o Ceremonia" 
                  :disabled="!localConfig.has_location"
                />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label class="flex justify-between items-center">
                  <span>Icono de Sección</span>
                  <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
                </label>
                <div class="dropdown dropdown-top dropdown-end w-full" :class="{ 'pointer-events-none opacity-40': !localConfig.has_location }">
                  <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                    <span class="flex items-center gap-2">
                      <img v-if="localConfig.location.icon && isUrl(localConfig.location.icon)" :src="localConfig.location.icon" class="w-6 h-6 object-contain" />
                      <span v-else class="text-lg">{{ localConfig.location.icon || '📍' }}</span>
                      <span class="text-xs text-slate-400">Seleccionar...</span>
                    </span>
                    <span class="text-xs">▼</span>
                  </div>
                  <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                    <div class="grid grid-cols-5 gap-2 text-center text-xl">
                      <button 
                        v-for="emoji in ['📍', '⛪', '🏛️', '💍', '🥂', '✉️', '👗', '🎁', '🕰️', '📅', '📸', '🎵', '🕊️', '📜', '✨']" 
                        :key="emoji"
                        type="button"
                        class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                        @click="localConfig.location.icon = emoji"
                      >
                        {{ emoji }}
                      </button>
                    </div>
                    <div class="border-t border-white/5 my-1"></div>
                    <div class="space-y-1.5">
                      <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                      <input 
                        v-model="localConfig.location.icon" 
                        type="text" 
                        placeholder="Pegar Emoji o URL SVG/PNG" 
                        class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                        :disabled="!localConfig.has_location"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-group flex flex-col gap-2">
                <label>Nombre del Lugar / Salón</label>
                <input 
                  v-model="localConfig.location.venueName" 
                  type="text" 
                  placeholder="Ej: Salón de Eventos Las Nubes" 
                  :disabled="!localConfig.has_location"
                />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label>Dirección</label>
                <input 
                  v-model="localConfig.location.address" 
                  type="text" 
                  placeholder="Ej: Av. Paseo de la Reforma #123, Col. Centro" 
                  :disabled="!localConfig.has_location"
                />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label>Enlace de Mapas (Google Maps, Waze, etc.)</label>
                <input 
                  v-model="localConfig.location.googleMapsUrl" 
                  type="text" 
                  placeholder="Ej: https://maps.app.goo.gl/..." 
                  :disabled="!localConfig.has_location"
                />
                <p class="text-[10px] text-slate-400 mt-1">Este enlace se usará para el botón "Cómo llegar". Abre directamente en las apps de navegación de los invitados.</p>
              </div>

              <!-- Múltiples Ubicaciones (Ceremonia y Recepción) -->
              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3 mt-4">
                <span class="text-xs font-bold text-amber-400">⛪ Ceremonia Religiosa / Civil</span>
                <div class="form-group flex flex-col gap-2">
                  <label class="text-[10px] uppercase font-bold text-slate-400">Nombre del Lugar</label>
                  <input v-model="localConfig.locations.ceremonyName" type="text" placeholder="Ej: Parroquia de Santa María" :disabled="!localConfig.has_location" />
                </div>
                <div class="form-group flex flex-col gap-2">
                  <label class="text-[10px] uppercase font-bold text-slate-400">Enlace de Google Maps</label>
                  <input v-model="localConfig.locations.ceremonyMapsUrl" type="url" placeholder="https://maps.google.com/..." :disabled="!localConfig.has_location" />
                </div>
              </div>

              <div class="p-4 bg-slate-900/40 rounded-2xl border border-slate-700/40 space-y-3 mt-4">
                <span class="text-xs font-bold text-amber-400">🥂 Recepción / Fiesta</span>
                <div class="form-group flex flex-col gap-2">
                  <label class="text-[10px] uppercase font-bold text-slate-400">Nombre del Salón / Jardín</label>
                  <input v-model="localConfig.locations.receptionName" type="text" placeholder="Ej: Jardín de Eventos Los Pinos" :disabled="!localConfig.has_location" />
                </div>
                <div class="form-group flex flex-col gap-2">
                  <label class="text-[10px] uppercase font-bold text-slate-400">Enlace de Google Maps</label>
                  <input v-model="localConfig.locations.receptionMapsUrl" type="url" placeholder="https://maps.google.com/..." :disabled="!localConfig.has_location" />
                </div>
              </div>

              <!-- Nivel de Zoom (Bloqueado a partir de Standard) -->
              <div class="form-group flex flex-col gap-2">
                <div class="flex justify-between items-center">
                  <label>Zoom del Mapa Integrado</label>
                  <span v-if="!allowedFeatures.countdown_timer" class="badge-lock">STANDARD 👑</span>
                  <span v-else class="text-xs font-black text-indigo-400 font-mono">{{ localConfig.location.zoom || 14 }}x</span>
                </div>
                <p class="text-[10px] text-slate-500">
                  Aumenta el zoom para enfocar la calle o redúcelo para ver la zona general.
                </p>
                
                <input 
                  :value="allowedFeatures.countdown_timer ? localConfig.location.zoom : 14"
                  @input="allowedFeatures.countdown_timer ? (localConfig.location.zoom = Number($event.target.value)) : null"
                  :disabled="!allowedFeatures.countdown_timer || !localConfig.has_location"
                  type="range" 
                  min="10" 
                  max="20" 
                  step="1"
                  class="w-full accent-indigo-500 cursor-pointer"
                  :class="{ 'opacity-50 cursor-not-allowed': !allowedFeatures.countdown_timer || !localConfig.has_location }"
                />
                
                <p v-if="!allowedFeatures.countdown_timer" class="text-[10px] text-amber-500 font-semibold mt-1">
                  El ajuste de zoom requiere un plan <strong>Standard</strong> o superior. El zoom para el plan básico está fijo en 14x.
                </p>
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
                <div class="flex gap-2">
                  <input 
                    v-model="localConfig.audioUrl" 
                    type="url" 
                    placeholder="https://..." 
                    class="flex-grow"
                    :disabled="!localConfig.has_music || !allowedFeatures.background_music"
                    @input="syncAudioUrl"
                  />
                  <button 
                    v-if="false"
                    type="button" 
                    @click="isMusicGalleryOpen = true" 
                    class="btn btn-sm btn-outline text-xs h-[42px] px-3 bg-white/5 border-white/10 text-amber-400 hover:bg-white/10 shrink-0"
                    :disabled="!localConfig.has_music || !allowedFeatures.background_music"
                  >
                    ✨ Buscar Melodías
                  </button>
                </div>
                <span class="help-text">Ingresa una URL directa o busca melodías libres de derechos.</span>
              </div>

              <!-- Punto de Inicio (Offset) -->
              <div class="form-group" v-if="localConfig.music">
                <label class="flex justify-between">
                  <span>Segundo de Inicio (Trim)</span>
                  <span class="font-bold font-mono">{{ (localConfig.music.audioStartOffset !== undefined && localConfig.music.audioStartOffset !== null) ? localConfig.music.audioStartOffset : 0 }}s</span>
                </label>
                <input 
                  type="range" 
                  min="0" 
                  max="180" 
                  v-model.number="localConfig.music.audioStartOffset" 
                  :disabled="!localConfig.has_music || !allowedFeatures.background_music"
                  class="hue-range"
                />
                <span class="help-text text-xs text-slate-400 mt-1 block">Desplaza el deslizador para elegir en qué segundo exacto empezará a sonar la melodía al abrir la invitación (ej: el coro).</span>
              </div>
            </div>
          </div>

          <!-- TAB ESTILO -->
          <div v-if="activeTab === 'theme'" class="tab-content fade-in space-y-6">
            <!-- Bloque 1: Estructura de Secciones (Tema) -->
            <div class="space-y-3">
              <h4 class="font-extrabold text-sm text-slate-350">1. Estructura de Secciones (Tema)</h4>
              <div class="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  @click="localConfig.theme.block_style = 'glassmorphic'; saveStatus = 'unsaved';"
                  class="py-3 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1.5"
                  :class="[
                    localConfig.theme.block_style === 'glassmorphic'
                      ? 'bg-primary border-primary text-white shadow-md'
                      : 'bg-slate-900 border-slate-700/50 text-slate-400 hover:border-slate-500'
                  ]"
                >
                  <span class="text-lg">🔮</span>
                  <span>Glassmorphic</span>
                </button>
                <button
                  type="button"
                  @click="localConfig.theme.block_style = 'solid_bands'; saveStatus = 'unsaved';"
                  class="py-3 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1.5"
                  :class="[
                    localConfig.theme.block_style === 'solid_bands'
                      ? 'bg-primary border-primary text-white shadow-md'
                      : 'bg-slate-900 border-slate-700/50 text-slate-400 hover:border-slate-500'
                  ]"
                >
                  <span class="text-lg">➖</span>
                  <span>Bandas</span>
                </button>
                <button
                  type="button"
                  @click="localConfig.theme.block_style = 'minimal'; saveStatus = 'unsaved';"
                  class="py-3 px-2 rounded-xl text-xs font-bold border transition-all flex flex-col items-center gap-1.5"
                  :class="[
                    localConfig.theme.block_style === 'minimal'
                      ? 'bg-primary border-primary text-white shadow-md'
                      : 'bg-slate-900 border-slate-700/50 text-slate-400 hover:border-slate-500'
                  ]"
                >
                  <span class="text-lg">🍃</span>
                  <span>Minimalista</span>
                </button>
              </div>
            </div>

            <!-- Bloque 2: Paleta de Colores -->
            <div class="space-y-3 pt-2">
              <div class="flex justify-between items-center">
                <h4 class="font-extrabold text-sm text-slate-350">2. Paleta de Colores</h4>
                <span v-if="!allowedFeatures.custom_theme" class="text-[9px] font-black uppercase tracking-wider bg-warning/20 text-warning px-1.5 py-0.5 rounded">MODO BASIC</span>
              </div>
              
              <!-- Categorías de Paletas -->
              <div class="flex gap-1 overflow-x-auto pb-1 scrollbar-none text-[10px]">
                <button
                  type="button"
                  @click="setPaletteCategory('basic')"
                  class="px-2.5 py-1.5 rounded-lg font-bold shrink-0 transition-colors"
                  :class="selectedPaletteCategory === 'basic' ? 'bg-primary text-white' : 'bg-slate-900 text-slate-400 hover:text-white'"
                >
                  Básicos
                </button>
                <button
                  type="button"
                  @click="setPaletteCategory('pastel')"
                  class="px-2.5 py-1.5 rounded-lg font-bold shrink-0 transition-colors flex items-center gap-1"
                  :class="selectedPaletteCategory === 'pastel' ? 'bg-primary text-white' : 'bg-slate-900 text-slate-400 hover:text-white'"
                >
                  Pastel 👑
                </button>
                <button
                  type="button"
                  @click="setPaletteCategory('candy')"
                  class="px-2.5 py-1.5 rounded-lg font-bold shrink-0 transition-colors flex items-center gap-1"
                  :class="selectedPaletteCategory === 'candy' ? 'bg-primary text-white' : 'bg-slate-900 text-slate-400 hover:text-white'"
                >
                  Candy 👑
                </button>
                <button
                  type="button"
                  @click="setPaletteCategory('neon')"
                  class="px-2.5 py-1.5 rounded-lg font-bold shrink-0 transition-colors flex items-center gap-1"
                  :class="selectedPaletteCategory === 'neon' ? 'bg-primary text-white' : 'bg-slate-900 text-slate-400 hover:text-white'"
                >
                  Neón 👑
                </button>
                <button
                  type="button"
                  @click="setPaletteCategory('metallic')"
                  class="px-2.5 py-1.5 rounded-lg font-bold shrink-0 transition-colors flex items-center gap-1"
                  :class="selectedPaletteCategory === 'metallic' ? 'bg-primary text-white' : 'bg-slate-900 text-slate-400 hover:text-white'"
                >
                  Metálicos 👑
                </button>
              </div>

              <!-- Rejilla de Opciones de Paletas -->
              <div class="grid grid-cols-1 gap-2.5 max-h-[220px] overflow-y-auto pr-1">
                <div
                  v-for="p in filteredPalettes"
                  :key="p.id"
                  @click="selectColorPalette(p)"
                  class="p-3 rounded-xl border text-left transition-all cursor-pointer flex items-center justify-between group"
                  :class="[
                    localConfig.theme.palette_id === p.id
                      ? 'bg-slate-800 border-primary text-white'
                      : 'bg-slate-900/60 border-slate-700/50 hover:border-slate-600 text-slate-300'
                  ]"
                >
                  <div class="flex flex-col gap-1">
                    <span class="text-xs font-black flex items-center gap-1">
                      {{ p.name }}
                      <span v-if="p.premium && !allowedFeatures.custom_theme" class="text-[8px] font-black bg-warning/20 text-warning px-1 py-0.5 rounded">PRO</span>
                    </span>
                    <span class="text-[9px] text-slate-400 capitalize">{{ p.category }} theme</span>
                  </div>
                  
                  <!-- Vista Previa de Colores (Círculos) -->
                  <div class="flex items-center gap-1">
                    <div class="w-4 h-4 rounded-full border border-slate-950" :style="{ backgroundColor: p.colors.primary }" title="Primario"></div>
                    <div class="w-4 h-4 rounded-full border border-slate-950" :style="{ backgroundColor: p.colors.accent }" title="Acento"></div>
                    <div class="w-4 h-4 rounded-full border border-slate-950" :style="{ backgroundColor: p.colors.contentBg }" title="Fondo"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Bloque 3: Fondo del Contenido -->
            <div class="space-y-3 pt-2">
              <h4 class="font-extrabold text-sm text-slate-350">3. Fondo del Contenido</h4>
              
              <div class="form-group">
                <label>Tipo de Fondo</label>
                <select 
                  v-model="localConfig.theme.content_bg_type" 
                  @change="localConfig.theme.content_bg_texture = 'none'; saveStatus = 'unsaved';"
                  class="select-input"
                >
                  <option value="color">Color Liso de la Paleta</option>
                  <option value="texture">Textura Decorativa 👑</option>
                </select>
              </div>

              <!-- Selector de Texturas Premium -->
              <div v-if="localConfig.theme.content_bg_type === 'texture'" class="space-y-2">
                <label class="text-[10px] text-slate-400 uppercase font-black tracking-wider block">Elige la Textura</label>
                <div class="grid grid-cols-1 gap-2 max-h-[160px] overflow-y-auto pr-1">
                  <div
                    v-for="t in CONTENT_TEXTURES.filter(x => x.id !== 'none')"
                    :key="t.id"
                    @click="selectContentTexture(t)"
                    class="p-2.5 rounded-xl border text-left transition-all cursor-pointer flex items-center justify-between"
                    :class="[
                      localConfig.theme.content_bg_texture === t.id
                        ? 'bg-slate-800 border-primary text-white'
                        : 'bg-slate-900/60 border-slate-700/50 hover:border-slate-600 text-slate-400 hover:text-white'
                    ]"
                  >
                    <span class="text-xs font-extrabold flex items-center gap-1.5">
                      📄 {{ t.name }}
                      <span v-if="t.premium && !allowedFeatures.custom_theme" class="text-[8px] font-black bg-warning/20 text-warning px-1 py-0.5 rounded">PRO</span>
                    </span>
                    
                    <!-- Previsualización Mini-textura -->
                    <div 
                      class="w-8 h-8 rounded-lg border border-slate-950 shadow-inner bg-slate-900"
                      :style="t.style"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Divisores de Secciones (Mantener) -->
            <div class="form-group pt-2">
              <label>Separador de Secciones</label>
              <select v-model="localConfig.theme.divider_style" class="select-input" @change="saveStatus = 'unsaved';">
                <option value="none">Ninguno (Línea en blanco)</option>
                <option value="simple-line">Línea Minimalista</option>
                <option value="geometric-diamonds">Diamantes Geométricos</option>
                <option value="floral-twigs">Follaje & Ramas</option>
                <option value="soft-wave">Onda Suave</option>
              </select>
              <span class="help-text text-slate-500 mt-1 block">Elige el estilo visual para los divisores entre secciones del lienzo.</span>
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

          <!-- TAB DRESS CODE -->
          <div v-if="activeTab === 'dress_code'" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Código de Vestimenta</h3>
            </div>
            <p class="text-xs text-slate-400">Detalla la etiqueta o vestimenta sugerida para tus invitados.</p>

            <!-- Activar código de vestimenta -->
            <div class="flex items-center justify-between bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <div>
                <h4 class="font-bold text-sm text-slate-200">Mostrar Código de Vestimenta</h4>
                <p class="text-[10px] text-slate-400">Activa esta sección en la invitación</p>
              </div>
              <input 
                type="checkbox" 
                v-model="localConfig.has_dress_code" 
                @change="syncDressCodeVisibility"
                class="toggle toggle-primary toggle-sm"
              />
            </div>

            <div class="form-group flex flex-col gap-2">
              <label>Tipo de Código de Vestimenta</label>
              <select v-model="localConfig.dressCode.type" class="select-input" :disabled="!localConfig.has_dress_code">
                <option value="FORMAL">Formal</option>
                <option value="ETIQUETA">Etiqueta (Gala)</option>
                <option value="COCKTAIL">Cóctel</option>
                <option value="GUAYABERA">Guayabera / Clima Cálido</option>
                <option value="CASUAL">Casual</option>
                <option value="PLAYA">Playa</option>
              </select>
            </div>

            <div class="form-group flex flex-col gap-2">
              <label class="flex justify-between items-center">
                <span>Icono de Sección</span>
                <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
              </label>
              <div class="dropdown dropdown-top dropdown-end w-full" :class="{ 'pointer-events-none opacity-40': !localConfig.has_dress_code }">
                <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                  <span class="flex items-center gap-2">
                    <img v-if="localConfig.dressCode.icon && isUrl(localConfig.dressCode.icon)" :src="localConfig.dressCode.icon" class="w-6 h-6 object-contain" />
                    <span v-else class="text-lg">{{ localConfig.dressCode.icon || '👗👔' }}</span>
                    <span class="text-xs text-slate-400">Seleccionar...</span>
                  </span>
                  <span class="text-xs">▼</span>
                </div>
                <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                  <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                  <div class="grid grid-cols-5 gap-2 text-center text-xl">
                    <button 
                      v-for="emoji in ['👗👔', '👗', '👔', '👠', '👞', '👒', '🕶️', '💍', '🥂', '✉️', '🎁', '🕰️', '📅', '🕊️', '✨']" 
                      :key="emoji"
                      type="button"
                      class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                      @click="localConfig.dressCode.icon = emoji"
                    >
                      {{ emoji }}
                    </button>
                  </div>
                  <div class="border-t border-white/5 my-1"></div>
                  <div class="space-y-1.5">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                    <input 
                      v-model="localConfig.dressCode.icon" 
                      type="text" 
                      placeholder="Pegar Emoji o URL SVG/PNG" 
                      class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                      :disabled="!localConfig.has_dress_code"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group flex flex-col gap-2">
              <label>Especificaciones / Detalles Adicionales</label>
              <textarea 
                v-model="localConfig.dressCode.details" 
                placeholder="Ej: Traje oscuro caballeros y vestido largo damas..." 
                class="compact-textarea"
                rows="4"
                :disabled="!localConfig.has_dress_code"
              ></textarea>
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

          <!-- TAB SECCIONES (ESTRUCTURA) -->
          <div v-if="activeTab === 'sections'" class="tab-content fade-in space-y-4">
            <h3 class="font-extrabold text-white text-lg">Estructura de la Invitación</h3>
            <p class="text-xs text-slate-400">Arrastra para reordenar cómo aparecerán los bloques de arriba a abajo. Prende o apaga según tu plan.</p>
            
            <div class="flex flex-col gap-3 mt-4">
              <div 
                v-for="(block, index) in localConfig.blocks" 
                :key="block.id"
                class="flex items-center justify-between p-4 rounded-2xl border transition-all duration-300 select-none"
                :class="[
                  block.visible ? 'bg-slate-900 border-slate-700/50 text-white' : 'bg-slate-950 border-slate-800/30 text-slate-500',
                  block.locked ? 'cursor-not-allowed opacity-75' : 'cursor-move hover:border-primary/50'
                ]"
                :draggable="!block.locked"
                @dragstart="onDragStart($event, index)"
                @dragover.prevent
                @drop="onDrop($event, index)"
              >
                <div class="flex items-center gap-3">
                  <span class="text-slate-400 font-bold" v-if="!block.locked">☰</span>
                  <span class="font-bold text-sm">{{ block.name }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span v-if="block.configKey && !allowedFeatures[block.id === 'timer' ? 'countdown_timer' : block.id]" class="text-[8px] font-black uppercase tracking-wider bg-warning/20 text-warning px-1.5 py-0.5 rounded">PRO</span>
                  <!-- Botón de eliminar para bloques dinámicos -->
                  <button 
                    v-if="!block.locked && (block.id.startsWith('protocol_words_') || block.id.startsWith('invitation_text_'))" 
                    type="button" 
                    @click.stop="block.id.startsWith('protocol_words_') ? deleteProtocolBlock(block.id) : deleteThoughtsBlock(block.id)"
                    class="text-rose-500 hover:text-rose-450 font-bold text-xs p-1 mr-1"
                    title="Eliminar Sección"
                  >
                    🗑️
                  </button>

                  <input 
                    v-if="block.configKey"
                    type="checkbox" 
                    v-model="localConfig[block.configKey]"
                    @change="toggleBlockVisibility(block)"
                    class="toggle toggle-primary toggle-xs"
                  />
                  <input 
                    v-else-if="block.id.startsWith('protocol_words_') || block.id.startsWith('invitation_text_')"
                    type="checkbox" 
                    v-model="block.visible"
                    class="toggle toggle-primary toggle-xs"
                  />
                  <span v-else class="text-[9px] font-black text-primary uppercase tracking-widest">FIJO</span>
                </div>
              </div>
            </div>

            <button 
              type="button" 
              @click="addProtocolBlock" 
              class="w-full mt-2 py-2.5 border border-dashed border-slate-700 hover:border-slate-500 hover:bg-slate-900/60 text-slate-400 hover:text-white rounded-xl text-xs font-bold transition-all mb-2"
            >
              ➕ Agregar Sección Protocolar
            </button>
            <button 
              type="button" 
              @click="addThoughtsBlock" 
              class="w-full py-2.5 border border-dashed border-slate-700 hover:border-slate-500 hover:bg-slate-900/60 text-slate-400 hover:text-white rounded-xl text-xs font-bold transition-all"
            >
              ➕ Agregar Pensamiento / Texto
            </button>
          </div>

          <!-- TAB REGALOS (MESA DE REGALOS) -->
          <div v-if="activeTab === 'gift'" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Mesa de Regalos</h3>
              <span v-if="!allowedFeatures.gift_table" class="badge badge-warning text-[9px] font-black py-1 px-2 uppercase">PRO</span>
            </div>

            <!-- PRO OVERLAY BLOCK -->
            <div v-if="!allowedFeatures.gift_table" class="bg-warning/10 border border-warning/20 p-4 rounded-2xl flex flex-col gap-3">
              <p class="text-xs text-warning leading-relaxed font-semibold">Esta función está bloqueada en tu plan básico/estándar. Actualiza para permitir transferencias bancarias y enlaces a tiendas como Liverpool o Amazon.</p>
              <button @click="showUpgradeModal = true" class="btn btn-warning btn-xs rounded-xl font-bold py-1.5 w-full uppercase">Comprar Plan Premium</button>
            </div>

            <div :class="{ 'opacity-40 pointer-events-none': !allowedFeatures.gift_table }" class="space-y-4">
              <!-- Activar mesa en el formulario -->
              <div class="flex items-center justify-between bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                <div>
                  <h4 class="font-bold text-sm text-slate-200">Mostrar Mesa de Regalos</h4>
                  <p class="text-[10px] text-slate-400">Activa esta sección en la invitación</p>
                </div>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_gift_table" 
                  @change="syncGiftTableVisibility"
                  class="toggle toggle-primary toggle-sm"
                  :disabled="!allowedFeatures.gift_table"
                />
              </div>

              <div class="form-group">
                <label>Título de la Sección</label>
                <input v-model="localConfig.gift_table.title" type="text" placeholder="Ej: Mesa de Regalos" :disabled="!allowedFeatures.gift_table || !localConfig.has_gift_table" />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label class="flex justify-between items-center">
                  <span>Icono de Sección</span>
                  <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
                </label>
                <div class="dropdown dropdown-top dropdown-end w-full" :class="{ 'pointer-events-none opacity-40': !allowedFeatures.gift_table || !localConfig.has_gift_table }">
                  <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                    <span class="flex items-center gap-2">
                      <img v-if="localConfig.gift_table.icon && isUrl(localConfig.gift_table.icon)" :src="localConfig.gift_table.icon" class="w-6 h-6 object-contain" />
                      <span v-else class="text-lg">{{ localConfig.gift_table.icon || '🎁' }}</span>
                      <span class="text-xs text-slate-400">Seleccionar...</span>
                    </span>
                    <span class="text-xs">▼</span>
                  </div>
                  <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                    <div class="grid grid-cols-5 gap-2 text-center text-xl">
                      <button 
                        v-for="emoji in ['🎁', '🏦', '🛍️', '💵', '💳', '💍', '🥂', '✉️', '👗', '📍', '🕰️', '📅', '🕊️', '✨', '🍽️']" 
                        :key="emoji"
                        type="button"
                        class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                        @click="localConfig.gift_table.icon = emoji"
                      >
                        {{ emoji }}
                      </button>
                    </div>
                    <div class="border-t border-white/5 my-1"></div>
                    <div class="space-y-1.5">
                      <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                      <input 
                        v-model="localConfig.gift_table.icon" 
                        type="text" 
                        placeholder="Pegar Emoji o URL SVG/PNG" 
                        class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                        :disabled="!allowedFeatures.gift_table || !localConfig.has_gift_table"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>Descripción / Mensaje</label>
                <textarea v-model="localConfig.gift_table.description" placeholder="Escribe un mensaje para tus invitados..." :disabled="!allowedFeatures.gift_table || !localConfig.has_gift_table" rows="3"></textarea>
              </div>

              <!-- Cuentas Bancarias List -->
              <div class="space-y-3 pt-2">
                <div class="flex justify-between items-center">
                  <h4 class="font-extrabold text-sm text-slate-300">Cuentas para Transferencia</h4>
                  <button @click="addBankAccount" :disabled="!allowedFeatures.gift_table || !localConfig.has_gift_table" class="btn btn-ghost btn-xs text-primary font-bold">+ Agregar</button>
                </div>
                
                <div v-for="(acc, idx) in localConfig.gift_table.bank_accounts" :key="idx" class="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3 relative">
                  <button @click="removeBankAccount(idx)" class="absolute top-2 right-2 text-error hover:text-error-focus text-xs">✕</button>
                  <div class="grid grid-cols-2 gap-2">
                    <div class="form-group">
                      <label class="text-[10px] uppercase font-bold text-slate-400">Banco</label>
                      <input v-model="acc.bank" type="text" placeholder="Ej: BBVA" class="input-xs bg-slate-900 border-slate-800 text-white rounded" />
                    </div>
                    <div class="form-group">
                      <label class="text-[10px] uppercase font-bold text-slate-400">Titular</label>
                      <input v-model="acc.holder" type="text" placeholder="Ej: Juan Pérez" class="input-xs bg-slate-900 border-slate-800 text-white rounded" />
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="text-[10px] uppercase font-bold text-slate-400">Número CLABE (18 dígitos)</label>
                    <input v-model="acc.clabe" type="text" placeholder="0123..." class="input-xs font-mono bg-slate-900 border-slate-800 text-white rounded" maxlength="18" />
                  </div>
                </div>
              </div>

              <!-- Tiendas Registries List -->
              <div class="space-y-3 pt-4">
                <div class="flex justify-between items-center">
                  <h4 class="font-extrabold text-sm text-slate-300">Mesas de Regalos en Tiendas</h4>
                  <button @click="addGiftRegistry" :disabled="!allowedFeatures.gift_table || !localConfig.has_gift_table" class="btn btn-ghost btn-xs text-primary font-bold">+ Agregar</button>
                </div>
                
                <div v-for="(reg, idx) in localConfig.gift_table.gift_registries" :key="idx" class="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3 relative">
                  <button @click="removeGiftRegistry(idx)" class="absolute top-2 right-2 text-error hover:text-error-focus text-xs">✕</button>
                  <div class="grid grid-cols-2 gap-2">
                    <div class="form-group">
                      <label class="text-[10px] uppercase font-bold text-slate-400">Tienda</label>
                      <input v-model="reg.store" type="text" placeholder="Ej: Liverpool" class="input-xs bg-slate-900 border-slate-800 text-white rounded" />
                    </div>
                    <div class="form-group">
                      <label class="text-[10px] uppercase font-bold text-slate-400">ID Evento (Opcional)</label>
                      <input v-model="reg.event_id" type="text" placeholder="Ej: 501234" class="input-xs bg-slate-900 border-slate-800 text-white rounded" />
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="text-[10px] uppercase font-bold text-slate-400">URL del Registro</label>
                    <input v-model="reg.url" type="url" placeholder="https://..." class="input-xs font-mono bg-slate-900 border-slate-800 text-white rounded" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB GALERÍA (FOTOS) -->
          <div v-if="activeTab === 'gallery'" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Galería de Fotos</h3>
              <span v-if="!allowedFeatures.photo_carousel" class="badge badge-warning text-[9px] font-black py-1 px-2 uppercase">PRO</span>
            </div>

            <!-- PRO OVERLAY BLOCK -->
            <div v-if="!allowedFeatures.photo_carousel" class="bg-warning/10 border border-warning/20 p-4 rounded-2xl flex flex-col gap-3">
              <p class="text-xs text-warning leading-relaxed font-semibold">Esta función está bloqueada en tu plan básico/estándar. Actualiza para permitir desplegar un hermoso carrusel fotográfico de tu historia de amor.</p>
              <button @click="showUpgradeModal = true" class="btn btn-warning btn-xs rounded-xl font-bold py-1.5 w-full uppercase">Comprar Plan Premium</button>
            </div>

            <div :class="{ 'opacity-40 pointer-events-none': !allowedFeatures.photo_carousel }" class="space-y-4">
              <!-- Activar galería -->
              <div class="flex items-center justify-between bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                <div>
                  <h4 class="font-bold text-sm text-slate-200">Mostrar Galería</h4>
                  <p class="text-[10px] text-slate-400">Activa esta sección en la invitación</p>
                </div>
                <input 
                  type="checkbox" 
                  v-model="localConfig.has_photo_carousel" 
                  @change="syncPhotoCarouselVisibility"
                  class="toggle toggle-primary toggle-sm"
                  :disabled="!allowedFeatures.photo_carousel"
                />
              </div>

              <div class="form-group">
                <label>Título de la Sección</label>
                <input v-model="localConfig.photo_carousel.title" type="text" placeholder="Ej: Nuestra Historia" :disabled="!allowedFeatures.photo_carousel || !localConfig.has_photo_carousel" />
              </div>

              <div class="form-group">
                <label>Descripción (Opcional)</label>
                <input v-model="localConfig.photo_carousel.description" type="text" placeholder="Ej: Momentos especiales" :disabled="!allowedFeatures.photo_carousel || !localConfig.has_photo_carousel" />
              </div>

              <!-- Input para agregar nueva imagen URL -->
              <div class="space-y-2 pt-2">
                <label class="font-bold text-xs text-slate-300 block">Agregar Enlace de Imagen (URL)</label>
                <div class="flex gap-2">
                  <input 
                    v-model="newImageUrl" 
                    type="url" 
                    placeholder="https://images.unsplash.com/..." 
                    class="input-xs w-full font-mono bg-slate-950 border-slate-800 text-white rounded-xl h-9 px-3"
                    :disabled="!allowedFeatures.photo_carousel || !localConfig.has_photo_carousel"
                    @keyup.enter="addImageUrl"
                  />
                  <button 
                    @click="addImageUrl" 
                    :disabled="!allowedFeatures.photo_carousel || !localConfig.has_photo_carousel || !newImageUrl"
                    class="btn btn-primary btn-xs h-9 rounded-xl font-bold px-4"
                  >
                    + Agregar
                  </button>
                </div>
                <p class="text-[10px] text-slate-400 leading-normal">Pega la URL de una foto guardada en la web (ej: Unsplash, Pinterest, tu drive público, etc.).</p>
              </div>

              <!-- Input para subir imágenes locales -->
              <div class="space-y-2 pt-2">
                <label class="font-bold text-xs text-slate-300 block">Subir Fotos desde tu dispositivo</label>
                <div class="flex gap-2 items-center">
                  <input 
                    type="file" 
                    multiple 
                    accept="image/*"
                    @change="uploadImages"
                    class="file-input file-input-bordered file-input-xs w-full bg-slate-950 border-slate-800 text-white"
                    :disabled="!allowedFeatures.photo_carousel || !localConfig.has_photo_carousel || isUploading"
                  />
                  <span v-if="isUploading" class="loading loading-spinner loading-xs text-primary"></span>
                </div>
                <p class="text-[10px] text-slate-400 leading-normal">Selecciona una o más fotos para subirlas y agregarlas a tu galería.</p>
              </div>

              <!-- Listado de imágenes agregadas -->
              <div class="space-y-3 pt-4">
                <h4 class="font-extrabold text-sm text-slate-300">Imágenes Agregadas ({{ localConfig.photo_carousel.images ? localConfig.photo_carousel.images.length : 0 }})</h4>
                
                <div v-if="!localConfig.photo_carousel.images || localConfig.photo_carousel.images.length === 0" class="text-center py-6 text-xs text-slate-500 font-medium">
                  Aún no has agregado enlaces de imágenes.
                </div>

                <div v-else class="grid grid-cols-2 gap-3">
                  <div 
                    v-for="(imgUrl, idx) in localConfig.photo_carousel.images" 
                    :key="idx" 
                    class="bg-slate-950 p-2 rounded-2xl border border-slate-800 flex flex-col gap-2 relative group"
                  >
                    <div class="aspect-video w-full rounded-lg overflow-hidden bg-slate-900 border border-slate-800">
                      <img :src="imgUrl" class="object-cover w-full h-full" alt="Miniatura" />
                    </div>
                    <p class="text-[10px] font-mono text-slate-500 truncate w-full select-all px-1">{{ imgUrl }}</p>
                    <button 
                      @click="removeImageUrl(idx)" 
                      class="absolute top-4 right-4 bg-error text-white font-bold rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-error-focus opacity-0 group-hover:opacity-100 transition-opacity shadow"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB DINÁMICA: PALABRAS PROTOCOLARES -->
          <div v-if="activeTab.startsWith('protocol_words_')" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Palabras Protocolares</h3>
              <button 
                type="button" 
                @click="deleteProtocolBlock(activeTab)"
                class="btn btn-error btn-xs rounded-xl font-bold px-3 py-1"
              >
                🗑️ Eliminar Sección
              </button>
            </div>

            <div class="space-y-4">
              <div class="form-group">
                <label>Título del Bloque</label>
                <input 
                  v-model="localConfig[activeTab].title" 
                  type="text" 
                  placeholder="Ej: Nuestros Padres" 
                  @input="updateBlockName(activeTab, localConfig[activeTab].title)"
                />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label class="flex justify-between items-center">
                  <span>Icono de Sección</span>
                  <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
                </label>
                <div class="dropdown dropdown-top dropdown-end w-full">
                  <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                    <span class="flex items-center gap-2">
                      <img v-if="localConfig[activeTab].icon && isUrl(localConfig[activeTab].icon)" :src="localConfig[activeTab].icon" class="w-6 h-6 object-contain" />
                      <span v-else class="text-lg">{{ localConfig[activeTab].icon || '📜' }}</span>
                      <span class="text-xs text-slate-400">Seleccionar...</span>
                    </span>
                    <span class="text-xs">▼</span>
                  </div>
                  <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                    <div class="grid grid-cols-5 gap-2 text-center text-xl">
                      <button 
                        v-for="emoji in ['📜', '👑', '🕊️', '✨', '💍', '🥂', '✉️', '👗', '📍', '🎁', '🕰️', '📅', '📸', '🎵', '⛪']" 
                        :key="emoji"
                        type="button"
                        class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                        @click="localConfig[activeTab].icon = emoji"
                      >
                        {{ emoji }}
                      </button>
                    </div>
                    <div class="border-t border-white/5 my-1"></div>
                    <div class="space-y-1.5">
                      <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                      <input 
                        v-model="localConfig[activeTab].icon" 
                        type="text" 
                        placeholder="Pegar Emoji o URL SVG/PNG" 
                        class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>Descripción / Dedicatoria</label>
                <textarea 
                  v-model="localConfig[activeTab].description" 
                  placeholder="Ej: Con la bendición de Dios y de nuestros padres..." 
                  class="compact-textarea"
                ></textarea>
              </div>

              <!-- Filas de Personas -->
              <div class="space-y-4 pt-2">
                <div class="flex justify-between items-center">
                  <h4 class="font-extrabold text-sm text-slate-350">Filas de Personas / Roles</h4>
                  <button 
                    type="button" 
                    @click="addProtocolRow(activeTab)" 
                    class="text-xs font-bold text-primary hover:underline"
                  >
                    ➕ Añadir Fila
                  </button>
                </div>

                <div 
                  v-for="(col, idx) in localConfig[activeTab].columns" 
                  :key="idx" 
                  class="p-4 bg-slate-900/60 rounded-2xl border border-slate-700/50 space-y-3 relative"
                >
                  <button 
                    type="button" 
                    @click="removeProtocolRow(activeTab, idx)" 
                    class="absolute top-3 right-3 text-rose-500 hover:text-rose-450 text-xs font-bold"
                    title="Eliminar Fila"
                  >
                    🗑️
                  </button>

                  <div class="form-group">
                    <label>Rol / Título (ej: Padres, Padrinos)</label>
                    <input 
                      v-model="col.role" 
                      type="text" 
                      placeholder="Ej: Padres de la Novia" 
                      class="compact-input"
                    />
                  </div>

                  <div class="form-group">
                    <label>Nombres (pueden ser varios)</label>
                    <textarea 
                      v-model="col.names" 
                      placeholder="Ej: Juan Pérez y María Gómez" 
                      class="compact-textarea"
                    ></textarea>
                  </div>
                </div>

                <div v-if="!localConfig[activeTab].columns || localConfig[activeTab].columns.length === 0" class="text-center py-6 text-xs text-slate-500 font-medium bg-slate-950/40 rounded-2xl border border-dashed border-slate-800">
                  No hay filas configuradas. Añade una para mostrar nombres.
                </div>
              </div>
            </div>
          </div>

          <!-- TAB DINÁMICA: PENSAMIENTOS / TEXTO DE INVITACIÓN -->
          <div v-if="activeTab.startsWith('invitation_text_') || activeTab === 'invitation_text'" class="tab-content fade-in space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-white text-lg">Texto de Invitación</h3>
              <button 
                type="button" 
                @click="deleteThoughtsBlock(activeTab)"
                class="btn btn-error btn-xs rounded-xl font-bold px-3 py-1"
              >
                🗑️ Eliminar Sección
              </button>
            </div>

            <div class="space-y-4">
              <div class="form-group">
                <label>Título del Bloque</label>
                <input 
                  v-model="localConfig[activeTab].title" 
                  type="text" 
                  placeholder="Ej: Pensamiento / Verso" 
                  @input="updateThoughtsBlockName(activeTab, localConfig[activeTab].title)"
                />
              </div>

              <div class="form-group flex flex-col gap-2">
                <label class="flex justify-between items-center">
                  <span>Icono de Sección</span>
                  <span class="text-[10px] text-slate-400">Emoji o URL SVG</span>
                </label>
                <div class="dropdown dropdown-top dropdown-end w-full">
                  <div tabindex="0" role="button" class="btn btn-outline border-white/10 w-full flex items-center justify-between px-3 h-[42px] bg-white/5 hover:bg-white/10 text-white rounded-xl">
                    <span class="flex items-center gap-2">
                      <img v-if="localConfig[activeTab].icon && isUrl(localConfig[activeTab].icon)" :src="localConfig[activeTab].icon" class="w-6 h-6 object-contain" />
                      <span v-else class="text-lg">{{ localConfig[activeTab].icon || '✨' }}</span>
                      <span class="text-xs text-slate-400">Seleccionar...</span>
                    </span>
                    <span class="text-xs">▼</span>
                  </div>
                  <div tabindex="0" class="dropdown-content menu p-4 shadow-2xl bg-slate-950 border border-white/10 rounded-2xl w-[280px] z-[100] gap-3">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Emojis sugeridos</span>
                    <div class="grid grid-cols-5 gap-2 text-center text-xl">
                      <button 
                        v-for="emoji in ['✨', '🕊️', '💍', '🥂', '✉️', '👗', '📍', '🎁', '🕰️', '📅', '📸', '🎵', '⛪', '📜', '🍽️']" 
                        :key="emoji"
                        type="button"
                        class="p-1.5 hover:bg-white/10 rounded-lg active:scale-95 transition-all text-slate-200"
                        @click="localConfig[activeTab].icon = emoji"
                      >
                        {{ emoji }}
                      </button>
                    </div>
                    <div class="border-t border-white/5 my-1"></div>
                    <div class="space-y-1.5">
                      <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Personalizado</span>
                      <input 
                        v-model="localConfig[activeTab].icon" 
                        type="text" 
                        placeholder="Pegar Emoji o URL SVG/PNG" 
                        class="input input-sm border-white/15 bg-white/5 h-8 rounded-lg text-xs w-full focus:border-primary text-slate-200"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <div class="flex justify-between items-center">
                  <label>Frase / Texto de Invitación</label>
                  <span 
                    class="text-[10px] font-bold" 
                    :class="getWordCount(localConfig[activeTab]?.text || '') > 100 ? 'text-rose-500 font-extrabold' : 'text-slate-400'"
                  >
                    Palabras: {{ getWordCount(localConfig[activeTab]?.text || '') }} / 100
                  </span>
                </div>
                <textarea 
                  v-model="localConfig[activeTab].text" 
                  placeholder="Ej: Familia tal y tal se enorgullece en invitarlo a usted y su apreciable familia..." 
                  class="compact-textarea"
                  rows="6"
                  @input="validateThoughtsText(activeTab)"
                ></textarea>
                <p v-if="getWordCount(localConfig[activeTab]?.text || '') > 100" class="text-rose-500 text-[10px] font-extrabold">
                  ⚠️ Has excedido el límite de 100 palabras. Por favor reduce el texto para evitar problemas de diseño.
                </p>
              </div>

              <!-- Align Options -->
              <div class="form-group">
                <label>Alineación del Texto</label>
                <select v-model="localConfig[activeTab].align" class="select select-bordered w-full rounded-2xl bg-slate-900 border-slate-700 text-white h-12 text-sm font-semibold">
                  <option value="center">Centrado</option>
                  <option value="left">Alineado a la izquierda</option>
                  <option value="right">Alineado a la derecha</option>
                </select>
              </div>

              <!-- Font Style Options -->
              <div class="form-group">
                <label>Estilo de Fuente</label>
                <select v-model="localConfig[activeTab].fontStyle" class="select select-bordered w-full rounded-2xl bg-slate-900 border-slate-700 text-white h-12 text-sm font-semibold">
                  <option value="serif">Serif (Elegante y Clásico)</option>
                  <option value="sans">Sans-serif (Moderno y Limpio)</option>
                </select>
              </div>
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
                  :tierLevel="localConfig.rsvp.tier || productTier"
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
                :tierLevel="localConfig.rsvp.tier || productTier"
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

    <!-- Modal de Galería de Recursos Gráficos -->
    <GraphicsGalleryModal 
      v-if="isGalleryOpen" 
      :isOpen="isGalleryOpen" 
      @close="isGalleryOpen = false" 
      @select-background="handleSelectBackground"
      @select-frame="handleSelectFrame"
    />

    <!-- Modal de Galería de Música Jamendo -->
    <MusicGalleryModal
      v-if="isMusicGalleryOpen"
      :isOpen="isMusicGalleryOpen"
      @close="isMusicGalleryOpen = false"
      @select-audio="handleSelectAudio"
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

    <!-- Modal de Confirmación Genérico (Premium) -->
    <div v-if="confirmModal.show" class="fixed inset-0 z-[200] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="confirmModal.show = false"></div>
      <div class="relative w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 md:p-8 flex flex-col gap-6 border border-slate-100 overflow-hidden text-center">
        <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-pink-500 to-indigo-600"></div>
        
        <div class="space-y-2 mt-2">
          <span class="text-4xl block">{{ confirmModal.emoji }}</span>
          <h3 class="text-xl font-black text-slate-800">{{ confirmModal.title }}</h3>
          <p class="text-slate-500 text-xs sm:text-sm whitespace-pre-line">
            {{ confirmModal.message }}
          </p>
        </div>

        <div class="flex gap-3 pt-2">
          <button 
            type="button" 
            @click="confirmModal.show = false" 
            class="btn btn-outline border-slate-200 text-slate-500 hover:bg-slate-50 flex-1 py-2.5 rounded-xl font-bold text-sm transition-all"
          >
            {{ confirmModal.cancelText }}
          </button>
          <button 
            type="button" 
            @click="handleConfirmModalAction" 
            class="btn bg-indigo-600 hover:bg-indigo-700 text-white flex-1 py-2.5 rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition-all"
          >
            {{ confirmModal.confirmText }}
          </button>
        </div>
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
import GraphicsGalleryModal from '@/modules/builder/components/GraphicsGalleryModal.vue';
import MusicGalleryModal from '@/modules/builder/components/MusicGalleryModal.vue';
import { COLOR_PALETTES, CONTENT_TEXTURES } from '@/modules/builder/constants/palettes';

// Variables de estado adicionales v0.8.4
const productTier = ref('BASIC');
const isUrl = (val) => {
  if (!val) return false;
  return val.startsWith('http') || val.startsWith('/') || val.startsWith('.') || val.includes('/');
};
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

// Modal de confirmación premium reusable
const confirmModal = ref({
  show: false,
  title: '',
  message: '',
  emoji: '⚠️',
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  onConfirm: null
});

const openConfirmModal = (options) => {
  confirmModal.value = {
    show: true,
    title: options.title || '¿Estás seguro?',
    message: options.message || '',
    emoji: options.emoji || '⚠️',
    confirmText: options.confirmText || 'Confirmar',
    cancelText: options.cancelText || 'Cancelar',
    onConfirm: options.onConfirm
  };
};

const handleConfirmModalAction = async () => {
  const callback = confirmModal.value.onConfirm;
  confirmModal.value.show = false;
  if (callback) {
    await callback();
  }
};


const route = useRoute();
const router = useRouter();
let authStore = null;
try {
  authStore = useAuthStore();
} catch (e) {
  // Silent fallback for unit testing environments without active Pinia
}
const isAdminOrDesigner = computed(() => {
  return authStore?.role === 'ADMIN' || authStore?.role === 'DESIGNER';
});
const toast = useToast();
const deploymentId = route.params.id;

const loading = ref(true);
const saveStatus = ref('saved'); // 'saved', 'unsaved', 'saving', 'error'
const activeTab = ref('cover'); // 'cover', 'rsvp', 'timer', 'timeline', 'music', 'theme', 'og', 'envelope'
const showMobilePreview = ref(false);
const showUpgradeModal = ref(false);
const showSuccessModal = ref(false);

const isGalleryOpen = ref(false);
const handleSelectBackground = (url) => {
  localConfig.value.cover.coverPhoto = url;
};
const handleSelectFrame = (url) => {
  localConfig.value.cover.frame_overlay = url;
};

const isMusicGalleryOpen = ref(false);
const handleSelectAudio = (url) => {
  localConfig.value.audioUrl = url;
  syncAudioUrl();
  if (localConfig.value.music) {
    localConfig.value.music.audioStartOffset = 0;
  }
};

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

const defaultBlocks = [
  { id: 'cover', type: 'CoverBlock', name: '🌅 Portada del Evento', visible: true, locked: true },
  { id: 'timer', type: 'CountdownTimer', name: '🕰️ Cuenta Regresiva', visible: false, configKey: 'has_timer' },
  { id: 'location', type: 'LocationBlock', name: '📍 Ubicación del Evento', visible: false, configKey: 'has_location' },
  { id: 'rsvp', type: 'RsvpFormBlock', name: '✉️ Confirmación RSVP', visible: true, locked: true },
  { id: 'dress_code', type: 'DressCodeBlock', name: '👗 Código de Vestimenta', visible: false, configKey: 'has_dress_code' },
  { id: 'timeline', type: 'TimelineBlock', name: '📅 Cronograma / Itinerario', visible: false, configKey: 'has_timeline' },
  { id: 'gift_table', type: 'GiftTableBlock', name: '🎁 Mesa de Regalos', visible: false, configKey: 'has_gift_table' },
  { id: 'photo_carousel', type: 'PhotoCarouselBlock', name: '📸 Galería de Fotos', visible: false, configKey: 'has_photo_carousel' }
];

const allowedFeatures = ref({
  background_music: false,
  custom_audio_url: false,
  countdown_timer: false,
  timeline: false,
  custom_theme: false,
  custom_og: false,
  gift_table: false,
  photo_carousel: false,
  location: true,
  dress_code: true,
});
const deploymentSlug = ref('');
const deploymentStatus = ref('DRAFT');

const protocolBlocks = computed(() => {
  return localConfig.value.blocks ? localConfig.value.blocks.filter(b => b.id && b.id.startsWith('protocol_words_')) : [];
});

const thoughtsBlocks = computed(() => {
  return localConfig.value.blocks ? localConfig.value.blocks.filter(b => b.id && b.id.startsWith('invitation_text_')) : [];
});

// Estructura por defecto en caso de que esté vacío
const localConfig = ref({
  cover: {
    title: '',
    subtitle: '',
    date: '',
    coverPhoto: '',
    titleColor: '#ffffff',
    subtitleColor: '#e2e8f0',
    headerLabelColor: '#fbbf24',
    dateColor: '#ffffff',
    overlayOpacity: 70,
    titleSize: 4.5,
    headerLabel: 'Nuestra Invitación',
    fontFamily: 'serif',
    frame_overlay: null,
    backgroundPositionX: 50,
    backgroundPositionY: 50
  },
  rsvp: {
    bgColor: '#f8fafc',
    btnColor: '#3b82f6',
    title: 'Confirma tu Asistencia',
    subtitle: 'Nos encantaría contar con tu presencia.',
    whatsappPhone: '',
    tier: 'BASIC'
  },
  has_location: false,
  location: {
    title: 'Ubicación del Evento',
    venueName: '',
    address: '',
    googleMapsUrl: '',
    zoom: 14
  },
  locations: {
    ceremonyName: '',
    ceremonyMapsUrl: '',
    receptionName: '',
    receptionMapsUrl: ''
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
    has_music: false,
    audioStartOffset: 0
  },
  theme: {
    hue: 38,
    saturation: '80%',
    lightness: '50%',
    divider_style: 'none',
    block_style: 'glassmorphic',
    palette_id: 'classic_navy',
    content_bg_type: 'color',
    content_bg_texture: 'none'
  },
  og_title: '',
  og_description: '',
  og_image: '',
  envelope_type: null,
  envelope: null,
  has_gift_table: false,
  gift_table: {
    title: 'Mesa de Regalos',
    description: 'Tu presencia es nuestro mejor regalo, pero si deseas tener un detalle con nosotros...',
    bank_accounts: [],
    gift_registries: []
  },
  has_photo_carousel: false,
  photo_carousel: {
    title: 'Nuestra Galería',
    description: '',
    images: []
  },
  has_dress_code: false,
  dressCode: {
    type: 'FORMAL',
    details: ''
  },
  blocks: []
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

      if (res.data.creation_mode === 'CATALOG' && !isAdminOrDesigner.value) {
        router.replace(`/builder/${deploymentId}/form`);
        return;
      }
      
      if (authStore?.role === 'ADMIN') {
        try {
          const storesRes = await crmService.fetchAllStores();
          storesList.value = storesRes.data || [];
        } catch (e) {
          console.error("Error al cargar tiendas:", e);
        }
      }
      
      if (isAdminOrDesigner.value) {
        allowedFeatures.value = {
          background_music: true,
          custom_audio_url: true,
          countdown_timer: true,
          timeline: true,
          custom_theme: true,
          custom_og: true,
          gift_table: true,
          photo_carousel: true,
          location: true,
          dress_code: true,
        };
      } else if (res.data.allowed_features) {
        allowedFeatures.value = {
          ...allowedFeatures.value,
          ...res.data.allowed_features
        };
      }

      
      const custom = res.data.custom_data;
      if (custom && Object.keys(custom).length > 0) {
        // Fusionar datos existentes para no romper la reactividad profunda
        localConfig.value.cover = { ...localConfig.value.cover, ...(custom.cover || {}) };
        localConfig.value.rsvp = { ...localConfig.value.rsvp, ...(custom.rsvp || {}) };
        if (!localConfig.value.rsvp.tier) {
          localConfig.value.rsvp.tier = res.data.product_tier || 'BASIC';
        }
        
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
        if (custom.gift_table) {
          localConfig.value.gift_table = { ...localConfig.value.gift_table, ...custom.gift_table };
        }
        if (custom.photo_carousel) {
          localConfig.value.photo_carousel = { ...localConfig.value.photo_carousel, ...custom.photo_carousel };
        }
        if (custom.location) {
          localConfig.value.location = { ...localConfig.value.location, ...custom.location };
        }
        if (custom.locations) {
          localConfig.value.locations = { ...localConfig.value.locations, ...custom.locations };
        }
        if (custom.dressCode) {
          localConfig.value.dressCode = { ...localConfig.value.dressCode, ...custom.dressCode };
        }

        // Copiar dinámicamente claves de palabras protocolares y pensamientos
        Object.keys(custom).forEach(key => {
          if (key.startsWith('protocol_words_') || key.startsWith('invitation_text_')) {
            localConfig.value[key] = custom[key];
          }
        });
        
        // Copiar otros campos planos
        localConfig.value.has_timer = custom.has_timer ?? false;
        localConfig.value.has_timeline = custom.has_timeline ?? false;
        localConfig.value.has_music = custom.has_music ?? false;
        localConfig.value.has_gift_table = custom.has_gift_table ?? false;
        localConfig.value.has_photo_carousel = custom.has_photo_carousel ?? false;
        localConfig.value.has_location = custom.has_location ?? false;
        localConfig.value.has_dress_code = custom.has_dress_code ?? !!(custom.dressCode?.type);
        localConfig.value.audioUrl = custom.audioUrl ?? '';
        localConfig.value.og_title = custom.og_title ?? '';
        localConfig.value.og_description = custom.og_description ?? '';
        localConfig.value.og_image = custom.og_image ?? '';
        localConfig.value.envelope_type = custom.envelope_type ?? custom.envelope ?? null;
        localConfig.value.envelope = custom.envelope_type ?? custom.envelope ?? null;

        // Cargar blocks dinámicos o inicializar fallback
        if (Array.isArray(custom.blocks)) {
          const loadedBlocks = custom.blocks.map(b => {
            const db = defaultBlocks.find(d => d.id === b.id);
            return { ...db, ...b };
          }).filter(b => b.id);
          
          // Asegurar que cualquier block nuevo por defecto (ej: location) esté presente en localConfig
          const missingBlocks = defaultBlocks.filter(db => !loadedBlocks.some(lb => lb.id === db.id));
          localConfig.value.blocks = [...loadedBlocks, ...missingBlocks];
        } else {
          localConfig.value.blocks = defaultBlocks.map(db => {
            let visible = db.visible;
            if (db.id === 'timer') visible = custom.has_timer ?? false;
            if (db.id === 'timeline') visible = custom.has_timeline ?? false;
            if (db.id === 'gift_table') visible = custom.has_gift_table ?? false;
            if (db.id === 'photo_carousel') visible = custom.has_photo_carousel ?? false;
            if (db.id === 'location') visible = custom.has_location ?? false;
            if (db.id === 'dress_code') visible = custom.has_dress_code ?? !!(custom.dressCode?.type);
            return { ...db, visible };
          });
        }
      } else {
        // Inicializar blocks por defecto en invitaciones vacías
        localConfig.value.blocks = [...defaultBlocks];
        localConfig.value.rsvp.tier = res.data.product_tier || 'BASIC';
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
    confirmRequestReview();
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

const confirmRequestReview = () => {
  openConfirmModal({
    title: 'Solicitar Revisión',
    message: '¿Estás seguro de que deseas enviar este diseño a revisión por el administrador? Se notificará al equipo de control de calidad para su aprobación.',
    emoji: '📨',
    confirmText: 'Enviar a Revisión',
    cancelText: 'Cancelar',
    onConfirm: async () => {
      try {
        await builderService.requestReview(deploymentId);
        toast.success('Solicitud de revisión enviada al administrador.');
      } catch (error) {
        const errMsg = error.response?.data?.error || 'Error al enviar la solicitud de revisión.';
        toast.error(errMsg);
      }
    }
  });
};

const confirmPublishPaid = () => {
  openConfirmModal({
    title: 'Publicar Invitación',
    message: '¿Estás seguro de que deseas poner tu invitación en vivo? Esto la hará accesible para todos tus invitados.',
    emoji: '🚀',
    confirmText: 'Publicar Ahora',
    cancelText: 'Cancelar',
    onConfirm: async () => {
      try {
        await builderService.updateDeployment(deploymentId, { status: 'LIVE' });
        deploymentStatus.value = 'LIVE';
        toast.success('¡Tu invitación está En Vivo!');
      } catch (e) {
        toast.error('Error al publicar la invitación.');
      }
    }
  });
};

const pauseInvitation = () => {
  openConfirmModal({
    title: 'Pausar Invitación',
    message: '¿Estás seguro de que deseas pausar tu invitación? Esto desactivará el acceso público temporalmente y la devolverá al estado borrador.',
    emoji: '⏸️',
    confirmText: 'Pausar',
    cancelText: 'Cancelar',
    onConfirm: async () => {
      try {
        await builderService.updateDeployment(deploymentId, { status: 'DRAFT' });
        deploymentStatus.value = 'DRAFT';
        toast.info('Invitación pausada correctamente.');
      } catch (e) {
        toast.error('Error al pausar la invitación.');
      }
    }
  });
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

// --- Lógica del Gestor de Secciones y Bloques Premium ---
const dragIndex = ref(null);
const newImageUrl = ref('');
const isUploading = ref(false);

const onDragStart = (event, index) => {
  if (localConfig.value.blocks[index].locked) {
    event.preventDefault();
    return;
  }
  dragIndex.value = index;
  event.dataTransfer.effectAllowed = 'move';
};

const onDrop = (event, index) => {
  if (localConfig.value.blocks[index].locked) {
    return;
  }
  const fromIndex = dragIndex.value;
  if (fromIndex !== null && fromIndex !== index) {
    const temp = localConfig.value.blocks[fromIndex];
    localConfig.value.blocks.splice(fromIndex, 1);
    localConfig.value.blocks.splice(index, 0, temp);
  }
  dragIndex.value = null;
};

const addProtocolBlock = () => {
  const timestamp = Date.now();
  const id = `protocol_words_${timestamp}`;
  
  // 1. Agregar a localConfig.blocks
  localConfig.value.blocks.push({
    id,
    type: 'ProtocolWordsBlock',
    name: '📜 P. Protocolares',
    visible: true,
    locked: false
  });
  
  // 2. Inicializar configuración por defecto
  localConfig.value[id] = {
    title: 'Palabras Protocolares',
    description: 'Mensaje de agradecimiento o bendición.',
    columns: [
      { role: 'Padres de la Novia', names: 'Nombre del Padre & Madre' },
      { role: 'Padres del Novio', names: 'Nombre del Padre & Madre' }
    ]
  };
  
  // 3. Abrir la pestaña de edición de esta nueva sección de inmediato
  activeTab.value = id;
  toast.success('Nueva sección protocolar agregada');
};

const deleteProtocolBlock = (id) => {
  openConfirmModal({
    title: 'Eliminar Sección',
    message: '¿Estás seguro de que deseas eliminar esta sección protocolar? Esta acción no se puede deshacer.',
    emoji: '🗑️',
    confirmText: 'Sí, eliminar',
    cancelText: 'Cancelar',
    onConfirm: () => {
      // 1. Remover de blocks list
      localConfig.value.blocks = localConfig.value.blocks.filter(b => b.id !== id);
      // 2. Eliminar su clave de configuración
      delete localConfig.value[id];
      
      // 3. Si la pestaña activa era esta, regresar a 'sections'
      if (activeTab.value === id) {
        activeTab.value = 'sections';
      }
      toast.success('Sección protocolar eliminada');
    }
  });
};

const updateBlockName = (id, title) => {
  const block = localConfig.value.blocks.find(b => b.id === id);
  if (block) {
    block.name = `📜 P. Protocolares: ${title || 'Sin título'}`;
  }
};

const addProtocolRow = (id) => {
  if (!localConfig.value[id].columns) {
    localConfig.value[id].columns = [];
  }
  localConfig.value[id].columns.push({
    role: 'Nuevo Rol',
    names: 'Nombre'
  });
  saveStatus.value = 'unsaved';
};

const removeProtocolRow = (id, idx) => {
  localConfig.value[id].columns.splice(idx, 1);
  saveStatus.value = 'unsaved';
};

const addThoughtsBlock = () => {
  const timestamp = Date.now();
  const id = `invitation_text_${timestamp}`;
  
  // 1. Agregar a localConfig.blocks
  localConfig.value.blocks.push({
    id,
    type: 'InvitationTextBlock',
    name: '✍️ Pensamiento',
    visible: true,
    locked: false
  });
  
  // 2. Inicializar configuración por defecto
  localConfig.value[id] = {
    title: 'Pensamiento',
    text: 'Familia tal y tal se enorgullece en invitarlo a usted y su apreciable familia...',
    align: 'center',
    fontStyle: 'serif'
  };
  
  // 3. Abrir la pestaña de edición de esta nueva sección de inmediato
  activeTab.value = id;
  toast.success('Nueva sección de pensamientos agregada');
};

const deleteThoughtsBlock = (id) => {
  openConfirmModal({
    title: 'Eliminar Sección',
    message: '¿Estás seguro de que deseas eliminar esta sección de pensamiento? Esta acción no se puede deshacer.',
    emoji: '🗑️',
    confirmText: 'Sí, eliminar',
    cancelText: 'Cancelar',
    onConfirm: () => {
      // 1. Remover de blocks list
      localConfig.value.blocks = localConfig.value.blocks.filter(b => b.id !== id);
      // 2. Eliminar su clave de configuración
      delete localConfig.value[id];
      
      // 3. Si la pestaña activa era esta, regresar a 'sections'
      if (activeTab.value === id) {
        activeTab.value = 'sections';
      }
      toast.success('Sección de pensamiento eliminada');
    }
  });
};

const updateThoughtsBlockName = (id, title) => {
  const block = localConfig.value.blocks.find(b => b.id === id);
  if (block) {
    block.name = `✍️ Pensamiento: ${title || 'Sin título'}`;
  }
};

const getWordCount = (str) => {
  if (!str) return 0;
  const cleanStr = str.trim();
  if (cleanStr === '') return 0;
  return cleanStr.split(/\s+/).length;
};

const validateThoughtsText = (id) => {
  saveStatus.value = 'unsaved';
  const text = localConfig.value[id].text || '';
  const words = text.trim().split(/\s+/);
  if (words.length > 120) {
    toast.warning('Has alcanzado el límite máximo de palabras para esta sección.');
    localConfig.value[id].text = words.slice(0, 120).join(' ');
  }
};

const selectedPaletteCategory = ref('basic');
const setPaletteCategory = (cat) => {
  selectedPaletteCategory.value = cat;
};

const filteredPalettes = computed(() => {
  return COLOR_PALETTES.filter(p => p.category === selectedPaletteCategory.value);
});

const selectColorPalette = (palette) => {
  if (palette.premium && !allowedFeatures.value.custom_theme) {
    showUpgradeModal.value = true;
    toast.info('Esta paleta de colores premium requiere el pase de actualización.');
    return;
  }
  localConfig.value.theme.palette_id = palette.id;
  saveStatus.value = 'unsaved';
};

const selectContentTexture = (texture) => {
  if (texture.premium && !allowedFeatures.value.custom_theme) {
    showUpgradeModal.value = true;
    toast.info('Esta textura premium de fondo requiere el pase de actualización.');
    return;
  }
  localConfig.value.theme.content_bg_texture = texture.id;
  saveStatus.value = 'unsaved';
};

const toggleBlockVisibility = (block) => {
  if (block.locked) return;

  const configKey = block.configKey;
  const isNowVisible = localConfig.value[configKey];

  let allowed = true;
  if (block.id === 'timer' && !allowedFeatures.value.countdown_timer) allowed = false;
  if (block.id === 'timeline' && !allowedFeatures.value.timeline) allowed = false;
  if (block.id === 'gift_table' && !allowedFeatures.value.gift_table) allowed = false;
  if (block.id === 'photo_carousel' && !allowedFeatures.value.photo_carousel) allowed = false;

  if (!allowed && isNowVisible) {
    localConfig.value[configKey] = false;
    showUpgradeModal.value = true;
    return;
  }

  const b = localConfig.value.blocks.find(x => x.id === block.id);
  if (b) {
    b.visible = isNowVisible;
  }
};

const syncGiftTableVisibility = () => {
  if (!allowedFeatures.value.gift_table && localConfig.value.has_gift_table) {
    localConfig.value.has_gift_table = false;
    showUpgradeModal.value = true;
    return;
  }
  const b = localConfig.value.blocks?.find(x => x.id === 'gift_table');
  if (b) b.visible = localConfig.value.has_gift_table;
};

const syncPhotoCarouselVisibility = () => {
  if (!allowedFeatures.value.photo_carousel && localConfig.value.has_photo_carousel) {
    localConfig.value.has_photo_carousel = false;
    showUpgradeModal.value = true;
    return;
  }
  const b = localConfig.value.blocks?.find(x => x.id === 'photo_carousel');
  if (b) b.visible = localConfig.value.has_photo_carousel;
};

const syncDressCodeVisibility = () => {
  const b = localConfig.value.blocks?.find(x => x.id === 'dress_code');
  if (b) b.visible = localConfig.value.has_dress_code;
};

// Cuentas Bancarias
const addBankAccount = () => {
  if (!localConfig.value.gift_table.bank_accounts) {
    localConfig.value.gift_table.bank_accounts = [];
  }
  localConfig.value.gift_table.bank_accounts.push({
    bank: '',
    holder: '',
    clabe: ''
  });
};

const removeBankAccount = (index) => {
  localConfig.value.gift_table.bank_accounts.splice(index, 1);
};

// Mesas de Regalos en Tiendas
const addGiftRegistry = () => {
  if (!localConfig.value.gift_table.gift_registries) {
    localConfig.value.gift_table.gift_registries = [];
  }
  localConfig.value.gift_table.gift_registries.push({
    store: '',
    event_id: '',
    url: ''
  });
};

const removeGiftRegistry = (index) => {
  localConfig.value.gift_table.gift_registries.splice(index, 1);
};

// Galería de Imágenes
const addImageUrl = () => {
  if (newImageUrl.value && newImageUrl.value.trim() !== '') {
    if (!localConfig.value.photo_carousel.images) {
      localConfig.value.photo_carousel.images = [];
    }
    localConfig.value.photo_carousel.images.push(newImageUrl.value.trim());
    newImageUrl.value = '';
    toast.success('¡Enlace de imagen agregado!');
  }
};

const uploadImages = async (event) => {
  const files = event.target.files;
  if (!files || files.length === 0) return;

  isUploading.value = true;
  
  try {
    for (let i = 0; i < files.length; i++) {
      const formData = new FormData();
      formData.append('file', files[i]);
      
      const response = await builderService.uploadMedia(deploymentId, formData);
      if (response.data && response.data.url) {
        if (!localConfig.value.photo_carousel.images) {
          localConfig.value.photo_carousel.images = [];
        }
        localConfig.value.photo_carousel.images.push(response.data.url);
      }
    }
    toast.success('¡Imágenes subidas exitosamente!');
    // Limpiar input
    event.target.value = '';
    saveStatus.value = 'unsaved';
  } catch (error) {
    console.error(error);
    toast.error('Ocurrió un error al subir algunas imágenes.');
  } finally {
    isUploading.value = false;
  }
};

const removeImageUrl = (index) => {
  localConfig.value.photo_carousel.images.splice(index, 1);
  toast.info('Imagen eliminada de la lista.');
};

// Watchers de sincronización bidireccional reactiva para previsualización instantánea
watch(() => localConfig.value.has_timer, (val) => {
  const b = localConfig.value.blocks?.find(x => x.id === 'timer');
  if (b) b.visible = val;
});

watch(() => localConfig.value.has_timeline, (val) => {
  const b = localConfig.value.blocks?.find(x => x.id === 'timeline');
  if (b) b.visible = val;
});

watch(() => localConfig.value.has_gift_table, (val) => {
  const b = localConfig.value.blocks?.find(x => x.id === 'gift_table');
  if (b) b.visible = val;
});

watch(() => localConfig.value.has_photo_carousel, (val) => {
  const b = localConfig.value.blocks?.find(x => x.id === 'photo_carousel');
  if (b) b.visible = val;
});

watch(() => localConfig.value.has_location, (val) => {
  const b = localConfig.value.blocks?.find(x => x.id === 'location');
  if (b) b.visible = val;
});

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
    transformOrigin: 'top center',
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
  overflow: hidden;
  min-height: 0;
}

/* Panel de Controles */
.control-panel {
  width: 380px;
  background: #0b0f19;
  color: white;
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.5);
  z-index: 10;
  min-height: 0;
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

/* Horizontal Scrollable Tabs */
.horizontal-tabs-container {
  scrollbar-width: none; /* Firefox */
}
.horizontal-tabs-container::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}
.h-tab-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  background: #020617;
  border: 1px solid rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  padding: 0.5rem 0.75rem;
  border-radius: 12px;
  min-width: 72px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.h-tab-btn:hover {
  border-color: rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
}
.h-tab-btn.active {
  background: rgba(56, 189, 248, 0.15);
  border: 1px solid rgba(56, 189, 248, 0.3);
  color: #38bdf8;
  box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1);
}

.config-form {
  flex: 1;
  padding: 0 1.5rem 2rem 1.5rem;
  overflow-y: auto;
  min-height: 0;
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
  width: 44px;
  height: 24px;
  border-radius: 12px;
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
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: white;
  top: 2px;
  left: 2px;
  transition: transform 0.2s ease;
}
.switch-input:checked::before {
  transform: translateX(20px);
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
  -webkit-appearance: none;
  width: 100%;
  cursor: pointer;
  height: 8px;
  background: #334155;
  border-radius: 4px;
  outline: none;
}
.hue-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #38bdf8;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}
.hue-range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #38bdf8;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
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
    height: 100%; /* Respetar el layout padre con 100dvh */
    overflow: hidden;
  }
  .control-panel {
    width: 100%;
    height: 100%;
  }
  .config-form {
    padding: 0 1rem 7rem 1rem; /* Espacio para la bottom bar y reducción de padding horizontal */
  }
  .preview-panel {
    padding: 0;
    height: 100%;
  }
  .simulator-scale-wrapper {
    width: 100%;
    height: 100%;
    transform: none !important; /* Disable any scale transform on mobile */
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
  .preview-canvas {
    padding-bottom: 7rem; /* Espacio para la bottom bar */
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

.preview-canvas :deep(h1) {
  font-size: 2.5rem; /* Sin !important para permitir la sobrescritura del slider de tamaño del título */
  line-height: 1.1 !important;
  word-break: break-word !important;
  overflow-wrap: break-word !important;
}

.preview-canvas :deep(.min-h-screen) {
  min-height: 800px !important;
}
</style>
