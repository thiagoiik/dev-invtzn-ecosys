<template>
  <div 
    v-if="config"
    class="py-12 px-6 max-w-4xl mx-auto space-y-6 bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6"
    :class="[
      config.align === 'left' ? 'text-left' : config.align === 'right' ? 'text-right' : 'text-center'
    ]"
  >
    <div class="space-y-4">
      <!-- Elegante icono superior -->
      <span class="text-4xl block select-none">✨</span>
      
      <h2 
        v-if="config.title" 
        class="text-3xl font-black text-slate-800 tracking-tight"
      >
        {{ config.title }}
      </h2>
      
      <p 
        v-if="config.text" 
        class="text-base text-slate-600 max-w-2xl mx-auto leading-loose whitespace-pre-line"
        :class="[
          config.fontStyle === 'serif' ? 'font-serif' : 'font-sans'
        ]"
      >
        {{ config.text }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: 'Pensamiento',
      text: '',
      align: 'center',
      fontStyle: 'serif'
    })
  }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}
</style>
