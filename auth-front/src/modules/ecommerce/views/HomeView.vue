<template>
  <div class="min-h-screen bg-slate-50 flex flex-col font-sans overflow-x-hidden">
    
    <!-- Navbar Minimalista para el Home -->
    <header class="fixed top-0 w-full z-50 transition-all duration-300" :class="{ 'bg-white/80 backdrop-blur-md shadow-sm': scrolled, 'bg-transparent': !scrolled }">
      <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-2xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600">
            Invitazyon
          </span>
        </div>
        <nav class="hidden md:flex items-center gap-8 font-medium text-slate-600">
          <router-link to="/catalog" class="hover:text-slate-900 transition-colors">Plantillas</router-link>
          <a href="#servicios" class="hover:text-slate-900 transition-colors">Servicios a Medida</a>
          <router-link to="/login" class="hover:text-slate-900 transition-colors">Iniciar Sesión</router-link>
        </nav>
        <router-link to="/auth/registration" class="hidden md:flex btn btn-primary rounded-full px-6 py-2.5 font-bold shadow-lg shadow-primary/30 hover:shadow-primary/50 transition-all hover:-translate-y-0.5">
          Crear Invitación Gratis
        </router-link>
        <!-- Mobile Menu Toggle -->
        <button class="md:hidden text-slate-900 p-2" @click="isMobileMenuOpen = !isMobileMenuOpen">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
        </button>
      </div>
    </header>

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
              <span class="text-xs font-bold text-slate-600 uppercase tracking-widest">Plataforma B2B / B2C v0.6.x</span>
            </div>
            
            <h1 class="text-5xl lg:text-7xl font-black text-slate-900 tracking-tight leading-[1.1] mb-6 animate-fade-in-up" style="animation-delay: 100ms;">
              Tu Evento Comienza <br/>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-600">Aquí.</span>
            </h1>
            
            <p class="text-lg lg:text-xl text-slate-600 mb-10 leading-relaxed animate-fade-in-up" style="animation-delay: 200ms;">
              Diseña invitaciones digitales interactivas en minutos, administra tus invitados con Códigos QR y haz de tu evento una experiencia inolvidable desde el primer clic.
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 animate-fade-in-up" style="animation-delay: 300ms;">
              <router-link to="/auth/registration" class="btn btn-primary text-lg rounded-full px-8 py-4 font-bold shadow-xl shadow-primary/30 hover:shadow-primary/50 transition-all hover:-translate-y-1 text-center">
                Comenzar a Diseñar
              </router-link>
              <router-link to="/catalog" class="btn bg-white text-slate-900 border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-lg rounded-full px-8 py-4 font-bold shadow-sm transition-all hover:-translate-y-1 text-center">
                Ver Catálogo
              </router-link>
            </div>
            
            <div class="mt-10 flex items-center gap-4 text-sm text-slate-500 font-medium animate-fade-in-up" style="animation-delay: 400ms;">
              <div class="flex -space-x-2">
                <div class="w-8 h-8 rounded-full bg-slate-200 border-2 border-white"></div>
                <div class="w-8 h-8 rounded-full bg-slate-300 border-2 border-white"></div>
                <div class="w-8 h-8 rounded-full bg-slate-400 border-2 border-white"></div>
              </div>
              <p>Únete a cientos de novios y organizadores.</p>
            </div>
          </div>

          <!-- Visual / Mockup -->
          <div class="relative lg:h-[600px] flex items-center justify-center animate-fade-in-up" style="animation-delay: 200ms;">
            <!-- Glass Mockup -->
            <div class="relative w-full max-w-md aspect-[9/16] bg-white/40 backdrop-blur-2xl rounded-[3rem] border-8 border-white shadow-2xl overflow-hidden flex items-center justify-center">
              <div class="absolute inset-0 bg-gradient-to-br from-white/60 to-white/10 z-0"></div>
              
              <!-- Simulación de UI dentro del teléfono -->
              <div class="relative z-10 w-full h-full flex flex-col p-6 bg-white rounded-[2.5rem]">
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
                <div class="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center font-bold">✓</div>
                <div>
                  <p class="text-sm font-bold text-slate-900">Ana Confirmó</p>
                  <p class="text-xs text-slate-500">Mesa 4 • QR Emitido</p>
                </div>
              </div>
            </div>
            
            <div class="absolute -left-8 bottom-1/4 bg-white p-4 rounded-2xl shadow-xl border border-slate-100 animate-float" style="animation-delay: -2s;">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold">✨</div>
                <div>
                  <p class="text-sm font-bold text-slate-900">Diseño Premium</p>
                  <p class="text-xs text-slate-500">Música + Animación 3D</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const scrolled = ref(false);
const isMobileMenuOpen = ref(false);

const handleScroll = () => {
  scrolled.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
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
