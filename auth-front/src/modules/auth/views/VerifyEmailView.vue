<template>
  <div class="verify-email-container">
    <h2>Verificación de Cuenta</h2>
    
    <div v-if="!loading && !success && !error">
      <p>Estás a un solo paso. Haz clic en el botón para confirmar tu cuenta.</p>
      <button @click="verifyAccount">Confirmar mi correo electrónico</button>
    </div>

    <p v-if="loading">Verificando tu correo electrónico, por favor espera...</p>
    <p v-if="success" class="success-message">¡Tu correo ha sido verificado con éxito! Redirigiendo al inicio de sesión...</p>
    <p v-if="error" class="error-message">Ocurrió un error al verificar tu correo. El enlace puede ser inválido o haber expirado.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authService } from '@/modules/auth/services/authService';
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();

// Ahora no cargamos la petición por defecto
const loading = ref(false);
const success = ref(false);
const error = ref(false);
const key = ref(null);

onMounted(() => {
  // Captura la llave (key) desde los parámetros dinámicos de la ruta
  key.value = route.params.key || route.query.key;

  if (!key.value) {
    error.value = true;
    toast.error('Falta la clave de verificación en la URL.');
  }
});

// La mejor práctica para evitar que robots de correo o dobles recargas quemen la sesión, es no realizar la petición POST automáticamente al cargar la página
const verifyAccount = async () => {
  loading.value = true;
  error.value = false;

  try {
    await authService.verifyEmail(key.value); 
    success.value = true;
    toast.success('Correo verificado exitosamente.');
    
    setTimeout(() => {
      router.push({ name: 'login' });
    }, 3000);
  } catch (err) {
    error.value = true;
    toast.error('El enlace es inválido o ya fue utilizado.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.verify-email-container {
  max-width: 400px;
  margin: 50px auto;
  text-align: center;
}
.success-message { color: green; }
.error-message { color: red; }
button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
button:hover {
  background-color: #45a049;
}
</style>