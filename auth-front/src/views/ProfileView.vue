<template>
  <div class="profile-container" v-if="authStore.user">
    <h2>Mi Perfil</h2>
    
    <section class="user-info">
      <p><strong>Email:</strong> {{ authStore.user.email }} <small>(No editable)</small></p>
    </section>

    <hr />

    <h3>Editar Datos Personales</h3>
    <form @submit.prevent="handleUpdateProfile">
      <div class="form-group">
        <label>Usuario:</label>
        <input v-model="editForm.username" type="text" required :disabled="loadingProfile" />
      </div>
      <div class="form-group">
        <label>Nombre:</label>
        <input v-model="editForm.first_name" type="text" :disabled="loadingProfile" />
      </div>
      <div class="form-group">
        <label>Apellidos:</label>
        <input v-model="editForm.last_name" type="text" :disabled="loadingProfile" />
      </div>
      <button type="submit" :disabled="loadingProfile">
        {{ loadingProfile ? 'Guardando...' : 'Guardar Cambios' }}
      </button>
    </form>

    <hr />

    <h3>Cambiar Contraseña</h3>
    <form @submit.prevent="handleChangePassword">
      <div class="form-group">
        <input v-model="pwForm.old_password" type="password" placeholder="Contraseña actual" required :disabled="loadingPassword" />
      </div>
      <div class="form-group">
        <input v-model="pwForm.new_password1" type="password" placeholder="Nueva contraseña" required :disabled="loadingPassword" />
      </div>
      <div class="form-group">
        <input v-model="pwForm.new_password2" type="password" placeholder="Confirmar nueva contraseña" required :disabled="loadingPassword" />
      </div>
      <button type="submit" :disabled="loadingPassword">
        {{ loadingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { authService } from '@/services/authService';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const toast = useToast();

// Estados de carga independientes
const loadingProfile = ref(false);
const loadingPassword = ref(false);

// Estado para la edición del perfil
const editForm = ref({
  username: '',
  first_name: '',
  last_name: ''
});

// Estado para el cambio de contraseña
const pwForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
});

// Precargar los datos actuales del usuario al montar el componente
onMounted(() => {
  if (authStore.user) {
    editForm.value.username = authStore.user.username || '';
    editForm.value.first_name = authStore.user.first_name || '';
    editForm.value.last_name = authStore.user.last_name || '';
  }
});

// Manejador para actualizar el perfil
const handleUpdateProfile = async () => {
  // 1. Creamos un objeto vacío para guardar solo lo modificado
  const changedData = {};

  // 2. Comparamos el formulario con los datos originales del Store
  if (editForm.value.username !== authStore.user.username) {
    changedData.username = editForm.value.username;
  }
  if (editForm.value.first_name !== authStore.user.first_name) {
    changedData.first_name = editForm.value.first_name;
  }
  if (editForm.value.last_name !== authStore.user.last_name) {
    changedData.last_name = editForm.value.last_name;
  }

  // 3. Si el objeto está vacío, detenemos la función y avisamos al usuario
  if (Object.keys(changedData).length === 0) {
    return toast.info("No has realizado ningún cambio en tus datos.");
  }

  loadingProfile.value = true;
  try {
    // 4. Implementar actualización de datos del usuario (PATCH /user/) enviando únicamente los campos modificados para evitar falsos positivos de duplicidad
    const response = await authService.updateUserDetails(changedData);
    
    // Actualizamos el Store con los nuevos datos devueltos por el servidor
    authStore.user = response.data; 
    toast.success("Perfil actualizado correctamente.");
    
  } catch (error) {
    // 5. Manejo dinámico de errores: El backend bloquea la petición si el nombre de usuario ya existe en la base de datos y le pertenece a otra persona
    if (error.response && error.response.data) {
      const data = error.response.data;
      if (data.username) {
        toast.warning(`Error en Usuario: ${data.username[0]}`);
      } else {
        toast.error("Verifica los datos ingresados.");
      }
    } else {
      toast.error("Error de conexión al actualizar el perfil.");
    }
  } finally {
    loadingProfile.value = false;
  }
};

// Manejador para cambiar la contraseña
const handleChangePassword = async () => {
  if (pwForm.value.new_password1 !== pwForm.value.new_password2) {
    return toast.warning("Las contraseñas nuevas no coinciden.");
  }
  
  loadingPassword.value = true;
  try {
    await authService.passwordChange(pwForm.value);
    toast.success("Tu contraseña ha sido actualizada correctamente.");
    pwForm.value = { old_password: '', new_password1: '', new_password2: '' };
  } catch (error) {
    toast.error("Error al actualizar. Verifica que tu contraseña actual sea correcta.");
  } finally {
    loadingPassword.value = false;
  }
};
</script>