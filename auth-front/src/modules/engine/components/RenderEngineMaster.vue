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
      v-if="status === 'DRAFT' && !isStudioMode" 
      @purchase="handlePurchaseRedirect" 
    />

    <!-- Render Blocks dynamically based on configuration -->
    <div class="master-canvas" :class="{ 'pt-[44px]': status === 'DRAFT' }">
      <component
        v-for="block in orderedBlocks"
        :key="block.id"
        :is="block.component"
        :config="block.config"
        v-bind="block.component === RsvpFormBlock ? { slug: slug, tierLevel: tierLevel } : {}"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import DraftWatermarkOverlay from './DraftWatermarkOverlay.vue';
import CoverBlock from './CoverBlock.vue';
import AudioPlayer from './AudioPlayer.vue';
import CountdownTimer from './CountdownTimer.vue';
import TimelineBlock from './TimelineBlock.vue';
import RsvpFormBlock from './RsvpFormBlock.vue';
import { useTelemetry } from '../composables/useTelemetry';

const props = defineProps({
  status: { type: String, required: true },
  customData: { type: Object, required: true },
  slug: { type: String, required: true },
  deploymentId: { type: [Number, String], default: null },
  isStudioMode: { type: Boolean, default: false },
  tierLevel: { type: String, default: 'BASIC' }
});

const emit = defineEmits(['purchase']);

const telemetry = useTelemetry();

onMounted(() => {
  // Silent tracking of page visits upon master load
  telemetry.trackVisit(props.slug);
});

const handlePurchaseRedirect = () => {
  emit('purchase');
};

// Mapeo de componentes disponibles para renderizado dinámico
const componentMap = {
  CoverBlock: CoverBlock,
  CountdownTimer: CountdownTimer,
  TimelineBlock: TimelineBlock,
  RsvpFormBlock: RsvpFormBlock
};

// Generar el orden dinámico de bloques con fallback retrocompatible
const orderedBlocks = computed(() => {
  // Caso 1: Estructura moderna con ordenamiento dinámico
  if (Array.isArray(props.customData.blocks)) {
    return props.customData.blocks
      .map(b => ({
        id: b.id,
        component: componentMap[b.type],
        config: b.config || {},
        visible: b.visible !== false
      }))
      .filter(b => b.component && b.visible);
  }

  // Caso 2: Fallback retrocompatible para registros antiguos
  const fallback = [];

  if (!props.customData.hide_cover) {
    fallback.push({
      id: 'cover',
      component: CoverBlock,
      config: props.customData.cover || {}
    });
  }

  if (props.customData.has_timer || props.customData.timer) {
    fallback.push({
      id: 'timer',
      component: CountdownTimer,
      config: props.customData.timer || {}
    });
  }

  if (props.customData.has_timeline || props.customData.timeline) {
    fallback.push({
      id: 'timeline',
      component: TimelineBlock,
      config: props.customData.timeline || {}
    });
  }

  if (!props.customData.hide_rsvp) {
    fallback.push({
      id: 'rsvp',
      component: RsvpFormBlock,
      config: props.customData.rsvp || {}
    });
  }

  return fallback;
});

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
