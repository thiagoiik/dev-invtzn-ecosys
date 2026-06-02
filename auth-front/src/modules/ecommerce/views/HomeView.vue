<template>
  <div class="min-h-screen bg-slate-50 flex flex-col font-sans overflow-x-hidden">
    
    <!-- Navbar Minimalista para el Home -->
    <header class="fixed top-0 w-full z-50 transition-all duration-300" :class="{ 'bg-white/80 backdrop-blur-md shadow-sm': scrolled, 'bg-transparent': !scrolled }">
      <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2">
          <span class="text-2xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600">
            Invitazyon
          </span>
        </router-link>
        <nav class="hidden md:flex items-center gap-8 font-medium text-slate-600">
          <router-link to="/catalog" class="hover:text-slate-900 transition-colors">Catalogo</router-link>
          <a href="#servicios" class="hover:text-slate-900 transition-colors">Servicios a Medida</a>
          <router-link to="/login" class="hover:text-slate-900 transition-colors">Iniciar Sesión</router-link>
        </nav>
        <button @click="handleStartDesigning" class="hidden md:flex btn btn-primary rounded-full px-6 py-2.5 font-bold shadow-lg shadow-primary/30 hover:shadow-primary/50 transition-all hover:-translate-y-0.5" :disabled="loadingAction">
          <span v-if="loadingAction" class="loading loading-spinner loading-xs mr-1"></span>
          Crear Invitación Gratis
        </button>
        <!-- Mobile Menu Toggle -->
        <button class="md:hidden text-slate-900 p-2" @click="isMobileMenuOpen = !isMobileMenuOpen">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
        </button>
      </div>
    </header>

    <!-- Mobile Menu Dropdown -->
    <div 
      v-if="isMobileMenuOpen" 
      class="md:hidden fixed top-20 left-0 w-full bg-white/95 backdrop-blur-md border-b border-slate-100 shadow-lg z-40 py-6 px-8 flex flex-col gap-4 animate-fade-in-up"
    >
      <router-link to="/catalog" class="text-lg font-bold text-slate-800" @click="isMobileMenuOpen = false">Catálogo</router-link>
      <a href="#servicios" class="text-lg font-bold text-slate-800" @click="isMobileMenuOpen = false">Servicios a Medida</a>
      <router-link to="/login" class="text-lg font-bold text-slate-800" @click="isMobileMenuOpen = false">Iniciar Sesión</router-link>
      <button @click="handleStartDesigning(); isMobileMenuOpen = false" class="btn btn-primary rounded-full w-full h-12 font-black mt-2" :disabled="loadingAction">
        <span v-if="loadingAction" class="loading loading-spinner loading-xs mr-1"></span>
        Crear Invitación Gratis
      </button>
    </div>

    <!-- Hero Section -->
    <main class="flex-1 flex flex-col">
      <section class="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden flex-1 flex items-center">
        <!-- Background Gradients -->
        <div class="absolute inset-0 bg-slate-50"></div>
        <div class="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-br from-primary/20 to-purple-300/20 rounded-full blur-3xl opacity-50 transform translate-x-1/3 -translate-y-1/4"></div>
        <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-amber-200/20 to-orange-300/20 rounded-full blur-3xl opacity-50 transform -translate-x-1/3 translate-y-1/4"></div>

        <div class="max-w-7xl mx-auto px-6 relative z-10 grid lg:grid-cols-2 gap-12 items-center">
          
          <!-- Text Content -->
          <div class="max-w-2xl">
            <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/60 backdrop-blur-sm border border-slate-200 shadow-sm mb-6 animate-fade-in-up">
              <span class="flex h-2 w-2 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span class="text-xs font-bold text-slate-600 uppercase tracking-widest">Invitaciones Especiales</span>
            </div>
                        <h1 class="text-5xl lg:text-7xl font-light font-serif text-slate-900 tracking-tight leading-[1.1] mb-6 animate-fade-in-up" style="animation-delay: 100ms;">
              El primer gran momento <br/>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-600 font-serif font-black">de tu evento.</span>
            </h1>
            
            <p class="text-lg lg:text-xl text-slate-600 mb-10 leading-relaxed animate-fade-in-up" style="animation-delay: 200ms;">
              Diseña la puerta de entrada a tu celebración. Invitaciones digitales interactivas de alta gama con confirmación inteligente, listas para personalizar en minutos o creadas desde cero en nuestro estudio.
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 animate-fade-in-up" style="animation-delay: 300ms;">
              <button @click="handleStartDesigning" class="btn btn-primary text-lg rounded-full px-8 py-4 font-bold shadow-xl shadow-primary/30 hover:shadow-primary/50 transition-all hover:-translate-y-1 text-center animate-pulse-subtle" :disabled="loadingAction">
                <span v-if="loadingAction" class="loading loading-spinner mr-2"></span>
                Diseñar desde Cero
              </button>
              <router-link to="/catalog" class="btn bg-white text-slate-900 border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-lg rounded-full px-8 py-4 font-bold shadow-sm transition-all hover:-translate-y-1 text-center">
                Explorar Catálogo
              </router-link>
            </div>
            
            <div 
              @click="scrollToTestimonios"
              class="mt-10 flex items-center gap-4 text-sm text-slate-500 font-medium animate-fade-in-up cursor-pointer hover:text-slate-800 transition-colors" 
              style="animation-delay: 400ms;"
            >
              <div class="flex -space-x-2">
                <div class="w-8 h-8 rounded-full bg-primary/20 border-2 border-white flex items-center justify-center text-[10px] font-black text-primary">S</div>
                <div class="w-8 h-8 rounded-full bg-purple-100 border-2 border-white flex items-center justify-center text-[10px] font-black text-purple-700">A</div>
                <div class="w-8 h-8 rounded-full bg-pink-100 border-2 border-white flex items-center justify-center text-[10px] font-black text-pink-600">D</div>
              </div>
              <p class="hover:underline">Únete a cientos de novios y organizadores.</p>
            </div>
          </div>

          <!-- Visual / Mockup -->
          <div class="relative lg:h-[600px] flex items-center justify-center animate-fade-in-up" style="animation-delay: 200ms;">
            <!-- Smartphone styled mockup for dynamic CoverBlock preview -->
            <div class="relative w-full max-w-[300px] aspect-[9/16] bg-slate-900 rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.15)] hover:shadow-[0_25px_60px_rgba(0,0,0,0.3)] hover:scale-[1.02] transition-all duration-500 border-4 border-slate-950 overflow-hidden flex items-center justify-center">
              <!-- Dynamic CSS Preview -->
              <div 
                v-if="featuredProduct && featuredProduct.has_template && featuredProduct.template_config" 
                class="absolute inset-0 overflow-hidden pointer-events-none"
              >
                <div 
                  class="absolute top-0 left-0 w-[200%] h-[200%] origin-top-left scale-50"
                >
                  <CoverBlock 
                    :config="getCoverConfig(featuredProduct.template_config)"
                    :style="{ minHeight: '100%', height: '100%', ...getThemeVariables(featuredProduct.template_config) }"
                  />
                </div>
              </div>
              
              <!-- Fallback Mockup UI -->
              <div v-else class="relative z-10 w-full h-full flex flex-col p-6 bg-white rounded-[2.2rem]">
                <!-- Imagen de Invitación -->
                <div class="h-1/2 w-full rounded-2xl mb-4 overflow-hidden bg-slate-100 flex items-center justify-center relative">
                   <div class="absolute inset-0 bg-gradient-to-tr from-amber-100 to-rose-100 opacity-50"></div>
                   <span class="text-4xl relative z-10">💍</span>
                </div>
                <!-- Textos -->
                <h3 class="font-serif text-2xl text-slate-800 text-center mb-1 font-bold">Carlos & María</h3>
                <p class="text-xs text-slate-500 text-center mb-6 uppercase tracking-widest">24 Dic 2026</p>
                <!-- Botón -->
                <div class="h-12 w-full bg-primary/10 rounded-xl mt-auto border border-primary/20 flex items-center justify-center">
                   <span class="text-primary font-bold text-sm">RSVP Abierto</span>
                </div>
              </div>
            </div>

            <!-- Floating Elements -->
            <div class="absolute -right-6 top-1/4 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 animate-float">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <div>
                  <p class="text-sm font-bold text-slate-900">Ana Confirmó</p>
                  <p class="text-xs text-slate-500">Mesa 4 • Confirmación Recibida</p>
                </div>
              </div>
            </div>
            
            <div class="absolute -left-8 bottom-1/4 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 animate-float" style="animation-delay: -2s;">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.286L13 21l-2.286-5.714L5 12l5.714-2.286L13 3z"></path></svg>
                </div>
                <div>
                  <p class="text-sm font-bold text-slate-900">Diseño Premium</p>
                  <p class="text-xs text-slate-500">Música + Animación 3D</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Sección: Dos Caminos -->
      <section id="caminos" class="py-24 bg-white border-t border-slate-100 relative">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <span class="text-xs font-bold tracking-[0.2em] text-primary uppercase">Crea a tu manera</span>
            <h2 class="text-4xl font-serif font-black text-slate-900 tracking-tight">Dos caminos hacia la invitación perfecta</h2>
            <div class="w-16 h-1.5 bg-gradient-to-r from-primary to-purple-600 mx-auto rounded-full"></div>
          </div>
          
          <div class="grid md:grid-cols-2 gap-8 lg:gap-12">
            <!-- Camino A: Catálogo -->
            <div class="group p-8 lg:p-12 rounded-[2.5rem] bg-slate-50 border border-slate-100 hover:border-slate-200 hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
              <div class="space-y-6">
                <div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
                  <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                </div>
                <h3 class="text-2xl font-serif font-bold text-slate-800">Colecciones de Autor</h3>
                <p class="text-slate-650 leading-relaxed">
                  Elige entre decenas de plantillas exclusivas creadas por diseñadores profesionales. Simplemente ingresa tus datos y tu invitación estará lista para compartir en minutos. Ideal si buscas elegancia y rapidez sin complicaciones de edición.
                </p>
              </div>
              <div class="pt-8">
                <router-link to="/catalog" class="btn btn-outline border-slate-300 text-slate-700 hover:bg-slate-100/50 hover:text-slate-900 rounded-full px-6 py-2.5 font-bold transition-all">
                  Explorar Catálogo
                </router-link>
              </div>
            </div>

            <!-- Camino B: Studio -->
            <div class="group p-8 lg:p-12 rounded-[2.5rem] bg-slate-950 border border-slate-850 hover:shadow-xl transition-all duration-300 flex flex-col justify-between text-white">
              <div class="space-y-6">
                <div class="w-14 h-14 bg-purple-500/10 rounded-2xl flex items-center justify-center text-purple-400 group-hover:scale-110 transition-transform">
                  <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                </div>
                <h3 class="text-2xl font-serif font-bold">Estudio Creativo Profesional</h3>
                <p class="text-slate-400 leading-relaxed">
                  Diseña con total libertad. Nuestro editor en blanco te permite personalizar cada color, tipografía, cargar tu propia música de fondo y organizar los bloques de contenido a tu gusto para que la invitación sea tan única como tu evento.
                </p>
              </div>
              <div class="pt-8">
                <button @click="handleStartDesigning" class="btn btn-primary rounded-full px-8 py-2.5 font-bold shadow-lg shadow-primary/30 hover:shadow-primary/50 transition-all hover:-translate-y-0.5" :disabled="loadingAction">
                  <span v-if="loadingAction" class="loading loading-spinner loading-xs mr-1"></span>
                  Comenzar a Diseñar
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección: RSVP -->
      <section id="rsvp" class="py-24 bg-slate-50 border-t border-slate-100 relative">
        <div class="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-8">
            <div class="space-y-4">
              <span class="text-xs font-bold tracking-[0.2em] text-primary uppercase">Asistencia sin estrés</span>
              <h2 class="text-4xl font-serif font-black text-slate-900 tracking-tight leading-tight">Confirmaciones RSVP organizadas, fluidas y elegantes</h2>
              <p class="text-lg text-slate-600 leading-relaxed">
                Olvídate de las listas a mano y del desorden de mensajes. Ofrece a tus invitados una experiencia interactiva al confirmar su asistencia y mantén el control de tu evento en tiempo real.
              </p>
            </div>

            <!-- Tiers comparativos elegantes -->
            <div class="space-y-4">
              <div class="p-6 rounded-2xl bg-white border border-slate-150 flex gap-4">
                <div class="w-10 h-10 rounded-xl bg-slate-50 flex-shrink-0 flex items-center justify-center text-slate-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.94.725l.548 2.2a1 1 0 01-.321.988l-1.305.98a10.582 10.582 0 004.872 4.872l.98-1.305a1 1 0 01.988-.321l2.2.548a1 1 0 01.725.94V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-800">Confirmación Básica vía WhatsApp</h4>
                  <p class="text-sm text-slate-500 mt-1">Tus invitados llenan el formulario y el sistema abre un mensaje automático directo al teléfono del organizador.</p>
                </div>
              </div>

              <div class="p-6 rounded-2xl bg-white border border-slate-150 flex gap-4">
                <div class="w-10 h-10 rounded-xl bg-slate-50 flex-shrink-0 flex items-center justify-center text-slate-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z"></path></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-800">Panel de Control Privado (Standard)</h4>
                  <p class="text-sm text-slate-500 mt-1">Las confirmaciones se guardan automáticamente en tu cuenta. Visualiza quién asiste en tiempo real desde tu Dashboard privado.</p>
                </div>
              </div>

              <div class="p-6 rounded-2xl bg-white border border-slate-150 flex gap-4">
                <div class="w-10 h-10 rounded-xl bg-primary/10 flex-shrink-0 flex items-center justify-center text-primary">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
                </div>
                <div>
                  <h4 class="font-bold text-slate-800 flex items-center gap-2">
                    <span>Campos Avanzados y Filtros (Premium)</span>
                    <span class="bg-primary/10 text-primary text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">VIP</span>
                  </h4>
                  <p class="text-sm text-slate-500 mt-1">Personaliza el formulario preguntando sobre alergias alimentarias, opciones de menú, pases adicionales, requerimientos especiales y espacio para saludos.</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Lado derecho: Visual de RSVP simulado -->
          <div class="bg-white p-8 rounded-[2.5rem] border border-slate-200/60 shadow-xl space-y-6">
            <span class="text-xs font-black text-slate-400 uppercase tracking-widest">Ejemplo de Formulario RSVP</span>
            <div class="space-y-4">
              <div class="space-y-1">
                <label class="text-[10px] font-bold text-slate-500 uppercase">Nombre del Invitado</label>
                <div class="w-full h-11 bg-slate-50 rounded-xl border border-slate-200/80 px-4 flex items-center text-slate-700 text-sm font-medium">Sofía & Carlos Martínez</div>
              </div>
              <div class="space-y-1">
                <label class="text-[10px] font-bold text-slate-500 uppercase">Asistencia</label>
                <div class="grid grid-cols-2 gap-3">
                  <div class="h-12 rounded-xl border-2 border-primary bg-primary/5 text-primary flex items-center justify-center font-bold text-xs">Confirmar Asistencia</div>
                  <div class="h-12 rounded-xl border border-slate-200 text-slate-450 flex items-center justify-center font-bold text-xs">No podré asistir</div>
                </div>
              </div>
              <div class="space-y-1">
                <label class="text-[10px] font-bold text-slate-500 uppercase">Preferencias de Menú</label>
                <div class="w-full h-11 bg-slate-50 rounded-xl border border-slate-200/80 px-4 flex items-center text-slate-500 text-sm">Menú Vegano / Alergia al gluten</div>
              </div>
            </div>
            <div class="w-full h-12 bg-slate-900 text-white font-bold rounded-xl flex items-center justify-center text-xs tracking-wider uppercase">Enviar Confirmación</div>
          </div>
        </div>
      </section>

      <!-- Sección: Testimonios / Prueba Social -->
      <section id="testimonios" class="py-24 bg-white border-t border-slate-100 relative">
        <div class="max-w-7xl mx-auto px-6 space-y-16">
          <div class="text-center max-w-3xl mx-auto space-y-4">
            <span class="text-xs font-bold tracking-[0.2em] text-primary uppercase">Prueba Social</span>
            <h2 class="text-4xl font-serif font-black text-slate-900 tracking-tight leading-tight">Parejas reales, momentos inolvidables</h2>
            <div class="w-16 h-1.5 bg-gradient-to-r from-primary to-purple-600 mx-auto rounded-full"></div>
            <p class="text-lg text-slate-500 leading-relaxed max-w-2xl mx-auto">
              Descubre por qué cientos de novios y organizadores confían en nosotros para dar el primer gran paso de su evento.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div 
              v-for="rev in publicReviews" 
              :key="rev.id" 
              class="bg-slate-50/60 p-8 rounded-3xl border border-slate-150 shadow-xs space-y-5 hover:-translate-y-1 hover:shadow-md transition-all duration-300 flex flex-col justify-between"
            >
              <div class="space-y-4">
                <div class="flex text-amber-400 text-sm gap-0.5">
                  <span v-for="star in 5" :key="star">{{ star <= rev.rating ? '★' : '☆' }}</span>
                </div>
                <p class="text-slate-600 text-sm italic leading-relaxed">
                  "{{ rev.comment }}"
                </p>
              </div>
              <div class="flex items-center gap-3 pt-4 border-t border-slate-100">
                <div class="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-black uppercase shadow-inner">
                  {{ rev.reviewer_name?.charAt(0) || '?' }}
                </div>
                <div>
                  <p class="text-xs font-black text-slate-800 tracking-wider">{{ rev.reviewer_name }}</p>
                  <p class="text-[9px] text-slate-400 font-bold uppercase tracking-widest mt-0.5">Cliente Verificado</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Sección: Servicios a Medida (VIP Concierge) -->
      <section id="servicios" class="py-24 bg-white border-t border-slate-100 relative">
        <div class="max-w-5xl mx-auto px-6 text-center space-y-10">
          <div class="space-y-4">
            <span class="text-xs font-bold tracking-[0.2em] text-primary uppercase">Concierge VIP</span>
            <h2 class="text-4xl font-serif font-black text-slate-900 tracking-tight max-w-2xl mx-auto leading-tight">¿Tienes una idea o requerimiento a tu medida?</h2>
            <div class="w-16 h-1.5 bg-gradient-to-r from-primary to-purple-600 mx-auto rounded-full"></div>
          </div>
          <p class="text-lg text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Si tu evento requiere un desarrollo web especializado, un concepto interactivo único fuera del catálogo estándar o integraciones de sistemas especiales, nuestro equipo de diseño y desarrollo exclusivo está a tu disposición. Nos encargamos de programar tus ideas.
          </p>
          <div class="pt-4">
            <router-link to="/ayuda" class="btn btn-primary btn-lg rounded-full px-10 py-4 font-black shadow-xl shadow-primary/25 hover:shadow-primary/45 transition-all hover:-translate-y-1">
              Solicitar Proyecto a Medida
            </router-link>
          </div>
        </div>
      </section>

      <!-- Sección: Invitazyon Físico -->
      <section id="fisicos" class="py-24 bg-slate-950 text-white relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 z-0"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl opacity-30 pointer-events-none"></div>

        <div class="max-w-7xl mx-auto px-6 relative z-10 grid lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-8">
            <div class="space-y-4">
              <span class="text-xs font-bold tracking-[0.2em] text-purple-400 uppercase">La Experiencia Impresa</span>
              <h2 class="text-4xl font-serif font-black text-white tracking-tight leading-tight">El tacto del papel fino. La elegancia de lo tangible.</h2>
              <div class="w-16 h-1.5 bg-purple-500 rounded-full"></div>
            </div>
            <p class="text-lg text-slate-400 leading-relaxed">
              Lleva tu temática digital al mundo real. Ofrecemos una colección exclusiva de papelería física, sobres con lacre, recuerdos del evento, impresos especiales de alta calidad y detalles personalizados para crear una experiencia de marca unificada para tu celebración.
            </p>
            <div class="flex items-center gap-6 text-slate-500 text-sm font-bold uppercase tracking-widest pt-4">
              <span>Sobres Premium</span>
              <span class="w-1.5 h-1.5 bg-slate-800 rounded-full"></span>
              <span>Papelería Fina</span>
              <span class="w-1.5 h-1.5 bg-slate-800 rounded-full"></span>
              <span>Detalles Físicos</span>
            </div>
          </div>
          <div class="relative flex items-center justify-center">
            <div class="w-full max-w-md aspect-video bg-gradient-to-br from-white/10 to-white/5 rounded-3xl border border-white/15 p-8 flex flex-col justify-between shadow-2xl backdrop-blur-md">
              <div class="flex justify-between items-start">
                <span class="text-white/40 text-[10px] font-black uppercase tracking-wider">Colección Impresa</span>
                <svg class="w-6 h-6 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              </div>
              <div class="space-y-2">
                <h4 class="text-xl font-serif text-white font-light">Invitaciones Físicas & Detalles</h4>
                <p class="text-xs text-slate-450">Acabados en metal, lacre artesanal y papeles texturizados importados.</p>
              </div>
              <div class="h-[1px] bg-white/10 w-full"></div>
              <span class="text-xs text-purple-400 font-bold uppercase tracking-widest">Próximamente disponible</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Modal de Selección de Flujo al Iniciar Diseño -->
    <div v-if="showResumePrompt" class="fixed inset-0 z-[100] flex items-center justify-center px-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="showResumePrompt = false"></div>
      <div class="relative bg-white w-full max-w-md rounded-[2.5rem] p-10 shadow-2xl border border-slate-100 overflow-hidden transform scale-100 transition-transform duration-300 space-y-6 text-center">
        <div class="w-16 h-16 bg-primary/10 text-primary rounded-2xl flex items-center justify-center text-3xl mx-auto shadow-sm">
          ✨
        </div>
        <div class="space-y-2">
          <h3 class="text-2xl font-black text-slate-900">Diseños Existentes</h3>
          <p class="text-slate-500 text-sm">Hemos detectado que ya tienes invitaciones guardadas en tu cuenta. ¿Qué deseas hacer?</p>
        </div>
        <div class="flex flex-col gap-3 pt-2">
          <button @click="goToMyDashboard" class="btn btn-primary h-14 rounded-2xl font-black shadow-lg shadow-primary/20 text-sm hover:scale-[1.02] transition-transform">
            📂 Ver Mis Diseños Existentes
          </button>
          <button @click="createNewBasicDesign" class="btn btn-outline border-slate-200 hover:border-slate-300 hover:bg-slate-50 h-14 rounded-2xl font-bold text-slate-700 text-sm hover:scale-[1.02] transition-transform">
            ➕ Crear Nuevo Borrador Básico
          </button>
          <button @click="showResumePrompt = false" class="btn btn-ghost text-slate-400 font-bold uppercase tracking-wider text-[10px] mt-2">
            Cancelar
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/modules/auth/store/auth';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import CoverBlock from '@/modules/engine/components/CoverBlock.vue';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const scrolled = ref(false);
const isMobileMenuOpen = ref(false);
const showResumePrompt = ref(false);
const loadingAction = ref(false);
const featuredProduct = ref(null);

