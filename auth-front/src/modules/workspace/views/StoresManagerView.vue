<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Gestión de Sucursales</h2>
        <p class="text-slate-500">Administra las tiendas físicas y puntos de venta.</p>
      </div>
      <div class="flex gap-2">
        <button class="btn btn-outline btn-sm" @click="testStripe">
          Test Stripe API
        </button>
        <button class="btn btn-primary" @click="showAddModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Nueva Tienda
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="store in stores" :key="store.id" class="card bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all">
        <div class="card-body">
          <div class="flex justify-between items-start">
            <div class="bg-slate-100 p-3 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div :class="['badge', store.is_active ? 'badge-success' : 'badge-ghost']">
              {{ store.is_active ? 'Activa' : 'Inactiva' }}
            </div>
          </div>
          <h3 class="text-xl font-bold text-slate-800 mt-4">{{ store.name }}</h3>
          <p class="text-slate-500 text-sm flex items-center gap-2 mt-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ store.address }}, {{ store.city }}
          </p>
          <div class="divider"></div>
          <div class="card-actions justify-end">
            <button class="btn btn-outline btn-primary btn-sm" @click="viewStaff(store)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a7 7 0 00-7 7v1h11v-1a7 7 0 00-7-7z" />
              </svg>
              Staff
            </button>
            <button 
              v-if="!store.stripe_onboarding_completed"
              class="btn btn-outline btn-info btn-sm" 
              @click="setupStripe(store)"
              :disabled="loading"
            >
              Configurar Stripe
            </button>
            <div v-else class="badge badge-info gap-2 py-3 px-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              Stripe OK
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Personal de la Tienda -->
    <div :class="['modal', { 'modal-open': !!selectedStoreForStaff }]">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Personal en {{ selectedStoreForStaff?.name }}</h3>
        <div class="py-4">
          <div v-if="loadingStaff" class="flex justify-center py-4">
            <span class="loading loading-spinner"></span>
          </div>
          <div v-else-if="filteredStaff.length === 0" class="text-center py-6">
            <p class="text-slate-400 italic text-sm">No hay personal asignado a esta sucursal.</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="member in filteredStaff" :key="member.remote_auth_id" class="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
              <div class="flex items-center gap-3">
                <div class="bg-primary/10 text-primary font-bold w-10 h-10 rounded-full flex items-center justify-center">
                  {{ member.full_name?.charAt(0) || '?' }}
                </div>
                <div>
                  <p class="font-bold text-slate-800 text-sm">{{ member.full_name }}</p>
                  <p class="text-[10px] uppercase font-black text-slate-400">{{ member.custom_role }} | {{ member.vendor_mode }}</p>
                </div>
              </div>
              <div class="badge badge-outline badge-xs">{{ member.customer_type }}</div>
            </div>
          </div>
        </div>
        <div class="modal-action">
          <button class="btn btn-primary" @click="selectedStoreForStaff = null">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- Modal Nueva Tienda -->
    <div :class="['modal', { 'modal-open': showAddModal }]">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Registrar Nueva Sucursal</h3>
        <div class="py-4 space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Nombre de la Tienda</span></label>
            <input v-model="newStore.name" type="text" placeholder="Ej: Sucursal Centro" class="input input-bordered" />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Dirección</span></label>
            <input v-model="newStore.address" type="text" placeholder="Calle Falsa 123" class="input input-bordered" />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Ciudad</span></label>
            <input v-model="newStore.city" type="text" placeholder="Ciudad de México" class="input input-bordered" />
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-bold">Dueño / Franquiciatario</span></label>
            <select v-model="newStore.owner" class="select select-bordered">
              <option :value="null">Sin asignar (Super Admin)</option>
              <option v-for="f in franchisees" :key="f.remote_auth_id" :value="f.id">
                {{ f.full_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-action">
          <button class="btn btn-ghost" @click="showAddModal = false">Cancelar</button>
          <button class="btn btn-primary" @click="saveStore" :disabled="loading">
            <span v-if="loading" class="loading loading-spinner"></span>
            Crear Sucursal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { crmService } from '@/modules/workspace/services/crmService';
import { useToast } from 'vue-toastification';

const toast = useToast();
const stores = ref([]);
const showAddModal = ref(false);
const loading = ref(false);

const franchisees = ref([]);
const newStore = ref({
  name: '',
  address: '',
  city: '',
  owner: null
});

// Lógica de Personal
const selectedStoreForStaff = ref(null);
const allProfiles = ref([]);
const filteredStaff = ref([]);
const loadingStaff = ref(false);

const fetchStores = async () => {
  try {
    const res = await crmService.fetchAllStores();
    stores.value = res.data;
  } catch (e) {
    toast.error('Error al cargar tiendas');
  }
};

const viewStaff = async (store) => {
  selectedStoreForStaff.value = store;
  loadingStaff.value = true;
  try {
    // Obtenemos todos los perfiles y filtramos por esta tienda
    const res = await crmService.fetchAllProfiles();
    filteredStaff.value = res.data.filter(p => p.assigned_store === store.id);
  } catch (e) {
    toast.error('Error al cargar el personal');
  } finally {
    loadingStaff.value = false;
  }
};

const testStripe = async () => {
  try {
    const res = await crmService.debugStripe();
    alert(`Conexión exitosa: ${JSON.stringify(res.data, null, 2)}`);
  } catch (e) {
    alert(`Error de conexión: ${e.response?.data?.error || e.message}`);
  }
};

const saveStore = async () => {
  if (!newStore.value.name) return;
  loading.value = true;
  try {
    await crmService.createStore(newStore.value);
    toast.success('Tienda creada exitosamente');
    showAddModal.value = false;
    newStore.value = { name: '', address: '', city: '', owner: null };
    fetchStores();
  } catch (e) {
    toast.error('Error al crear la tienda');
  } finally {
    loading.value = false;
  }
};

const setupStripe = async (store) => {
  loading.value = true;
  try {
    const res = await crmService.getStripeOnboardingLink(store.id, window.location.href);
    window.location.href = res.data.url;
  } catch (e) {
    toast.error('Error al generar enlace de Stripe');
  } finally {
    loading.value = false;
  }
};

const verifyStripeStatus = async (store) => {
  try {
    const res = await crmService.verifyStripeOnboarding(store.id);
    if (res.data.stripe_onboarding_completed && !store.stripe_onboarding_completed) {
      store.stripe_onboarding_completed = true;
    }
  } catch (e) {
    console.error('Error verificando Stripe', e);
  }
};

const fetchFranchisees = async () => {
  try {
    const res = await crmService.fetchAllProfiles();
    franchisees.value = res.data.filter(p => p.custom_role === 'FRANCHISEE');
  } catch (e) {
    console.error('Error al cargar franquiciatarios', e);
  }
};

onMounted(async () => {
  await fetchStores();
  await fetchFranchisees();
  // Verificar estado de stripe para todas las tiendas que tengan ID pero no estén completadas
  stores.value.forEach(s => {
    if (s.stripe_account_id && !s.stripe_onboarding_completed) {
      verifyStripeStatus(s);
    }
  });
});
</script>
