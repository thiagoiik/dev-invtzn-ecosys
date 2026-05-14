<template>
  <div>
    <h3 class="text-2xl font-bold text-center mb-6 text-slate-800">Iniciar Sesión</h3>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Usuario o Email</span></label>
        <input v-model="usernameOrEmail" type="text" placeholder="Ej. juanperez" class="input input-bordered w-full" :disabled="loading" required />
      </div>
      
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Contraseña</span></label>
        <input v-model="password" type="password" placeholder="••••••••" class="input input-bordered w-full" :disabled="loading" required />
      </div>
      
      <div class="mt-6">
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          <span v-if="loading" class="loading loading-spinner"></span>
          {{ loading ? 'Entrando...' : 'Ingresar' }}
        </button>
      </div>
      
      <p v-if="error" class="text-error text-sm text-center mt-2">{{ error }}</p>
    </form>
    
    <div class="mt-6 flex flex-col gap-2 text-center text-sm">
      <router-link to="/auth/registration" class="link link-primary">¿No tienes cuenta? Regístrate aquí</router-link>
      <router-link to="/password-reset" class="link link-hover text-slate-500">¿Olvidaste tu contraseña?</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
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