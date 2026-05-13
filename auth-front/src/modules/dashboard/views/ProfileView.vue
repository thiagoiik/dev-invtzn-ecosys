<template>
  <div class="profile-container" v-if="authStore.user">
    <h2>Mi Perfil</h2>
    
    <section class="user-info">
      <p><strong>Email:</strong> {{ authStore.user.email }} <small>(No editable)</small></p>
      
      <!-- Nuevos campos traídos de api-invtzn -->
      <div v-if="invtznProfile" class="business-profile">
        <p><strong>Rol en la plataforma:</strong> {{ invtznProfile.custom_role }}</p>
        <p><strong>Tipo de Cliente:</strong> {{ invtznProfile.customer_type }}</p>
        <p><strong>Saldo en Billetera:</strong> ${{ invtznProfile.current_balance }}</p>
      </div>
      <div v-else-if="loadingInvtzn">
        <p><em>Cargando perfil de negocio...</em></p>
      </div>
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
      <div class="form-group">
        <label>Teléfono (WhatsApp):</label>
        <input v-model="editForm.phone_number" type="text" :disabled="loadingProfile" />
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
import { useAuthStore } from '@/modules/auth/store/auth';
import { authService } from '@/modules/auth/services/authService';
import { profileService } from '@/modules/dashboard/services/profileService';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const toast = useToast();

// Estados de carga independientes
const loadingProfile = ref(false);
const loadingPassword = ref(false);
const loadingInvtzn = ref(false);

// Datos del perfil de api-invtzn
const invtznProfile = ref(null);

// Estado para la edición del perfil
const editForm = ref({
  username: '',
  first_name: '',
  last_name: '',
  phone_number: ''
});

// Estado para el cambio de contraseña
const pwForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
});

// Precargar los datos actuales del usuario al montar el componente
onMounted(async () => {
  if (authStore.user) {
    editForm.value.username = authStore.user.username || '';
    editForm.value.first_name = authStore.user.first_name || '';
    editForm.value.last_name = authStore.user.last_name || '';
  }
  
  // Cargar perfil de negocio de api-invtzn
  loadingInvtzn.value = true;
  try {
    const response = await profileService.fetchMyProfile();
    invtznProfile.value = response.data;
    editForm.value.phone_number = response.data.phone_number || '';
  } catch (error) {
    toast.error('No se pudo cargar el perfil de negocio.');
  } finally {
    loadingInvtzn.value = false;
  }
});

// Manejador para actualizar el perfil
const handleUpdateProfile = async () => {
  // 1. Creamos un objeto vacío para guardar solo lo modificado
  const changedAuthData = {};
  const changedInvtznData = {};

  // 2. Comparamos el formulario con los datos originales del Store y de invtznProfile
  if (editForm.value.username !== authStore.user.username) {
    changedAuthData.username = editForm.value.username;
  }
  if (editForm.value.first_name !== authStore.user.first_name) {
    changedAuthData.first_name = editForm.value.first_name;
  }
  if (editForm.value.last_name !== authStore.user.last_name) {
    changedAuthData.last_name = editForm.value.last_name;
  }
  if (invtznProfile.value && editForm.value.phone_number !== invtznProfile.value.phone_number) {
    changedInvtznData.phone_number = editForm.value.phone_number;
  }

  // 3. Si el objeto está vacío, detenemos la función y avisamos al usuario
  if (Object.keys(changedAuthData).length === 0 && Object.keys(changedInvtznData).length === 0) {
    return toast.info("No has realizado ningún cambio en tus datos.");
  }

  loadingProfile.value = true;
  try {
    // 4. Actualizar auth (username, nombre, apellido)
    if (Object.keys(changedAuthData).length > 0) {
      const response = await authService.updateUserDetails(changedAuthData);
      authStore.user = response.data; 
    }
    
    // 5. Actualizar api-invtzn (teléfono)
    if (Object.keys(changedInvtznData).length > 0) {
      const response = await profileService.updateMyProfile(changedInvtznData);
      invtznProfile.value = response.data;
    }
    
    toast.success("Perfil actualizado correctamente.");
  } catch (error) {
    // Manejo dinámico de errores: El backend bloquea la petición si el nombre de usuario ya existe en la base de datos
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