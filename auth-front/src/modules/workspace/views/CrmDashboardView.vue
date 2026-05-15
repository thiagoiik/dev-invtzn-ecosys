<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Centro de Control de Usuarios</h2>
        <p class="text-slate-500">Gestión centralizada de perfiles, roles y finanzas del ecosistema.</p>
      </div>
      <div class="flex gap-2">
        <div class="stats bg-slate-100/50 border border-slate-200 shadow-none px-4 py-1">
          <div class="stat p-0">
            <div class="stat-title text-[10px] font-black uppercase text-slate-400">Total Usuarios</div>
            <div class="stat-value text-xl text-slate-800">{{ crmStore.profiles.length }}</div>
          </div>
        </div>
      </div>
    </div>

    <UserSearchGrid 
      :profiles="crmStore.profiles" 
      @select="crmStore.selectProfile" 
    />

    <CustomerSideDrawer 
      :isOpen="crmStore.drawerOpen" 
      :profile="crmStore.selectedProfile" 
      @close="crmStore.closeDrawer"
      @refresh="crmStore.fetchProfiles"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCrmStore } from '../store/crmStore';
import UserSearchGrid from '../components/UserSearchGrid.vue';
import CustomerSideDrawer from '../components/CustomerSideDrawer.vue';

const crmStore = useCrmStore();

onMounted(() => {
  crmStore.fetchProfiles();
});
</script>
