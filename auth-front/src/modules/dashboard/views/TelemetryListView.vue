<template>
  <div class="telemetry-list-container p-6">
    <h1 class="text-2xl font-bold mb-4">Registro de Errores (Telemetría Sandbox)</h1>
    
    <div class="overflow-x-auto">
      <table class="table w-full bg-base-100 shadow-xl rounded-lg">
        <thead>
          <tr class="bg-base-200">
            <th>ID</th>
            <th>Usuario</th>
            <th>Rol</th>
            <th>Resolución</th>
            <th>Fecha</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" class="text-center py-4">
              <span class="loading loading-spinner loading-lg text-primary"></span>
            </td>
          </tr>
          <tr v-else-if="sessions.length === 0">
            <td colspan="6" class="text-center py-4 text-gray-500">No hay reportes de errores en el Sandbox.</td>
          </tr>
          <tr v-for="session in sessions" :key="session.id" class="hover">
            <td>#{{ session.id }}</td>
            <td>{{ session.user_name || 'Anónimo' }}</td>
            <td><div class="badge badge-outline">{{ session.role }}</div></td>
            <td>{{ session.window_width }}x{{ session.window_height }}</td>
            <td>{{ new Date(session.created_at).toLocaleString() }}</td>
            <td>
              <div class="flex gap-2">
                <button @click="openPlayer(session.id)" class="btn btn-sm btn-primary">
                  ▶ Reproducir
                </button>
                <button @click="deleteSession(session.id)" class="btn btn-sm btn-error btn-outline">
                  🗑️ Eliminar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para el reproductor -->
    <dialog id="telemetry_modal" class="modal">
      <div class="modal-box w-11/12 max-w-5xl bg-gray-900 text-white relative">
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <h3 class="font-bold text-lg mb-4">Reproducción de Sesión #{{ currentSessionId }}</h3>
        
        <!-- Contenedor dinámico del componente reproductor -->
        <div v-if="currentSessionId">
          <TelemetryPlayer :session-id="currentSessionId" />
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axiosModule from 'axios';
const axios = axiosModule.default || axiosModule;
import TelemetryPlayer from '../components/TelemetryPlayer.vue';
import { useAuthStore } from '@/modules/auth/store/auth';

const sessions = ref([]);
const loading = ref(true);
const currentSessionId = ref(null);
const authStore = useAuthStore();

const fetchSessions = async () => {
  try {
    const baseURL = import.meta.env.VITE_API_INVTZN_URL;
    const response = await axios.get(`${baseURL}telemetry/sessions/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });
    sessions.value = response.data;
  } catch (error) {
    console.error('Error al cargar las sesiones de telemetría:', error);
  } finally {
    loading.value = false;
  }
};

const deleteSession = async (id) => {
  if (!confirm('¿Estás seguro de que quieres eliminar esta grabación?')) return;
  
  try {
    const baseURL = import.meta.env.VITE_API_INVTZN_URL;
    await axios.delete(`${baseURL}telemetry/sessions/${id}/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    });
    // Remove from UI
    sessions.value = sessions.value.filter(s => s.id !== id);
  } catch (error) {
    console.error('Error al eliminar la sesión:', error);
    alert('Ocurrió un error al eliminar. Revisa la consola.');
  }
};

const openPlayer = (id) => {
  currentSessionId.value = null; // Reiniciar componente
  setTimeout(() => {
    currentSessionId.value = id;
    document.getElementById('telemetry_modal').showModal();
  }, 50);
};

onMounted(() => {
  fetchSessions();
});
</script>

<style scoped>
/* Estilos adicionales si es necesario */
</style>
