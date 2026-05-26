<template>
  <div class="fixed inset-0 pointer-events-none z-50">
    <!-- Top Watermark Banner -->
    <div class="pointer-events-auto w-full bg-gradient-to-r from-amber-600 via-amber-500 to-amber-600 text-white text-center py-2.5 font-black text-[10px] tracking-[0.3em] uppercase shadow-2xl border-b border-amber-400/30 backdrop-blur-md">
      ✨ MODO VISTA PREVIA - INVITAZYON DIGITAL ✨
    </div>

    <!-- Floating Purchase Action -->
    <div class="pointer-events-auto fixed bottom-8 right-8 animate-bounce">
      <button 
        @click="onClick" 
        class="btn btn-primary rounded-2xl shadow-2xl shadow-primary/45 border-2 border-white/25 px-6 h-14 font-black flex items-center gap-3 hover:scale-105 active:scale-95 transition-transform duration-300"
      >
        <span>🛒</span>
        <span>Comprar</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['purchase']);

const onClick = () => {
  emit('purchase');
};
</script>
