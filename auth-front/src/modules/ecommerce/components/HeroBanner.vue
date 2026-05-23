<template>
  <div class="relative overflow-hidden bg-slate-950 min-h-[60vh] flex items-center">
    <!-- Background Decor -->
    <div class="absolute inset-0 z-0">
      <div class="absolute top-0 -left-4 w-72 h-72 bg-primary/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
      <div class="absolute top-0 -right-4 w-72 h-72 bg-indigo-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500/10 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-4000"></div>
    </div>

    <div class="container mx-auto px-6 relative z-10 py-20 lg:py-0">
      <div class="flex flex-col lg:flex-row items-center gap-12">
        <div class="flex-1 text-center lg:text-left space-y-8 max-w-2xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-bold text-primary tracking-widest uppercase mb-4 animate-in fade-in slide-in-from-bottom-4">
            ✨ EL FUTURO DE LOS EVENTOS
          </div>
          
          <h1 class="text-5xl lg:text-7xl font-black text-white leading-tight">
            Invitaciones que <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-indigo-400">cobran vida</span>
          </h1>
          
          <p class="text-lg text-slate-400 leading-relaxed transition-opacity duration-700 ease-in-out">
            Crea experiencias digitales únicas para tus momentos más especiales. Gestión de invitados, RSVP interactivo y diseños de alta gama en un solo lugar.
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-4 transition-transform duration-700 ease-in-out">
            <router-link to="/catalog" class="btn btn-primary btn-lg shadow-xl shadow-primary/20 hover:scale-105 transition-all">
              Explorar Catálogo
            </router-link>
            <a href="/catalog" class="btn btn-outline border-slate-700 text-slate-300 hover:bg-slate-900 btn-lg">
              Ver Demo Live
            </a>
          </div>
        </div>

        <div class="flex-1 w-full max-w-lg lg:max-w-none transition-transform duration-700 ease-in-out">
          <div class="relative">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-500 rounded-3xl blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
            <img 
              src="/hero_premium_mockup.png" 
              alt="Premium Invitations" 
              class="relative rounded-3xl shadow-2xl border border-slate-800/50 hover:scale-[1.02] transition-transform duration-500"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['explore']);
</script>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
