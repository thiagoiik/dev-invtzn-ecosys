<template>
  <div>
    <h3 class="text-2xl font-bold text-center mb-6 text-slate-800">Crear Cuenta</h3>
    <form @submit.prevent="handleRegister" class="space-y-4">
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Usuario</span></label>
        <input v-model="form.username" type="text" class="input input-bordered w-full" required maxlength="150" />
      </div>
      
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Email (Opcional)</span></label>
        <input v-model="form.email" type="email" class="input input-bordered w-full" />
      </div>
      
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Contraseña</span></label>
        <input v-model="form.password1" type="password" class="input input-bordered w-full" required />
      </div>
      
      <div class="form-control w-full">
        <label class="label"><span class="label-text font-semibold">Confirmar Contraseña</span></label>
        <input v-model="form.password2" type="password" class="input input-bordered w-full" required />
      </div>
      
      <div class="mt-6">
        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
          <span v-if="loading" class="loading loading-spinner"></span>
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>
      </div>
    </form>
    
    <div class="mt-6 text-center text-sm">
      <router-link to="/login" class="link link-primary">¿Ya tienes cuenta? Inicia sesión</router-link>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { authService } from '@/modules/auth/services/authService';
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