<template>
  <div v-if="styleName !== 'none'" class="section-divider py-8 flex justify-center items-center w-full overflow-hidden select-none pointer-events-none">
    <!-- Style: simple-line -->
    <svg v-if="styleName === 'simple-line'" class="w-full max-w-[300px] h-6" viewBox="0 0 300 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="0" y1="12" x2="135" y2="12" stroke="currentColor" stroke-width="1" class="text-primary opacity-40" />
      <polygon points="150,6 156,12 150,18 144,12" fill="currentColor" class="text-primary" />
      <line x1="165" y1="12" x2="300" y2="12" stroke="currentColor" stroke-width="1" class="text-primary opacity-40" />
    </svg>

    <!-- Style: geometric-diamonds -->
    <svg v-else-if="styleName === 'geometric-diamonds'" class="w-full max-w-[200px] h-6" viewBox="0 0 200 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="100,4 108,12 100,20 92,12" fill="currentColor" class="text-primary" />
      <polygon points="70,7 75,12 70,17 65,12" fill="currentColor" class="text-primary opacity-60" />
      <polygon points="130,7 135,12 130,17 125,12" fill="currentColor" class="text-primary opacity-60" />
      <circle cx="40" cy="12" r="3" fill="currentColor" class="text-primary opacity-30" />
      <circle cx="160" cy="12" r="3" fill="currentColor" class="text-primary opacity-30" />
    </svg>

    <!-- Style: floral-twigs -->
    <svg v-else-if="styleName === 'floral-twigs'" class="w-full max-w-[250px] h-8" viewBox="0 0 250 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Central stem -->
      <path d="M 30 16 Q 125 24, 220 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" class="text-primary opacity-50" />
      <!-- Left twigs -->
      <path d="M 80 17 Q 65 10, 50 12" stroke="currentColor" stroke-width="1" class="text-primary opacity-60" />
      <path d="M 100 18 Q 90 26, 80 28" stroke="currentColor" stroke-width="1" class="text-primary opacity-60" />
      <!-- Right twigs -->
      <path d="M 170 17 Q 185 10, 200 12" stroke="currentColor" stroke-width="1" class="text-primary opacity-60" />
      <path d="M 150 18 Q 160 26, 170 28" stroke="currentColor" stroke-width="1" class="text-primary opacity-60" />
      <!-- Central flower/leaf -->
      <path d="M 125 6 C 120 12, 120 20, 125 26 C 130 20, 130 12, 125 6 Z" fill="currentColor" class="text-primary" />
    </svg>

    <!-- Style: soft-wave -->
    <svg v-else-if="styleName === 'soft-wave'" class="w-full max-w-[320px] h-6" viewBox="0 0 320 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M 10 12 Q 50 2, 90 12 T 170 12 T 250 12 T 310 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" class="text-primary opacity-50" />
      <circle cx="160" cy="12" r="4" fill="currentColor" class="text-primary" />
    </svg>
  </div>
</template>

<script setup>
defineProps({
  styleName: {
    type: String,
    default: 'none'
  }
});
</script>

<style scoped>
.section-divider {
  transition: all 0.3s ease;
}
.text-primary {
  color: hsl(var(--p));
}
</style>
