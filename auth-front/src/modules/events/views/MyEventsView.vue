<template>
  <div class="events-container">
    <h2>Mis Eventos</h2>

    <section class="new-event-section">
      <h3>Crear Nuevo Evento</h3>
      <form @submit.prevent="handleCreateEvent" class="event-form">
        <div class="form-group">
          <label>Título del Evento:</label>
          <input v-model="newEvent.title" type="text" placeholder="Ej: Boda de Martha y Pekas" required :disabled="loading" />
        </div>
        <div class="form-group">
          <label>Tipo de Evento:</label>
          <select v-model="newEvent.event_type" required :disabled="loading">
            <option value="BODA">Boda</option>
            <option value="XV">XV Años</option>
            <option value="BAUTIZO">Bautizo</option>
            <option value="CUMPLEANOS">Cumpleaños</option>
            <option value="CORPORATIVO">Corporativo</option>
            <option value="OTRO">Otro</option>
          </select>
        </div>
        <div class="form-group">
          <label>Fecha Principal:</label>
          <input v-model="newEvent.main_date" type="date" required :disabled="loading" />
        </div>
        <div class="form-group">
          <label>Lugar / Ciudad (Opcional):</label>
          <input v-model="newEvent.location_name" type="text" placeholder="Ej: Jardín Las Rosas, CDMX" :disabled="loading" />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Creando...' : 'Guardar Evento' }}
        </button>
      </form>
    </section>

    <hr />

    <section class="events-list-section">
      <h3>Lista de Eventos</h3>
      <div v-if="loadingEvents">
        <p><em>Cargando tus eventos...</em></p>
      </div>
      <div v-else-if="events.length === 0">
        <p>No tienes eventos registrados aún. ¡Crea el primero!</p>
      </div>
      <div v-else class="event-cards">
        <div v-for="event in events" :key="event.id" class="event-card">
          <h4>{{ event.title }}</h4>
          <p><strong>Tipo:</strong> {{ event.event_type }}</p>
          <p><strong>Fecha:</strong> {{ event.main_date }}</p>
          <p><strong>Lugar:</strong> {{ event.location_name || 'No especificado' }}</p>
          <p><strong>Estado:</strong> {{ event.is_active ? 'Activo' : 'Inactivo' }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { eventService } from '@/modules/events/services/eventService';
import { useToast } from 'vue-toastification';

const toast = useToast();

const events = ref([]);
const loadingEvents = ref(true);
const loading = ref(false);

const newEvent = ref({
  title: '',
  event_type: 'BODA',
  main_date: '',
  location_name: ''
});

const loadEvents = async () => {
  loadingEvents.value = true;
  try {
    const response = await eventService.fetchMyEvents();
    events.value = response.data;
  } catch (error) {
    toast.error('Ocurrió un error al cargar tus eventos.');
  } finally {
    loadingEvents.value = false;
  }
};

onMounted(() => {
  loadEvents();
});

const handleCreateEvent = async () => {
  loading.value = true;
  try {
    const response = await eventService.createEvent(newEvent.value);
    // Agregamos el nuevo evento a la lista reactiva inmediatamente
    events.value.unshift(response.data);
    toast.success('¡Evento creado con éxito!');
    
    // Limpiamos el formulario
    newEvent.value = {
      title: '',
      event_type: 'BODA',
      main_date: '',
      location_name: ''
    };
  } catch (error) {
    if (error.response && error.response.data) {
      toast.error('Revisa los datos ingresados. Formato inválido.');
    } else {
      toast.error('Error al intentar crear el evento.');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.events-container {
  max-width: 800px;
  margin: 0 auto;
}
.event-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
}
.event-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
.event-card {
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
  background: #f9f9f9;
}
.event-card h4 {
  margin-top: 0;
}
</style>
