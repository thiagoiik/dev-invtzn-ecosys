<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center">
    <div class="max-w-md w-full bg-white rounded-[3rem] p-12 shadow-2xl shadow-slate-200/50 border border-slate-100 space-y-8 animate-scale-in">
      
      <!-- Icon with soft glow -->
      <div class="w-24 h-24 bg-slate-50 rounded-[2rem] flex items-center justify-center text-5xl mx-auto shadow-inner">
        ⌛
      </div>

      <div class="space-y-4">
        <h2 class="text-3xl font-black text-slate-900 leading-tight">
          {{ title }}
        </h2>
        <p class="text-slate-500 font-medium leading-relaxed">
          {{ message }}
        </p>
      </div>

      <div class="pt-6 border-t border-slate-50">
        <div class="text-[10px] font-black text-slate-300 uppercase tracking-[0.3em] mb-4">Invitazyon Engine</div>
        <button v-if="showContact" @click="handleContact" class="btn btn-ghost btn-sm text-primary font-bold">
          Contactar Organizador
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  status: { type: String, default: 'EXPIRED' },
  showContact: { type: Boolean, default: false }
});

const title = props.status === 'EXPIRED' ? '¡El evento ha concluido!' : 'Invitación en pausa';
const message = props.status === 'EXPIRED' 
  ? 'Este momento ya es parte de los mejores recuerdos. La invitación ya no se encuentra activa.' 
  : 'El organizador ha pausado temporalmente la visualización de este diseño.';

const handleContact = () => {
  // Lógica futura para contactar
  window.alert('Funcionalidad de contacto próximamente.');
};
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
</style>
