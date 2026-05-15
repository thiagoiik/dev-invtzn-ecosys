<template>
  <div class="py-24 px-4 min-h-[60vh] flex items-center justify-center" :style="{ backgroundColor: config.bgColor || '#f8fafc' }">
    <div class="card w-full max-w-md bg-base-100 shadow-xl">
      <div class="card-body items-center text-center">
        <h2 class="card-title text-3xl font-bold text-slate-800 mb-2">Confirma tu Asistencia</h2>
        <p class="text-slate-500 mb-6">Nos encantaría contar con tu presencia.</p>
        
        <div v-if="successMsg" class="alert alert-success shadow-sm mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{{ successMsg }}</span>
        </div>

        <form v-else @submit.prevent="submitRSVP" class="w-full flex flex-col gap-4">
          <div class="form-control w-full">
            <input 
              v-model="form.full_name" 
              type="text" 
              placeholder="Nombre completo" 
              class="input input-bordered w-full" 
              required 
            />
          </div>
          
          <div class="form-control w-full">
            <select v-model="form.attending" class="select select-bordered w-full" required>
              <option value="" disabled selected>¿Asistirás?</option>
              <option value="yes">¡Sí, ahí estaré!</option>
              <option value="no">Lo siento, no podré asistir</option>
            </select>
          </div>
          
          <div class="card-actions w-full mt-4">
            <button 
              type="submit" 
              class="btn w-full text-white border-none shadow-md"
              :class="{ 'loading': loading }"
              :style="{ backgroundColor: config.btnColor || '#3b82f6' }"
              :disabled="loading"
            >
              {{ loading ? 'Enviando...' : 'Enviar Confirmación' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import { engineService } from '@/modules/engine/services/engineService';
import { useToast } from 'vue-toastification';

const props = defineProps({
  slug: {
    type: String,
    required: true
  },
  config: {
    type: Object,
    default: () => ({})
  }
});

const toast = useToast();
const loading = ref(false);
const successMsg = ref('');
const form = ref({
  full_name: '',
  attending: ''
});

const submitRSVP = async () => {
  if (!form.value.full_name || !form.value.attending) {
    return toast.warning('Por favor completa todos los campos.');
  }

  loading.value = true;
  try {
    await engineService.submitRSVP(props.slug, {
      full_name: form.value.full_name,
      attending: form.value.attending === 'yes'
    });
    
    successMsg.value = form.value.attending === 'yes' 
      ? '¡Genial! Hemos registrado tu asistencia.' 
      : 'Entendido. Lamentamos que no puedas venir.';
      
  } catch (error) {
    toast.error('Hubo un error al enviar tu respuesta. Intenta de nuevo.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Tailwind maneja los estilos */
</style>
