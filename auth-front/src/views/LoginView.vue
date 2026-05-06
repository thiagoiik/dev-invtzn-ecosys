<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <input v-model="usernameOrEmail" type="text" placeholder="Usuario o Email" :disabled="loading" required />
      <input v-model="password" type="password" placeholder="Contraseña" :disabled="loading" required />
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Entrando...' : 'Ingresar' }}
      </button>
      
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
    <router-link to="/password-reset">¿Olvidaste tu contraseña?</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const usernameOrEmail = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);

const handleLogin = async () => {
  error.value = null;
  loading.value = true;
  
  try {
    // Enviamos el identificador mapeado a 'username' y la contraseña
    await authStore.login({ 
      username: usernameOrEmail.value, 
      password: password.value 
    });
    
    toast.success('¡Bienvenido de vuelta!');
    router.push('/dashboard');
  } catch (err) {
    error.value = "Error al iniciar sesión. Revisa tus credenciales.";
    toast.error("Las credenciales no coinciden.");
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>