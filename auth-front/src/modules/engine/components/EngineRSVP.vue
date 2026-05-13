<template>
  <div class="engine-rsvp" :style="{ backgroundColor: config.bgColor || '#f8fafc' }">
    <div class="rsvp-card">
      <h2>Confirma tu Asistencia</h2>
      <p>Nos encantaría contar con tu presencia.</p>
      
      <form @submit.prevent="submitRSVP" class="rsvp-form">
        <input type="text" placeholder="Nombre completo" required />
        <select required>
          <option value="">¿Asistirás?</option>
          <option value="yes">¡Sí, ahí estaré!</option>
          <option value="no">Lo siento, no podré asistir</option>
        </select>
        <button type="submit" :style="{ backgroundColor: config.btnColor || '#3b82f6' }">
          Enviar Confirmación
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
});

const submitRSVP = () => {
  alert('Esto es un componente de prueba del Engine. En el futuro esto hará POST a /rsvp/');
};
</script>

<style scoped>
.engine-rsvp {
  padding: 4rem 1rem;
  display: flex;
  justify-content: center;
}
.rsvp-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  max-width: 400px;
  width: 100%;
}
.rsvp-card h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}
.rsvp-card p {
  color: #64748b;
  margin-bottom: 1.5rem;
}
.rsvp-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
input, select {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 1rem;
}
button {
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
}
</style>
