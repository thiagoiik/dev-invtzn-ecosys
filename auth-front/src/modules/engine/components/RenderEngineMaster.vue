<template>
  <div 
    class="min-h-screen relative overflow-x-hidden transition-all duration-500"
    :class="[
      `style-${customData.theme?.block_style || 'glassmorphic'}`
    ]"
    :style="[
      themeVariables,
      contentBgStyle
    ]"
  >
    <!-- Under Construction Screen for external guests if Draft status -->
    <UnderConstructionScreen 
      v-if="status === 'DRAFT' && !isStudioMode && !isOwner && !isTeamMember" 
    />

    <template v-else>
      <!-- Background Music Audio player if configured -->
      <AudioPlayer 
        v-if="customData.audioUrl || customData.has_music" 
        :config="customData.music || { audioUrl: customData.audioUrl }" 
      />

      <!-- Sandbox Premium Overlay if Draft status and visitor is Owner -->
      <DraftWatermarkOverlay 
        v-if="status === 'DRAFT' && !isStudioMode && showWatermark" 
        @purchase="handlePurchaseRedirect" 
      />

      <!-- Floating team member bar if Draft or Active status -->
      <div 
        v-if="['DRAFT', 'ACTIVE'].includes(status) && !isStudioMode && isTeamMember" 
        class="fixed top-0 left-0 right-0 bg-slate-900 text-white text-center py-2 z-50 flex items-center justify-center gap-4 text-xs font-black tracking-wider shadow-md px-4"
      >
        <span class="uppercase">
          <template v-if="status === 'ACTIVE'">🎨 Plantilla de Catálogo</template>
          <template v-else>🛠️ {{ barLabel }}</template>
        </span>
        <a 
          v-if="['ADMIN', 'DESIGNER'].includes(currentRole)"
          :href="`/builder/${deploymentId}`"
          class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-black px-3 py-1 rounded-lg uppercase transition-colors text-[10px]"
        >
          Editar en Builder
        </a>
      </div>

      <!-- Render Blocks dynamically based on configuration -->
      <div 
        class="master-canvas" 
        :class="{ 
          'pt-[44px]': (status === 'DRAFT' && !isStudioMode && showWatermark),
          'pt-[36px]': (['DRAFT', 'ACTIVE'].includes(status) && !isStudioMode && isTeamMember)
        }"
      >
        <template v-for="(block, idx) in orderedBlocks" :key="block.id">
          <SectionDivider 
            v-if="idx > 0 && customData.theme?.divider_style" 
            :style-name="customData.theme.divider_style" 
          />
          <component
            :is="block.component"
            :id="block.id"
            :config="block.config"
            v-bind="block.id === 'rsvp' ? { slug: slug, tierLevel: tierLevel } : {}"
          />
        </template>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import DraftWatermarkOverlay from './DraftWatermarkOverlay.vue';
import UnderConstructionScreen from './UnderConstructionScreen.vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import CoverBlock from './CoverBlock.vue';
import AudioPlayer from './AudioPlayer.vue';
import CountdownTimer from './CountdownTimer.vue';
import TimelineBlock from './TimelineBlock.vue';
import RsvpFormBlock from './RsvpFormBlock.vue';
import GiftTableBlock from './GiftTableBlock.vue';
import PhotoCarouselBlock from './PhotoCarouselBlock.vue';
import LocationBlock from './LocationBlock.vue';
import SectionDivider from './SectionDivider.vue';
import { useTelemetry } from '../composables/useTelemetry';
import DressCodeBlock from './DressCodeBlock.vue';
import ProtocolWordsBlock from './ProtocolWordsBlock.vue';
import InvitationTextBlock from './InvitationTextBlock.vue';
import { COLOR_PALETTES, CONTENT_TEXTURES } from '@/modules/builder/constants/palettes';

const props = defineProps({
  status: { type: String, required: true },
  customData: { type: Object, required: true },
  slug: { type: String, required: true },
  deploymentId: { type: [Number, String], default: null },
  isStudioMode: { type: Boolean, default: false },
  tierLevel: { type: String, default: 'BASIC' },
  ownerId: { type: [Number, String], default: null }
});

const emit = defineEmits(['purchase']);

const telemetry = useTelemetry();

let authStore = null;
try {
  authStore = useAuthStore();
} catch (e) {
  // Fail-safe for unit testing
}

const currentRole = computed(() => authStore?.role || null);

const isTeamMember = computed(() => {
  return ['ADMIN', 'DESIGNER', 'VENDOR', 'FRANCHISEE'].includes(currentRole.value);
});

