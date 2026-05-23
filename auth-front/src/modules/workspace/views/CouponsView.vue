<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold text-white tracking-tight">Gestión de Cupones</h1>
      <div class="flex gap-2">
        <button @click="showCreateModal = true" class="btn btn-primary shadow-lg shadow-primary/20">
          <i class="fas fa-plus mr-2"></i> Nuevo Cupón
        </button>
      </div>
    </div>

    <!-- Lista de Cupones -->
    <div class="card bg-slate-800/50 border border-slate-700">
      <div class="card-body">
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr class="text-slate-400 border-b border-slate-700">
                <th>Código</th>
                <th>Descuento</th>
                <th>Usos</th>
                <th>Vigencia</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="coupon in coupons" :key="coupon.id" class="border-b border-slate-700 hover:bg-slate-800/80 transition-colors">
                <td class="font-mono text-indigo-400 font-bold">{{ coupon.code }}</td>
                <td class="text-slate-300">
                  <span v-if="coupon.discount_percentage">{{ coupon.discount_percentage }}%</span>
                  <span v-else-if="coupon.discount_fixed">${{ coupon.discount_fixed }} MXN</span>
                  <span v-else>Envío Gratis</span>
                </td>
                <td class="text-slate-400">
                  {{ coupon.current_uses }} / {{ coupon.max_uses || '∞' }}
                </td>
                <td class="text-slate-400 text-sm">
                  <div v-if="coupon.valid_from">Desde: {{ new Date(coupon.valid_from).toLocaleDateString() }}</div>
                  <div v-if="coupon.valid_to">Hasta: {{ new Date(coupon.valid_to).toLocaleDateString() }}</div>
                  <div v-if="!coupon.valid_from && !coupon.valid_to">Sin Límite</div>
                </td>
                <td>
                  <span class="badge" :class="coupon.active ? 'badge-success' : 'badge-error'">
                    {{ coupon.active ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td>
                  <button @click="toggleStatus(coupon)" class="btn btn-sm btn-ghost" :class="coupon.active ? 'text-red-400' : 'text-green-400'">
                    {{ coupon.active ? 'Desactivar' : 'Activar' }}
                  </button>
                </td>
              </tr>
              <tr v-if="coupons.length === 0">
                <td colspan="6" class="text-center text-slate-500 py-8">No hay cupones creados.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Crear Cupón -->
    <dialog :class="{ 'modal-open': showCreateModal }" class="modal">
      <div class="modal-box bg-slate-800 border border-slate-700 w-11/12 max-w-2xl">
        <h3 class="font-bold text-lg text-white mb-4">Crear Nuevo Cupón</h3>
        <form @submit.prevent="createCoupon" class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text text-slate-300">Código Promocional</span></label>
            <input v-model="form.code" type="text" class="input input-bordered bg-slate-900 border-slate-700 text-white uppercase" placeholder="EJ: BLACKFRIDAY2026" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text text-slate-300">Descuento (%)</span></label>
              <input v-model.number="form.discount_percentage" type="number" min="0" max="100" class="input input-bordered bg-slate-900 border-slate-700 text-white" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text text-slate-300">Descuento Fijo ($)</span></label>
              <input v-model.number="form.discount_fixed" type="number" min="0" class="input input-bordered bg-slate-900 border-slate-700 text-white" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text text-slate-300">Límite de Usos (Opcional)</span></label>
              <input v-model.number="form.max_uses" type="number" min="1" class="input input-bordered bg-slate-900 border-slate-700 text-white" placeholder="Ej: 100" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text text-slate-300">Válido Desde (Opcional)</span></label>
              <input v-model="form.valid_from" type="datetime-local" class="input input-bordered bg-slate-900 border-slate-700 text-slate-300" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text text-slate-300">Válido Hasta (Opcional)</span></label>
              <input v-model="form.valid_to" type="datetime-local" class="input input-bordered bg-slate-900 border-slate-700 text-slate-300" />
            </div>
          </div>

          <div class="modal-action">
            <button type="button" @click="showCreateModal = false" class="btn btn-outline text-slate-300 border-slate-600">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
              Crear Cupón
            </button>
          </div>
        </form>
      </div>
      <div class="modal-backdrop" @click="showCreateModal = false"></div>
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
    const res = await invtznClient.get('sales/coupons/');
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

    await invtznClient.post('sales/coupons/', payload);
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
    await invtznClient.patch(`sales/coupons/${coupon.id}/`, { active: !coupon.active });
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
