<template>
  <div class="min-h-screen bg-white flex flex-col items-center justify-center p-8 text-center">
    <!-- Logo/Icon Animation -->
    <div class="relative mb-12">
      <div class="w-24 h-24 bg-primary/10 rounded-[2rem] flex items-center justify-center animate-pulse">
        <span class="text-5xl">✨</span>
      </div>
      <!-- Spinning ring -->
      <div class="absolute inset-0 border-4 border-transparent border-t-primary rounded-[2rem] animate-spin"></div>
    </div>

    <!-- Text Feedback -->
    <div class="space-y-4 animate-fade-up">
      <h2 class="text-2xl font-black text-slate-900 tracking-tight">Preparando tu experiencia</h2>
      <div class="flex items-center justify-center gap-1">
        <span v-for="i in 3" :key="i" 
          class="w-1.5 h-1.5 bg-primary rounded-full animate-bounce"
          :style="{ animationDelay: `${(i-1)*0.2}s` }">
        </span>
      </div>
      <p class="text-slate-400 font-bold uppercase tracking-[0.2em] text-[10px] pt-4">Invitazyon Digital Luxury</p>
    </div>
  </div>
</template>

<script setup>
/* Componente puramente visual */
</script>

<style scoped>
.animate-fade-up {
  animation: fadeUp 0.8s ease-out forwards;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
