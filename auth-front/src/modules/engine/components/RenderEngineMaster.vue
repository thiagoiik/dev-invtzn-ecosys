<template>
  <div 
    class="min-h-screen relative overflow-x-hidden"
    :style="themeVariables"
  >
    <!-- Background Music Audio player if configured -->
    <AudioPlayer 
      v-if="customData.audioUrl || customData.has_music" 
      :config="customData.music || { audioUrl: customData.audioUrl }" 
    />

    <!-- Sandbox Premium Overlay if Draft status -->
    <DraftWatermarkOverlay 
      v-if="status === 'DRAFT'" 
      @purchase="handlePurchaseRedirect" 
    />

    <!-- Render Blocks dynamically based on configuration -->
    <div class="master-canvas" :class="{ 'pt-[44px]': status === 'DRAFT' }">
      <!-- 1. Beautiful Hero Cover -->
      <CoverBlock 
        v-if="!customData.hide_cover" 
        :config="customData.cover || {}" 
      />

      <!-- 2. Countdown Timer Block -->
      <CountdownTimer 
        v-if="customData.has_timer || customData.timer" 
        :config="customData.timer || {}" 
      />

      <!-- 3. Dynamic Timeline Block -->
      <TimelineBlock 
        v-if="customData.has_timeline || customData.timeline" 
        :config="customData.timeline || {}" 
      />

      <!-- 4. RSVP Form Block (Always at the bottom) -->
      <EngineRSVP 
        v-if="!customData.hide_rsvp" 
        :slug="slug" 
        :config="customData.rsvp || {}" 
      />
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps, defineEmits } from 'vue';
import DraftWatermarkOverlay from './DraftWatermarkOverlay.vue';
import CoverBlock from './CoverBlock.vue';
import AudioPlayer from './AudioPlayer.vue';
import CountdownTimer from './CountdownTimer.vue';
import TimelineBlock from './TimelineBlock.vue';
import EngineRSVP from './EngineRSVP.vue';

const props = defineProps({
  status: { type: String, required: true },
  customData: { type: Object, required: true },
  slug: { type: String, required: true },
  deploymentId: { type: [Number, String], default: null }
});

const emit = defineEmits(['purchase']);

const handlePurchaseRedirect = () => {
  emit('purchase');
};

// Generates dynamic brand color palletes using HSL variables
const themeVariables = computed(() => {
  const theme = props.customData.theme || {};
  // Golden style pallete fallback
  const h = theme.hue || 38;      // Golden hue
  const s = theme.saturation || '80%';
  const l = theme.lightness || '50%';

  return {
    '--p': `${h} ${s} ${l}`, // Primary brand color variable
  };
});
</script>

<style scoped>
/* Inject HSL primary variables for daisyUI elements inside master */
:deep(.btn-primary) {
  background-color: hsl(var(--p));
  border-color: hsl(var(--p));
  color: white;
}
:deep(.text-primary) {
  color: hsl(var(--p));
}
:deep(.border-primary) {
  border-color: hsl(var(--p));
}
:deep(.bg-primary) {
  background-color: hsl(var(--p));
}
</style>
