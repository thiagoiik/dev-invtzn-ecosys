<template>
  <div 
    v-if="config"
    class="py-12 px-6 max-w-4xl mx-auto space-y-6 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6 text-center"
  >
    <div class="space-y-3">
      <div class="flex justify-center mb-2">
        <img v-if="config.icon && isUrl(config.icon)" :src="config.icon" class="w-12 h-12 object-contain" alt="icon" />
        <span v-else class="text-4xl block select-none">{{ config.icon || '📜' }}</span>
      </div>
      <h2 v-if="config.title" class="text-3xl font-black text-slate-800 tracking-tight">
        {{ config.title }}
      </h2>
      <p v-if="config.description" class="text-sm text-slate-500 max-w-lg mx-auto leading-relaxed whitespace-pre-line">
        {{ config.description }}
      </p>
    </div>

    <div 
      v-if="config.columns && config.columns.length > 0"
      class="grid protocol-grid mt-8 max-w-md mx-auto"
      :class="`cols-${config.columns.length}`"
    >
      <div 
        v-for="(col, idx) in config.columns" 
        :key="idx"
        class="bg-white/80 p-6 rounded-[2rem] border border-slate-100 shadow-sm flex flex-col justify-center space-y-3"
      >
        <span v-if="col.role" class="text-xs font-black uppercase tracking-widest text-primary">
          {{ col.role }}
        </span>
        <h3 v-if="col.names" class="text-lg font-black text-slate-800 leading-snug whitespace-pre-line">
          {{ col.names }}
        </h3>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: 'Palabras Protocolares',
      description: '',
      columns: [],
      icon: ''
    })
  }
});

const isUrl = (val) => {
  if (!val) return false;
  return val.startsWith('http') || val.startsWith('/') || val.startsWith('.') || val.includes('/');
};
</script>

<style scoped>
.protocol-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
</style>
