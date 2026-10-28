<template>
  <div class="telemetry-player-wrapper flex flex-col items-center w-full min-h-[500px]">
    <div v-if="loading" class="flex flex-col items-center justify-center flex-1">
      <span class="loading loading-bars loading-lg text-primary mb-4"></span>
      <p class="text-sm">Descargando datos de la sesión...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

    <!-- Contenedor donde rrweb-player inyectará el video -->
    <div v-show="!loading && !error" ref="playerContainer" class="w-full bg-black rounded-lg overflow-hidden flex justify-center"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import axiosModule from 'axios';
const axios = axiosModule.default || axiosModule;
import { useAuthStore } from '@/modules/auth/store/auth';

const props = defineProps({
  sessionId: {
    type: Number,
    required: true
  }
});

const playerContainer = ref(null);
const loading = ref(true);
const error = ref(null);
const authStore = useAuthStore();
let playerInstance = null;

const loadAndPlaySession = async () => {
  if (!props.sessionId) return;
  
  loading.value = true;
  error.value = null;

  try {
    const baseURL = import.meta.env.VITE_API_INVTZN_URL;
    const response = await axios.get(`${baseURL}telemetry/sessions/${props.sessionId}/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });
    
    const events = response.data.events_payload;
    if (!events || events.length < 2) {
      error.value = "La sesión no tiene suficientes eventos para ser reproducida.";
      loading.value = false;
      return;
    }

    // Importación dinámica de rrweb-player para no afectar el bundle inicial
    const rrwebPlayer = (await import('rrweb-player')).default;
    await import('rrweb-player/dist/style.css'); // Importar estilos dinámicamente

    // Limpiar reproductor anterior si existiera
    if (playerInstance) {
      playerContainer.value.innerHTML = '';
    }

    // Inicializar reproductor
    playerInstance = new rrwebPlayer({
      target: playerContainer.value,
      props: {
        events: events,
        width: 800, // Puedes hacerlo responsivo después
        height: 500,
        autoPlay: true,
      },
    });

  } catch (err) {
    console.error("Error cargando sesión:", err);
    error.value = "Error al descargar el video de la sesión. Revisa la consola.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadAndPlaySession();
});

watch(() => props.sessionId, () => {
  loadAndPlaySession();
});

onBeforeUnmount(() => {
  // Limpiar DOM si es necesario al cerrar el modal
  if (playerContainer.value) {
    playerContainer.value.innerHTML = '';
  }
});
</script>

<style>
/* Forzar estilos del reproductor si es necesario para modo oscuro */
.telemetry-player-wrapper .rr-player {
  box-shadow: none !important;
  border-radius: 8px;
}
</style>
