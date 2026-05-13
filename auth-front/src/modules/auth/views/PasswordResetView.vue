<template>
  <div class="auth-container">
    <h2>Recuperar Contraseña</h2>
    <p>Introduce tu correo y te enviaremos un enlace con las instrucciones.</p>
    <form @submit.prevent="handleReset">
      <div class="form-group">
        <input v-model="email" type="email" placeholder="Correo electrónico" required :disabled="loading" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Enviando...' : 'Enviar enlace de recuperación' }}
      </button>
    </form>
    <router-link to="/login">Volver al inicio de sesión</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { authService } from '@/modules/auth/services/authService';
import { useToast } from 'vue-toastification';

const email = ref('');
const loading = ref(false);
const toast = useToast();

const handleReset = async () => {
  loading.value = true;
  try {
    await authService.passwordReset(email.value); 
    toast.success("Si el correo existe en nuestro sistema, recibirás las instrucciones en breve.");
    email.value = ''; // Limpiamos el formulario por seguridad
  } catch (error) {
    toast.error("Ocurrió un error al intentar enviar el enlace. Inténtalo de nuevo.");
  } finally {
    loading.value = false;
  }
};
</script>