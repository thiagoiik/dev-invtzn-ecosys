<template>
  <div v-if="isActive" class="fixed bottom-4 right-4 z-[9999]">
    <button 
      @click="() => reportError(false)"
      :disabled="isReporting"
      class="btn btn-error shadow-lg rounded-full flex items-center gap-2 animate-bounce hover:animate-none"
    >
      <span v-if="isReporting" class="loading loading-spinner loading-xs"></span>
      <span v-else>🔴</span>
      {{ isReporting ? 'Enviando...' : 'Reportar Error' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useAuthStore } from '../modules/auth/store/auth';
import axiosModule from 'axios';
const axios = axiosModule.default || axiosModule;
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const toast = useToast();

const isReporting = ref(false);
const isActive = computed(() => {
  return import.meta.env.VITE_APP_ENV === 'sandbox' && authStore.isAuthenticated;
});

let events = [];
let stopFn = null;
const BUFFER_SIZE = 100; // Opcionalmente limitar por cantidad o por tiempo (60s)
const MAX_TIME_MS = 60 * 1000;

const startRecording = async () => {
  if (!isActive.value) return;

  try {
    // Importación dinámica para no afectar el bundle de producción
    const rrweb = await import('rrweb');
    
    stopFn = rrweb.record({
      emit(event) {
        events.push(event);
        
        // Rolling Buffer: Limpiar eventos más antiguos a 60 segundos
        const now = Date.now();
        // rrweb events tienen timestamp en ms
        events = events.filter(e => (now - e.timestamp) <= MAX_TIME_MS);
      },
      // Ignorar contraseñas u otros datos sensibles si es necesario
      maskAllInputs: true,
    });
    
    console.log("[Telemetry] Grabación de rrweb iniciada (Rolling buffer de 60s).");
  } catch (error) {
    console.error("[Telemetry] Error al cargar rrweb:", error);
  }
};

const reportError = async (isAuto = false, errorMessage = '') => {
  if (events.length === 0) {
    if (!isAuto) toast.warning("No hay suficientes datos grabados aún.");
    return;
  }

  isReporting.value = true;
  
  try {
    const payload = {
      events: events,
      window_width: window.innerWidth,
      window_height: window.innerHeight,
      error_message: errorMessage
    };
    
    // Asumiendo que el endpoint de telemetría está en la API de INVTZN
    const baseURL = import.meta.env.VITE_API_INVTZN_URL; 
    
    await axios.post(`${baseURL}telemetry/record-session/`, payload, {
      headers: {
        Authorization: `Bearer ${authStore.token}` // Si es que el endpoint requiere auth
      }
    });
    
    if (!isAuto) {
      toast.success("¡Reporte enviado exitosamente! Los ingenieros revisarán tu sesión.");
    }
  } catch (error) {
    console.error("Error al enviar el reporte rrweb:", error);
    if (!isAuto) toast.error("Ocurrió un error al enviar el reporte.");
  } finally {
    isReporting.value = false;
  }
};

let lastAutoReportTime = 0;
const AUTO_REPORT_COOLDOWN = 60 * 1000; // 1 minuto de enfriamiento

const handleGlobalError = (event) => {
  if (!isActive.value) return;
  const now = Date.now();
  if (now - lastAutoReportTime < AUTO_REPORT_COOLDOWN) return; // Evitar spam

  lastAutoReportTime = now;
  let errorMessage = 'Error JS desconocido';

  if (event instanceof ErrorEvent) {
    errorMessage = event.message;
  } else if (event instanceof PromiseRejectionEvent) {
    errorMessage = event.reason?.message || event.reason?.toString() || 'Promesa rechazada';
  }

  console.warn("[Telemetry] Auto-reportando error detectado:", errorMessage);
  reportError(true, errorMessage);
};

onMounted(() => {
  if (isActive.value) {
    startRecording();
    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleGlobalError);
  }
});

onBeforeUnmount(() => {
  if (stopFn) stopFn();
  window.removeEventListener('error', handleGlobalError);
  window.removeEventListener('unhandledrejection', handleGlobalError);
});
</script>
