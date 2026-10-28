<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center">
    <div class="max-w-md w-full bg-white rounded-[3rem] p-12 shadow-2xl shadow-slate-200/50 border border-slate-100 space-y-8 animate-scale-in">
      
      <!-- Icon with soft glow and subtle animation -->
      <div class="w-24 h-24 bg-gradient-to-tr from-amber-50 to-amber-100/30 rounded-[2rem] flex items-center justify-center text-5xl mx-auto shadow-inner animate-pulse-slow">
        ✨
      </div>

      <div class="space-y-4">
        <h2 class="text-3xl font-black text-slate-900 leading-tight">
          ¡Invitación en edición!
        </h2>
        <p class="text-slate-500 font-medium leading-relaxed">
          El organizador está puliendo los últimos detalles de este diseño. Estará disponible públicamente muy pronto.
        </p>
      </div>

      <div class="pt-6 border-t border-slate-100">
        <div class="text-[10px] font-black text-slate-300 uppercase tracking-[0.3em]">Invitazyon Engine</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Pantalla informativa de edición / borrador para visitantes externos
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.animate-pulse-slow {
  animation: pulseSlow 3s infinite ease-in-out;
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulseSlow {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(245, 158, 11, 0)); }
  50% { transform: scale(1.05); filter: drop-shadow(0 4px 12px rgba(245, 158, 11, 0.15)); }
}
</style>
