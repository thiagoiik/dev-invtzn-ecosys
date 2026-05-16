<template>
  <div :class="['fixed inset-y-0 right-0 w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out border-l border-slate-200 flex flex-col', isOpen ? 'translate-x-0' : 'translate-x-full']">
    <!-- Header -->
    <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
      <div>
        <h3 class="font-black text-slate-800 text-lg uppercase tracking-tight">Ficha de Cliente</h3>
        <p class="text-xs text-slate-400 font-bold uppercase">ID #{{ profile?.remote_auth_id }}</p>
      </div>
      <button @click="$emit('close')" class="btn btn-circle btn-ghost btn-sm">✕</button>
    </div>

    <!-- Content -->
    <div v-if="profile" class="flex-1 overflow-y-auto p-6 space-y-8">
      <!-- Info Básica -->
      <div class="text-center">
        <div class="avatar placeholder mb-4">
          <div class="bg-primary text-primary-content rounded-full w-20 shadow-lg">
            <span class="text-2xl font-black">{{ profile.full_name?.charAt(0) }}</span>
          </div>
        </div>
        <h4 class="text-xl font-bold text-slate-800">{{ profile.full_name || 'Sin Nombre' }}</h4>
        <p class="text-sm text-slate-500 font-medium">{{ profile.phone_number || 'Sin teléfono registrado' }}</p>
      </div>

      <div class="divider"></div>

      <!-- Gestión de Rol (Solo Admin y Franquiciatario pueden cambiar roles) -->
      <RoleSelector 
        v-if="['ADMIN', 'FRANCHISEE'].includes(currentUserRole)"
        v-model="profile.custom_role" 
        :loading="updatingRole" 
        @update:modelValue="handleRoleChange"
      />
      <div v-else class="p-4 bg-slate-50 rounded-xl border border-slate-100">
        <p class="text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Rol Actual</p>
        <p class="font-bold text-slate-700">{{ profile.custom_role }}</p>
      </div>

      <!-- Asignación de Sucursal (Para Vendedores y Gerentes) -->
      <div v-if="['VENDOR', 'MANAGER'].includes(profile.custom_role)" class="form-control w-full mt-4">
        <label class="label">
          <span class="label-text font-bold text-xs uppercase text-slate-500">Sucursal Asignada</span>
        </label>
        <select 
          v-model="profile.assigned_store" 
          class="select select-bordered w-full font-medium"
          @change="handleUpdateProfile"
        >
          <option :value="null">Ninguna / Central</option>
          <option v-for="store in crmStore.stores" :key="store.id" :value="store.id">
            {{ store.name }}
          </option>
        </select>
      </div>

      <!-- Gestión de Billetera -->
      <WalletManager 
        :profile-id="profile.remote_auth_id" 
        :current-balance="profile.current_balance"
        @updated="$emit('refresh')"
      />

      <!-- Notas Internas -->
      <div class="form-control">
        <label class="label">
          <span class="label-text font-bold text-xs uppercase text-slate-500">Notas Administrativas</span>
        </label>
        <textarea 
          v-model="profile.internal_notes" 
          class="textarea textarea-bordered h-24 text-sm font-medium" 
          placeholder="Añadir notas privadas sobre este cliente..."
          @blur="handleUpdateProfile"
        ></textarea>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-6 border-t border-slate-100 bg-slate-50">
      <button class="btn btn-outline btn-block" @click="$emit('close')">Cerrar Ficha</button>
    </div>
  </div>

  <!-- Backdrop -->
  <div v-if="isOpen" @click="$emit('close')" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import RoleSelector from './RoleSelector.vue';
import WalletManager from './WalletManager.vue';
import { crmService } from '@/modules/workspace/services/crmService';
import { useCrmStore } from '../store/crmStore';
import { useToast } from 'vue-toastification';
import { profileService } from '@/modules/dashboard/services/profileService';

const props = defineProps(['isOpen', 'profile']);
const emit = defineEmits(['close', 'refresh']);
const toast = useToast();
const crmStore = useCrmStore();

const updatingRole = ref(false);
const currentUserRole = ref(null);

onMounted(async () => {
  try {
    const res = await profileService.fetchMyProfile();
    currentUserRole.value = res.data.custom_role;
  } catch (e) {
    console.error("Error fetching current user role", e);
  }
});

const handleRoleChange = async (newRole) => {
  updatingRole.value = true;
  try {
    await crmService.updateProfileRole(props.profile.remote_auth_id, newRole);
    toast.success('Rol actualizado con éxito');
    emit('refresh');
  } catch (e) {
    toast.error('Error al actualizar rol');
  } finally {
    updatingRole.value = false;
  }
};

const handleUpdateProfile = async () => {
  try {
    await crmService.updateProfileStore(props.profile.remote_auth_id, props.profile.assigned_store, props.profile.vendor_mode);
    // Nota: El método updateProfileStore actualiza el perfil completo en el backend si el serializador lo permite
    // En este caso, estamos enviando notas, tienda y modo.
    // Vamos a añadir un método genérico a crmService para evitar confusión.
    await crmService.updateProfileGeneral(props.profile.remote_auth_id, {
      internal_notes: props.profile.internal_notes
    });
    toast.info('Notas guardadas');
  } catch (e) {
    toast.error('Error al guardar notas');
  }
};
</script>
