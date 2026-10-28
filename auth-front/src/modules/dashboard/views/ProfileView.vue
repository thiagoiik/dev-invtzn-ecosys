<template>
  <div class="max-w-4xl mx-auto space-y-8" v-if="authStore.user">
    <div>
      <h2 class="text-3xl font-extrabold text-slate-800">Mi Perfil</h2>
      <p class="text-slate-500 mt-1">Gestiona tu información personal y credenciales de acceso.</p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Columna Izquierda: Info General -->
      <div class="space-y-6 lg:col-span-1">
        <div class="card bg-white shadow-xl border border-slate-100">
          <div class="card-body">
            <h3 class="card-title text-lg border-b border-slate-100 pb-2">Información de Cuenta</h3>
            
            <div class="mt-4">
              <p class="text-sm text-slate-500 font-medium">Email Registrado</p>
              <p class="font-bold text-slate-800">{{ authStore.user.email }}</p>
              <span class="badge badge-sm badge-ghost mt-1">No editable</span>
            </div>

            <!-- Nuevos campos traídos de api-invtzn -->
            <div v-if="invtznProfile" class="mt-4 space-y-4">
              <div>
                <p class="text-sm text-slate-500 font-medium">Rol en la Plataforma</p>
                <div class="badge badge-primary mt-1">{{ invtznProfile.custom_role }}</div>
              </div>
              <div>
                <p class="text-sm text-slate-500 font-medium">Tipo de Cliente</p>
                <p class="font-bold text-slate-800">{{ invtznProfile.customer_type }}</p>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 mt-4">
                <p class="text-sm text-slate-500 font-medium">Saldo en Billetera</p>
                <p class="text-2xl font-black text-green-600">${{ invtznProfile.current_balance }} <span class="text-xs text-slate-400 font-normal">MXN</span></p>
              </div>
            </div>
            <div v-else-if="loadingInvtzn" class="mt-6 flex justify-center">
              <span class="loading loading-spinner text-primary"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Columna Derecha: Formularios -->
      <div class="space-y-8 lg:col-span-2">
        
        <!-- Formulario Datos Personales -->
        <div class="card bg-white shadow-xl border border-slate-100">
          <div class="card-body">
            <h3 class="card-title text-lg border-b border-slate-100 pb-2">Editar Datos Personales</h3>
            <form @submit.prevent="handleUpdateProfile" class="space-y-4 mt-4">
              <div class="form-control w-full">
                <label class="label"><span class="label-text font-medium">Usuario</span></label>
                <input v-model="editForm.username" type="text" class="input input-bordered w-full" required :disabled="loadingProfile" />
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-medium">Nombre</span></label>
                  <input v-model="editForm.first_name" type="text" class="input input-bordered w-full" :disabled="loadingProfile" />
                </div>
                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-medium">Apellidos</span></label>
                  <input v-model="editForm.last_name" type="text" class="input input-bordered w-full" :disabled="loadingProfile" />
                </div>
              </div>
              
              <div class="form-control w-full">
                <label class="label"><span class="label-text font-medium">Teléfono (WhatsApp)</span></label>
                <input v-model="editForm.phone_number" type="text" class="input input-bordered w-full" :disabled="loadingProfile" />
              </div>
              
              <div class="card-actions justify-end mt-6">
                <button type="submit" class="btn btn-primary" :disabled="loadingProfile">
                  <span v-if="loadingProfile" class="loading loading-spinner loading-sm"></span>
                  {{ loadingProfile ? 'Guardando...' : 'Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Formulario Cambiar Contraseña -->
        <div class="card bg-white shadow-xl border border-slate-100">
          <div class="card-body">
            <h3 class="card-title text-lg border-b border-slate-100 pb-2 text-error">Seguridad</h3>
            <form @submit.prevent="handleChangePassword" class="space-y-4 mt-4">
              <div class="form-control w-full">
                <label class="label"><span class="label-text font-medium">Contraseña Actual</span></label>
                <input v-model="pwForm.old_password" type="password" class="input input-bordered w-full" required :disabled="loadingPassword" />
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-medium">Nueva Contraseña</span></label>
                  <input v-model="pwForm.new_password1" type="password" class="input input-bordered w-full" required :disabled="loadingPassword" />
                </div>
                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-medium">Confirmar Nueva Contraseña</span></label>
                  <input v-model="pwForm.new_password2" type="password" class="input input-bordered w-full" required :disabled="loadingPassword" />
                </div>
              </div>
              
              <div class="card-actions justify-end mt-6">
                <button type="submit" class="btn btn-error btn-outline" :disabled="loadingPassword">
                  <span v-if="loadingPassword" class="loading loading-spinner loading-sm"></span>
                  {{ loadingPassword ? 'Actualizando...' : 'Cambiar Contraseña' }}
                </button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
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