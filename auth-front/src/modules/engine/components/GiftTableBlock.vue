<template>
  <div class="py-12 px-6 max-w-4xl mx-auto space-y-8 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6">
    <div class="text-center space-y-2">
      <h2 class="text-3xl font-black text-slate-800 tracking-tight">{{ config.title || 'Mesa de Regalos' }}</h2>
      <p class="text-sm text-slate-500 max-w-md mx-auto leading-relaxed">{{ config.description || 'Tu presencia es nuestro mejor regalo, pero si deseas tener un detalle con nosotros...' }}</p>
    </div>

    <!-- Cuentas Bancarias / Transferencias -->
    <div v-if="config.bank_accounts && config.bank_accounts.length > 0" class="space-y-4">
      <h3 class="text-lg font-extrabold text-slate-800/90 flex items-center gap-2">
        <span>🏦</span> Transferencias Bancarias
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="(acc, idx) in config.bank_accounts" 
          :key="idx" 
          class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm relative group hover:border-primary/30 transition-all"
        >
          <span class="text-xs text-slate-400 font-bold uppercase tracking-wider block mb-1">Banco</span>
          <p class="font-extrabold text-slate-800 text-lg mb-4">{{ acc.bank }}</p>
          
          <div class="space-y-3">
            <div>
              <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">CLABE</span>
              <p class="font-mono text-sm font-bold text-slate-700 select-all">{{ acc.clabe }}</p>
            </div>
            <div>
              <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Titular</span>
              <p class="text-sm font-semibold text-slate-600">{{ acc.holder }}</p>
            </div>
          </div>

          <button 
            @click="copyClabe(acc.clabe)" 
            class="btn btn-xs btn-outline btn-primary rounded-xl absolute top-6 right-6 font-bold flex items-center gap-1"
          >
            📋 Copiar
          </button>
        </div>
      </div>
    </div>

    <!-- Tiendas / Mesas de Registro -->
    <div v-if="config.gift_registries && config.gift_registries.length > 0" class="space-y-4">
      <h3 class="text-lg font-extrabold text-slate-800/90 flex items-center gap-2">
        <span>🎁</span> Mesas de Regalos Registradas
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <a 
          v-for="(reg, idx) in config.gift_registries" 
          :key="idx" 
          :href="reg.url" 
          target="_blank" 
          class="flex items-center justify-between p-5 bg-white rounded-2xl border border-slate-100 hover:border-primary hover:shadow-md transition-all group"
        >
          <div class="space-y-1">
            <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">Tienda</span>
            <p class="font-extrabold text-slate-800 text-sm group-hover:text-primary transition-colors">{{ reg.store }}</p>
            <span v-if="reg.event_id" class="text-xs text-slate-400 font-medium">Evento: {{ reg.event_id }}</span>
          </div>
          <span class="text-primary text-xl group-hover:translate-x-1 transition-transform">➔</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToast } from 'vue-toastification';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      title: 'Mesa de Regalos',
      description: 'Tu presencia es nuestro mejor regalo, pero si deseas tener un detalle con nosotros...',
      bank_accounts: [],
      gift_registries: []
    })
  }
});

const toast = useToast();

const copyClabe = (clabe) => {
  if (clabe) {
    navigator.clipboard.writeText(clabe);
    toast.success('¡CLABE copiada al portapapeles!');
  }
};
</script>