const publicReviews = ref([
  {
    id: 'mock-1',
    reviewer_name: 'Sofía & Carlos',
    comment: 'La mejor decisión para nuestra boda. Todos nuestros invitados confirmaron en cuestión de minutos y el panel de control es super intuitivo. ¡El diseño se ve espectacular en móvil!',
    rating: 5
  },
  {
    id: 'mock-2',
    reviewer_name: 'Alejandro Ruiz',
    comment: 'Como coordinador de eventos, esta plataforma me ha ahorrado días de llamadas y mensajes de confirmación. La opción de música de fondo y la cuenta regresiva le encantan a todos.',
    rating: 5
  },
  {
    id: 'mock-3',
    reviewer_name: 'Daniela & Javier',
    comment: 'Nos encantó el estilo del editor y la facilidad con la que pudimos enlazar los mapas de la iglesia y la recepción. Excelente soporte y atención de primer nivel.',
    rating: 5
  }
]);

const getCoverConfig = (templateConfig) => {
  if (!templateConfig) return {};
  if (Array.isArray(templateConfig.blocks)) {
    const coverBlock = templateConfig.blocks.find(b => b.type === 'CoverBlock');
    if (coverBlock) {
      return coverBlock.config || {};
    }
  }
  return templateConfig.cover || {};
};

