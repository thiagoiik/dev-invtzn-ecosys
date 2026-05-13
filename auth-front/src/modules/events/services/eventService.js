import invtznClient from '@/core/api/invtznClient';

export const eventService = {
  // Obtener todos los eventos del usuario activo
  fetchMyEvents() {
    return invtznClient.get('events/');
  },
  
  // Crear un nuevo evento
  createEvent(eventData) {
    return invtznClient.post('events/', eventData);
  }
};
