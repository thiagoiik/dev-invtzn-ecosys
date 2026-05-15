<template>
  <div class="space-y-4">
    <!-- Buscador -->
    <div class="relative group">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none transition-colors group-focus-within:text-primary text-slate-400">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <input 
        v-model="search" 
        type="text" 
        placeholder="Buscar por nombre, ID o teléfono..." 
        class="input input-bordered w-full pl-12 h-14 bg-white border-slate-200 shadow-sm focus:shadow-md transition-all font-medium text-slate-700"
      />
    </div>

    <!-- Grid / Tabla -->
    <div class="overflow-x-auto bg-white rounded-2xl shadow-sm border border-slate-200">
      <table class="table table-zebra w-full">
        <thead class="bg-slate-50">
          <tr>
            <th class="text-slate-500 uppercase text-[11px] font-black py-4 pl-6">Usuario</th>
            <th class="text-slate-500 uppercase text-[11px] font-black">Rol</th>
            <th class="text-slate-500 uppercase text-[11px] font-black text-right">Saldo</th>
            <th class="text-slate-500 uppercase text-[11px] font-black text-right pr-6">Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="profile in filteredProfiles" 
            :key="profile.remote_auth_id" 
            class="hover:bg-slate-50/80 cursor-pointer group transition-colors"
            @click="$emit('select', profile)"
          >
            <td class="pl-6">
              <div class="flex items-center gap-3">
                <div class="avatar placeholder">
                  <div class="bg-slate-100 text-slate-500 rounded-lg w-10 h-10 border border-slate-200 font-bold group-hover:bg-primary/10 group-hover:text-primary transition-colors">
                    {{ profile.full_name?.charAt(0) || '?' }}
                  </div>
                </div>
                <div>
                  <div class="font-bold text-slate-800">{{ profile.full_name || 'Desconocido' }}</div>
                  <div class="text-xs text-slate-400 font-medium">ID #{{ profile.remote_auth_id }}</div>
                </div>
              </div>
            </td>
            <td>
              <span :class="['badge font-black text-[10px] uppercase tracking-widest px-2', getBadgeClass(profile.custom_role)]">
                {{ profile.custom_role }}
              </span>
            </td>
            <td class="text-right font-black text-slate-700">
              ${{ profile.current_balance }}
            </td>
            <td class="text-right pr-6">
              <button class="btn btn-ghost btn-xs text-primary font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                Ver Detalles →
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps(['profiles']);
defineEmits(['select']);

const search = ref('');

const filteredProfiles = computed(() => {
  if (!search.value) return props.profiles;
  const s = search.value.toLowerCase();
  return props.profiles.filter(p => 
    p.full_name?.toLowerCase().includes(s) || 
    p.remote_auth_id.toString().includes(s) ||
    p.phone_number?.includes(s)
  );
});

const getBadgeClass = (role) => {
  switch(role) {
    case 'ADMIN': return 'badge-warning';
    case 'VENDOR': return 'badge-success text-white';
    default: return 'badge-ghost';
  }
};
</script>
