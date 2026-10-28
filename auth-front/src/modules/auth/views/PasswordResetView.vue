<template>
  <div>
    <h3 class="text-2xl font-bold text-center mb-4 text-slate-800">Recuperar Contraseña</h3>
    <p class="text-center text-sm text-slate-600 mb-6">Introduce tu correo y te enviaremos un enlace con las instrucciones.</p>
    
    <form @submit.prevent="handleReset" class="space-y-4">
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Correo Electrónico</span></label>
        <input v-model="email" type="email" placeholder="Ej. correo@ejemplo.com" class="input input-bordered w-full" required :disabled="loading" />
      </div>
      
      <div class="mt-6">
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          <span v-if="loading" class="loading loading-spinner"></span>
          {{ loading ? 'Enviando...' : 'Enviar enlace' }}
        </button>
      </div>
    </form>
    
    <div class="mt-6 text-center text-sm">
      <router-link to="/login" class="link link-primary">Volver al inicio de sesión</router-link>
    </div>
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