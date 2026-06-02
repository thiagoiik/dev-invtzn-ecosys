<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Moderación de Reseñas</h2>
        <p class="text-slate-500">Administra las opiniones de los clientes para alimentar la prueba social del Home.</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else-if="reviews.length === 0" class="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 text-center">
      <span class="text-5xl mb-4 block">💬</span>
      <h3 class="text-xl font-bold text-slate-800">Sin Reseñas</h3>
      <p class="text-slate-500 mt-2">Aún no se han registrado opiniones de los clientes.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="review in reviews" :key="review.id" class="card bg-white border border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
        <div class="card-body gap-4">
          <div class="flex justify-between items-start">
            <div class="flex text-amber-400 text-lg">
              <span v-for="star in 5" :key="star">{{ star <= review.rating ? '★' : '☆' }}</span>
            </div>
            <div :class="['badge', review.is_approved ? 'badge-success text-white' : 'badge-warning text-white']">
              {{ review.is_approved ? 'Aprobada' : 'Pendiente' }}
            </div>
          </div>
          <div>
            <h3 class="font-bold text-slate-800 text-lg">{{ review.reviewer_name }}</h3>
            <p class="text-xs text-slate-400 mt-0.5">{{ review.user_email || 'Cliente' }}</p>
          </div>
          <p class="text-slate-600 text-sm italic leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100 flex-grow">
            "{{ review.comment }}"
          </p>
          <p class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Fecha: {{ formatDate(review.created_at) }}</p>
          <div class="divider my-1"></div>
          <div class="card-actions justify-between items-center">
            <button 
              @click="toggleApprove(review)" 
              :class="['btn btn-sm rounded-xl font-bold', review.is_approved ? 'btn-outline btn-warning' : 'btn-success text-white']"
              :disabled="actionLoading === review.id"
            >
              <span v-if="actionLoading === review.id" class="loading loading-spinner loading-xs mr-1"></span>
              {{ review.is_approved ? 'Ocultar' : 'Aprobar' }}
            </button>
            <button 
              @click="confirmDelete(review)" 
              class="btn btn-error btn-sm btn-outline rounded-xl font-bold"
              :disabled="actionLoading === review.id"
            >
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div :class="['modal', { 'modal-open': !!reviewToDelete }]">
      <div class="modal-box max-w-sm rounded-2xl text-center space-y-4">
        <span class="text-4xl block">⚠️</span>
        <h3 class="font-bold text-lg text-slate-800">¿Eliminar Reseña?</h3>
        <p class="text-slate-500 text-sm">Esta acción es irreversible y eliminará permanentemente el testimonio de {{ reviewToDelete?.reviewer_name }}.</p>
        <div class="modal-action justify-center gap-4">
          <button class="btn btn-ghost rounded-xl" @click="reviewToDelete = null">Cancelar</button>
          <button class="btn btn-error rounded-xl text-white" @click="deleteReview">Confirmar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { reviewsService } from '@/modules/workspace/services/reviewsService';
import { useToast } from 'vue-toastification';

const toast = useToast();
const reviews = ref([]);
const loading = ref(true);
const actionLoading = ref(null);
const reviewToDelete = ref(null);

const fetchReviews = async () => {
  loading.value = true;
  try {
    const res = await reviewsService.fetchAllReviews();
    reviews.value = res.data;
  } catch (e) {
    toast.error('Error al cargar las reseñas.');
  } finally {
    loading.value = false;
  }
};

const toggleApprove = async (review) => {
  actionLoading.value = review.id;
  try {
    const res = await reviewsService.toggleApprove(review.id);
    review.is_approved = res.data.is_approved;
    toast.success(review.is_approved ? 'Reseña aprobada para mostrar en el Home' : 'Reseña oculta de la vista pública');
  } catch (e) {
    toast.error('No se pudo actualizar el estado de la reseña.');
  } finally {
    actionLoading.value = null;
  }
};

const confirmDelete = (review) => {
  reviewToDelete.value = review;
};

const deleteReview = async () => {
  if (!reviewToDelete.value) return;
  const targetId = reviewToDelete.value.id;
  reviewToDelete.value = null;
  actionLoading.value = targetId;
  try {
    await reviewsService.deleteReview(targetId);
    reviews.value = reviews.value.filter(r => r.id !== targetId);
    toast.success('Reseña eliminada correctamente.');
  } catch (e) {
    toast.error('Error al eliminar la reseña.');
  } finally {
    actionLoading.value = null;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

onMounted(() => {
  fetchReviews();
});
</script>
