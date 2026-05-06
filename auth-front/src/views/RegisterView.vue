<template>
  <div class="register-container">
    <h2>Crear Cuenta</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Usuario:</label>
        <input v-model="form.username" type="text" required maxlength="150" />
      </div>
      <div class="form-group">
        <label>Email (Opcional):</label>
        <input v-model="form.email" type="email" />
      </div>
      <div class="form-group">
        <label>Contraseña:</label>
        <input v-model="form.password1" type="password" required />
      </div>
      <div class="form-group">
        <label>Confirmar Contraseña:</label>
        <input v-model="form.password2" type="password" required />
      </div>
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Registrando...' : 'Registrarse' }}
      </button>
    </form>
    <router-link to="/login">¿Ya tienes cuenta? Inicia sesión</router-link>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { authService } from '@/services/authService';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();
const loading = ref(false);

// Reflejamos estrictamente los parámetros que espera el backend: username, email, password1, password2
const form = reactive({
  username: '', // Se validó maxlength="150" para el username
  email: '',    // Se eliminó el atributo required del email (la API lo marcaba como opcional)
  password1: '',
  password2: ''
});

const handleRegister = async () => {
  if (form.password1 !== form.password2) {
    return toast.warning('Las contraseñas no coinciden.');
  }

  loading.value = true;
  try {
    await authService.register(form);
    toast.success('¡Registro exitoso! Por favor, verifica tu correo.');
    router.push({ name: 'login' });
  } catch (error) {
    toast.error('Error al registrar. Verifica los datos ingresados.');
  } finally {
    loading.value = false;
  }
};
</script>