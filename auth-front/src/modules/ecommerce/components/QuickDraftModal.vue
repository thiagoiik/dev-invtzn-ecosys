<template>
  <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center px-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm animate-fade-in" @click="close"></div>

    <!-- Modal Content -->
    <div class="relative bg-white w-full max-w-lg rounded-[2.5rem] shadow-2xl overflow-hidden animate-scale-up">
      <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-primary to-indigo-500"></div>
      
      <div class="p-10">
        <header class="text-center space-y-2 mb-8">
          <div class="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center text-3xl mx-auto shadow-sm">
            ✨
          </div>
          <h3 class="text-2xl font-black text-slate-900">Tu diseño, tus datos</h3>
          <p class="text-slate-400 font-medium">Personaliza esta prueba en segundos.</p>
        </header>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div class="form-control">
            <label class="label"><span class="label-text font-black text-slate-500 uppercase tracking-widest text-[10px]">Nombres de los festejados</span></label>
            <input 
              v-model="formData.names" 
              type="text" 
              placeholder="Ej: Ana & Luis" 
              class="input input-bordered w-full h-14 rounded-2xl focus:border-primary text-lg font-bold"
              required
            />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-black text-slate-500 uppercase tracking-widest text-[10px]">Fecha del Evento</span></label>
            <input 
              v-model="formData.date" 
              type="date" 
              class="input input-bordered w-full h-14 rounded-2xl focus:border-primary text-lg font-bold"
              required
            />
          </div>

          <div class="pt-4">
            <button 
              type="submit" 
              class="btn btn-primary w-full h-16 rounded-2xl text-lg font-black shadow-lg shadow-primary/20"
              :disabled="loading"
            >
              <span v-if="loading" class="loading loading-spinner"></span>
              {{ loading ? 'Creando Magia...' : '✨ Ver mi Invitación' }}
            </button>
            <button 
              type="button" 
              @click="close" 
              class="btn btn-ghost w-full mt-2 text-slate-400 font-bold uppercase tracking-widest text-[10px]"
              :disabled="loading"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits } from 'vue';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { useToast } from 'vue-toastification';

const props = defineProps({
  isOpen: Boolean,
  productId: Number
});

const emit = defineEmits(['close', 'success']);
const toast = useToast();
const loading = ref(false);

const formData = reactive({
  names: '',
  date: ''
});

const close = () => {
  if (!loading.value) emit('close');
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    // Estructura de datos personalizada para el motor de renderizado
    const customData = {
      cover: {
        names: formData.names,
        date: formData.date
      },
      rsvp: {
        event_date: formData.date
      }
    };

    const res = await deploymentService.createSandbox(props.productId, customData);
    toast.success('¡Tu invitación está lista!');
    emit('success', res.data);
  } catch (error) {
    console.error(error);
    toast.error('No pudimos crear tu prueba. Intenta más tarde.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
.animate-scale-up { animation: scaleUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
