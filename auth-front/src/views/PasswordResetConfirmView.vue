<template>
  <div class="auth-container">
    <h2>Crear nueva contraseña</h2>
    <form @submit.prevent="handleConfirmReset">
      <div class="form-group">
        <input v-model="form.new_password1" type="password" placeholder="Nueva contraseña" required maxlength="128" :disabled="loading" />
      </div>
      <div class="form-group">
        <input v-model="form.new_password2" type="password" placeholder="Confirmar nueva contraseña" required maxlength="128" :disabled="loading" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Actualizando...' : 'Cambiar contraseña' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authService } from '@/services/authService';
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const loading = ref(false);

// El objeto reactivo incluye exactamente los 4 parámetros que pide el backend
const form = reactive({
  uid: '',
  token: '',
  new_password1: '',
  new_password2: ''
});

onMounted(() => {
  // Capturamos el uid y token que vienen en la URL 
  // (Ejemplo: misitio.com/password-reset-confirm/Mg/1wIhdl-token)
  form.uid = route.params.uid;
  form.token = route.params.token;
});

const handleConfirmReset = async () => {
  if (form.new_password1 !== form.new_password2) {
    return toast.warning("Las contraseñas no coinciden.");
  }

  loading.value = true;
  try {
    await authService.passwordResetConfirm(form);
    toast.success("Tu contraseña ha sido actualizada con éxito. Ya puedes iniciar sesión.");
    router.push({ name: 'login' });
  } catch (error) {
    toast.error("El enlace es inválido o ha expirado. Solicita uno nuevo.");
  } finally {
    loading.value = false;
  }
};
</script>