const isOwner = computed(() => {
  const isMatched = authStore?.user && (
    String(authStore.user.pk) === String(props.ownerId) || 
    String(authStore.user.id) === String(props.ownerId)
  );
  const isLocalSandbox = !props.ownerId && localStorage.getItem('pending_sandbox_id') == props.deploymentId;
  return !!(isMatched || isLocalSandbox);
});

const showWatermark = computed(() => {
  return props.status === 'DRAFT' && !props.isStudioMode && isOwner.value;
});

const barLabel = computed(() => {
  const role = currentRole.value;
  if (role === 'ADMIN') return 'Modo Administrador';
  if (role === 'DESIGNER') return 'Modo Diseñador';
  if (role === 'VENDOR') return 'Modo Vendedor';
  if (role === 'FRANCHISEE') return 'Modo Franquicia';
  return 'Modo Staff';
});

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
  RsvpFormBlock: RsvpFormBlock,
  GiftTableBlock: GiftTableBlock,
  PhotoCarouselBlock: PhotoCarouselBlock,
  LocationBlock: LocationBlock,
  DressCodeBlock: DressCodeBlock,
  ProtocolWordsBlock: ProtocolWordsBlock,
  InvitationTextBlock: InvitationTextBlock
};

const orderedBlocks = computed(() => {
  // Caso 1: Estructura moderna con ordenamiento dinámico
  if (Array.isArray(props.customData.blocks)) {
    const list = props.customData.blocks
      .map(b => {
        // Resolver la configuración desde las llaves de nivel superior para garantizar reactividad en tiempo real
        let resolvedConfig = b.config || {};
        if (b.id === 'cover') {
          resolvedConfig = props.customData.cover || {};
        } else if (b.id === 'rsvp') {
          resolvedConfig = props.customData.rsvp || {};
        } else if (b.id === 'timer') {
          resolvedConfig = props.customData.timer || {};
        } else if (b.id === 'timeline') {
          resolvedConfig = props.customData.timeline || {};
        } else if (b.id === 'gift_table') {
          resolvedConfig = props.customData.gift_table || {};
        } else if (b.id === 'photo_carousel') {
          resolvedConfig = props.customData.photo_carousel || {};
        } else if (b.id === 'location') {
          resolvedConfig = {
            ...(props.customData.location || {}),
            locations: props.customData.locations || null
          };
        } else if (b.id === 'dress_code') {
          resolvedConfig = props.customData.dressCode || {};
        } else if (b.id.startsWith('protocol_words_')) {
          resolvedConfig = props.customData[b.id] || {};
        } else if (b.id.startsWith('invitation_text_') || b.id === 'invitation_text') {
          resolvedConfig = props.customData[b.id] || {};
        }

        return {
          id: b.id,
          component: componentMap[b.type],
          config: resolvedConfig,
          visible: b.visible !== false
        };
      })
      .filter(b => b.component && b.visible);

    const hasDressCode = list.some(b => b.id === 'dress_code');
    if (!hasDressCode && props.customData.has_dress_code) {
      const rsvpIdx = list.findIndex(b => b.id === 'rsvp');
      const dressCodeBlock = {
        id: 'dress_code',
        component: DressCodeBlock,
        config: props.customData.dressCode || {},
        visible: true
      };
      if (rsvpIdx !== -1) {
        list.splice(rsvpIdx, 0, dressCodeBlock);
      } else {
        list.push(dressCodeBlock);
      }
    }
    return list;
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

  if (props.customData.has_gift_table || props.customData.gift_table) {
    fallback.push({
      id: 'gift_table',
      component: GiftTableBlock,
      config: props.customData.gift_table || {}
    });
  }

  if (props.customData.has_photo_carousel || props.customData.photo_carousel) {
    fallback.push({
      id: 'photo_carousel',
      component: PhotoCarouselBlock,
      config: props.customData.photo_carousel || {}
    });
  }

  if (props.customData.has_location || props.customData.location || props.customData.locations) {
    fallback.push({
      id: 'location',
      component: LocationBlock,
      config: {
        ...(props.customData.location || {}),
        locations: props.customData.locations || null
      }
    });
  }

  if (props.customData.has_dress_code) {
    fallback.push({
      id: 'dress_code',
      component: DressCodeBlock,
      config: props.customData.dressCode || {}
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

const activePalette = computed(() => {
  const theme = props.customData.theme || {};
  const paletteId = theme.palette_id || 'classic_navy';
  return COLOR_PALETTES.find(p => p.id === paletteId) || COLOR_PALETTES[0];
});

const activeTexture = computed(() => {
  const theme = props.customData.theme || {};
  if (theme.content_bg_type !== 'texture') return null;
  const textureId = theme.content_bg_texture || 'none';
  return CONTENT_TEXTURES.find(t => t.id === textureId) || null;
});

const contentBgStyle = computed(() => {
  const theme = props.customData.theme || {};
  if (theme.content_bg_type === 'texture') {
    const texture = activeTexture.value;
    if (texture && texture.style) {
      const styleObj = {};
      if (texture.id === 'starry_night') {
        styleObj.background = 'radial-gradient(circle, rgba(20,20,35,1) 0%, rgba(3,7,18,1) 100%)';
        styleObj.backgroundImage = 'radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px), radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px)';
        styleObj.backgroundSize = '550px 550px, 350px 350px';
        styleObj.backgroundPosition = '0 0, 40px 60px';
      } else if (texture.url) {
        styleObj.backgroundImage = `url("${texture.url}")`;
        styleObj.backgroundRepeat = 'repeat';
        if (texture.id === 'watercolor_soft') {
          styleObj.backgroundRepeat = 'no-repeat';
          styleObj.backgroundSize = 'cover';
          styleObj.backgroundPosition = 'center';
        }
      }
      return styleObj;
    }
  }
  return {
    backgroundColor: activePalette.value.colors.contentBg
  };
});

// Generates dynamic brand color palletes using HSL variables
const themeVariables = computed(() => {
  const palette = activePalette.value;
  const theme = props.customData.theme || {};
  const h = theme.hue || 38;      // Golden hue
  const s = theme.saturation || '80%';
  const l = theme.lightness || '50%';

  const vars = {
    '--p': `${h} ${s} ${l}`, // Primary brand color variable
    '--color-primary': palette.colors.primary,
    '--color-secondary': palette.colors.secondary,
    '--color-accent': palette.colors.accent,
    '--color-block-bg': palette.colors.blockBg,
    '--color-card-bg': palette.colors.cardBg,
    '--color-content-bg': palette.colors.contentBg,
  };

  if (palette.colors.primaryGradient) {
    vars['--color-accent-gradient'] = palette.colors.primaryGradient;
  }

  return vars;
});
</script>

<style scoped>
/* Divisores dinámicos del estilo de bloques */
.style-solid_bands :deep(.max-w-4xl),
.style-solid_bands :deep(.max-w-6xl) {
  max-width: 100% !important;
  border-radius: 0px !important;
  border: none !important;
  box-shadow: none !important;
  margin-top: 0px !important;
  margin-bottom: 0px !important;
  background-color: var(--color-block-bg) !important;
  backdrop-filter: none !important;
}

.style-minimal :deep(.max-w-4xl),
.style-minimal :deep(.max-w-6xl) {
  max-width: 100% !important;
  border-radius: 0px !important;
  border: none !important;
  box-shadow: none !important;
  background-color: transparent !important;
  backdrop-filter: none !important;
  margin-top: 1rem !important;
  margin-bottom: 1rem !important;
}

/* Inyección de variables cromáticas en textos y elementos */
:deep(h2:not(#cover h2)),
:deep(h3:not(#cover h3):not(.text-primary)) {
  color: var(--color-primary) !important;
}

:deep(p:not(#cover p)) {
  color: var(--color-secondary) !important;
}

:deep(.text-primary:not(#cover *)),
:deep(.text-indigo-500:not(#cover *)),
:deep(.text-amber-500:not(#cover *)) {
  color: var(--color-accent) !important;
}

:deep(.btn-primary) {
  background: var(--color-accent-gradient, var(--color-accent)) !important;
  border-color: var(--color-accent) !important;
  color: white !important;
}

:deep(.border-primary),
:deep(.border-indigo-500) {
  border-color: var(--color-accent) !important;
}

:deep(.bg-primary) {
  background-color: var(--color-accent) !important;
}

/* Tarjetas y detalles internos adaptados a la paleta */
:deep(.max-w-4xl) .bg-white\/80,
:deep(.max-w-4xl) .bg-white,
:deep(.max-w-4xl) .bg-slate-50,
:deep(.max-w-6xl) .bg-white\/80,
:deep(.max-w-6xl) .bg-white,
:deep(.max-w-6xl) .bg-slate-50 {
  background-color: var(--color-card-bg) !important;
  border-color: rgba(255,255,255,0.08) !important;
}
</style>