const getThemeVariables = (templateConfig) => {
  if (!templateConfig) return {};
  const theme = templateConfig.theme || {};
  const h = theme.hue || 38;      // Golden hue
  const s = theme.saturation || '80%';
  const l = theme.lightness || '50%';

  return {
    '--p': `${h} ${s} ${l}`, // Primary brand color variable
  };
};

const handleScroll = () => {
  scrolled.value = window.scrollY > 20;
};

onMounted(async () => {
  window.addEventListener('scroll', handleScroll);
  try {
    const response = await catalogService.fetchProducts();
    const allProducts = response.data || [];
    featuredProduct.value = allProducts.find(p => p.has_template && p.template_slug === 'dfce56a7') || allProducts.find(p => p.has_template);
  } catch (error) {
    console.error('Error al cargar producto destacado en Home:', error);
  }

  // Cargar opiniones reales aprobadas de los clientes
  try {
    const res = await catalogService.fetchPublicReviews();
    if (res.data && res.data.length > 0) {
      publicReviews.value = res.data;
    }
  } catch (error) {
    console.error('Error al cargar reseñas públicas:', error);
  }
});

const scrollToTestimonios = () => {
  document.getElementById('testimonios')?.scrollIntoView({ behavior: 'smooth' });
};

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

const handleStartDesigning = async () => {
  if (!authStore.isAuthenticated) {
    // Si no está logueado, redirigir a registro con redirección para crear borrador básico
    router.push({ name: 'register', query: { redirect: 'create-basic' } });
    return;
  }
  
  loadingAction.value = true;
  try {
    const res = await deploymentService.fetchMyDeployments();
    if (res.data && res.data.length > 0) {
      // Tiene diseños existentes, mostrar modal interactivo
      showResumePrompt.value = true;
    } else {
      // No tiene diseños, crear uno nuevo de tipo BASIC (ID = 1)
      await createNewBasicDesign();
    }
  } catch (error) {
    toast.error('Error al verificar tus diseños.');
  } finally {
    loadingAction.value = false;
  }
};

const createNewBasicDesign = async () => {
  loadingAction.value = true;
  try {
    const res = await deploymentService.createSandbox(1);
    const newId = res.data.id;
    toast.success('¡Lienzo básico creado!');
    router.push(`/builder/${newId}`);
  } catch (error) {
    toast.error('No se pudo crear el lienzo básico.');
  } finally {
    loadingAction.value = false;
    showResumePrompt.value = false;
  }
};

const goToMyDashboard = () => {
  router.push('/dashboard');
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 5s ease-in-out infinite;
}
</style>
