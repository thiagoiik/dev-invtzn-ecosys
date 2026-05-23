<template>
  <div class="space-y-6">
    <!-- Header Card -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Gestión de Cupones</h2>
        <p class="text-slate-500 text-sm">Crea y administra códigos promocionales para la tienda B2C.</p>
      </div>
      <div>
        <button @click="showCreateModal = true" class="btn btn-primary shadow-lg shadow-primary/20">
          ➕ Nuevo Cupón
        </button>
      </div>
    </div>

    <!-- Lista de Cupones -->
    <div class="card bg-white border border-slate-200 shadow-sm rounded-2xl">
      <div class="card-body p-6">
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr class="text-slate-500 border-b border-slate-200">
                <th class="font-bold text-slate-700">Código</th>
                <th class="font-bold text-slate-700">Descuento</th>
                <th class="font-bold text-slate-700">Usos</th>
                <th class="font-bold text-slate-700">Vigencia</th>
                <th class="font-bold text-slate-700">Estado</th>
                <th class="font-bold text-slate-700">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="coupon in coupons" :key="coupon.id" class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                <td class="font-mono text-primary font-bold text-sm">{{ coupon.code }}</td>
                <td class="text-slate-700 font-medium">
                  <span v-if="parseFloat(coupon.discount_percentage) > 0" class="bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md text-xs font-bold">{{ coupon.discount_percentage }}%</span>
                  <span v-else-if="parseFloat(coupon.discount_fixed) > 0" class="bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-md text-xs font-bold">${{ coupon.discount_fixed }} MXN</span>
                  <span v-else class="text-slate-400 italic text-xs">Sin descuento</span>
                </td>
                <td class="text-slate-600 text-sm">
                  <span class="font-semibold">{{ coupon.current_uses }}</span> <span class="text-slate-400">/</span> {{ coupon.max_uses || '∞' }}
                </td>
                <td class="text-slate-600 text-xs space-y-0.5">
                  <div v-if="coupon.valid_from"><span class="text-slate-400 font-medium">Desde:</span> {{ new Date(coupon.valid_from).toLocaleDateString() }}</div>
                  <div v-if="coupon.valid_to"><span class="text-slate-400 font-medium">Hasta:</span> {{ new Date(coupon.valid_to).toLocaleDateString() }}</div>
                  <div v-if="!coupon.valid_from && !coupon.valid_to" class="text-slate-400 italic">Sin límite temporal</div>
                </td>
                <td>
                  <span class="badge" :class="coupon.active ? 'badge-success text-white' : 'badge-ghost text-slate-500'">
                    {{ coupon.active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td>
                  <button @click="toggleStatus(coupon)" class="btn btn-sm btn-ghost text-xs" :class="coupon.active ? 'text-rose-600 hover:bg-rose-50' : 'text-emerald-600 hover:bg-emerald-50'">
                    {{ coupon.active ? 'Desactivar' : 'Activar' }}
                  </button>
                </td>
              </tr>
              <tr v-if="coupons.length === 0">
                <td colspan="6" class="text-center text-slate-400 py-12">
                  <div class="text-3xl mb-2">🎫</div>
                  No hay cupones creados aún.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Crear Cupón -->
    <dialog :class="{ 'modal-open': showCreateModal }" class="modal">
      <div class="modal-box bg-white border border-slate-200 rounded-2xl w-11/12 max-w-2xl shadow-2xl">
        <h3 class="font-bold text-xl text-slate-800 mb-4 flex items-center gap-2">
          <span>🎫</span> Crear Nuevo Cupón
        </h3>
        <form @submit.prevent="createCoupon" class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-700">Código Promocional</span></label>
            <input v-model="form.code" type="text" class="input input-bordered bg-white border-slate-300 text-slate-800 placeholder-slate-400 uppercase font-mono font-bold" placeholder="EJ: BODA2026" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-700">Descuento (%)</span></label>
              <input v-model.number="form.discount_percentage" type="number" min="0" max="100" class="input input-bordered bg-white border-slate-300 text-slate-800" placeholder="Ej: 15" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-700">Descuento Fijo ($)</span></label>
              <input v-model.number="form.discount_fixed" type="number" min="0" class="input input-bordered bg-white border-slate-300 text-slate-800" placeholder="Ej: 200" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-700">Límite de Usos (Opcional)</span></label>
              <input v-model.number="form.max_uses" type="number" min="1" class="input input-bordered bg-white border-slate-300 text-slate-800" placeholder="Ej: 100" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-700">Válido Desde (Opcional)</span></label>
              <input v-model="form.valid_from" type="datetime-local" class="input input-bordered bg-white border-slate-300 text-slate-700" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-700">Válido Hasta (Opcional)</span></label>
              <input v-model="form.valid_to" type="datetime-local" class="input input-bordered bg-white border-slate-300 text-slate-700" />
            </div>
          </div>

          <div class="modal-action border-t border-slate-100 pt-4 mt-6">
            <button type="button" @click="showCreateModal = false" class="btn btn-outline border-slate-300 text-slate-600 hover:bg-slate-50">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
              Crear Cupón
            </button>
          </div>
        </form>
      </div>
      <div class="modal-backdrop bg-slate-900/40 backdrop-blur-xs" @click="showCreateModal = false"></div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import invtznClient from '@/core/api/invtznClient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const coupons = ref([]);
const showCreateModal = ref(false);
const isLoading = ref(false);

const form = ref({
  code: '',
  discount_percentage: null,
  discount_fixed: null,
  max_uses: null,
  valid_from: '',
  valid_to: '',
  active: true
});

const fetchCoupons = async () => {
  try {
    const res = await invtznClient.get('coupons/');
    coupons.value = res.data.results || res.data;
  } catch (error) {
    toast.error('Error al cargar cupones');
  }
};

const createCoupon = async () => {
  isLoading.value = true;
  try {
    const payload = { ...form.value };
    if (!payload.valid_from) delete payload.valid_from;
    if (!payload.valid_to) delete payload.valid_to;
    if (!payload.discount_percentage) payload.discount_percentage = '0.00';
    if (!payload.discount_fixed) payload.discount_fixed = '0.00';

    await invtznClient.post('coupons/', payload);
    toast.success('Cupón creado exitosamente');
    showCreateModal.value = false;
    form.value = { code: '', discount_percentage: null, discount_fixed: null, max_uses: null, valid_from: '', valid_to: '', active: true };
    fetchCoupons();
  } catch (error) {
    toast.error(error.response?.data?.code?.[0] || 'Error al crear cupón');
  } finally {
    isLoading.value = false;
  }
};

const toggleStatus = async (coupon) => {
  try {
    await invtznClient.patch(`coupons/${coupon.id}/`, { active: !coupon.active });
    coupon.active = !coupon.active;
    toast.success('Estado actualizado');
  } catch (error) {
    toast.error('Error al actualizar');
  }
};

onMounted(() => {
  fetchCoupons();
});
</script>
