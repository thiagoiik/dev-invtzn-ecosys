<template>
  <div 
    class="py-12 px-6 max-w-4xl mx-auto bg-white/40 backdrop-blur-md rounded-[2.5rem] border border-slate-100/50 shadow-xl my-6 flex items-center justify-center transition-all"
  >
    <!-- 1. Success Message Panel -->
    <RsvpSuccessMessage 
      v-if="submitted" 
      :attending="form.attending === 'yes'" 
      :fullName="form.full_name"
      :eventTitle="config.eventTitle"
      :eventDate="config.eventDate"
    />

    <!-- 2. Interactive Input Form -->
    <div 
      v-else
      class="w-full max-w-md p-2 space-y-8 animate-fade-in"
    >
      <header class="text-center space-y-2">
        <span class="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em]">Confirma tu presencia</span>
        <h2 class="text-3xl font-serif font-bold text-slate-900">
          {{ config.title || 'Confirma tu Asistencia' }}
        </h2>
        <p class="text-slate-400 font-medium text-sm">
          {{ config.subtitle || 'Nos encantaría contar con tu presencia.' }}
        </p>
      </header>

      <form @submit.prevent="handleFormSubmit" class="space-y-6">
        <!-- Full Name input -->
        <div class="space-y-2">
          <label class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">Tu Nombre Completo</label>
          <input 
            v-model="form.full_name" 
            type="text" 
            placeholder="Ej. Juan Pérez" 
            class="input input-bordered w-full h-14 rounded-2xl border-slate-200 focus:border-primary text-slate-800 font-medium focus:ring-2 focus:ring-primary/10 transition-all" 
            required 
          />
        </div>

        <!-- Big Dynamic Toggle Buttons for Attendance -->
        <div class="space-y-2">
          <label class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">¿Nos Acompañarás?</label>
          <div class="grid grid-cols-2 gap-4">
            <!-- Yes Option -->
            <button 
              type="button"
              @click="form.attending = 'yes'"
              class="h-16 rounded-2xl border-2 flex flex-col items-center justify-center font-bold transition-all duration-300 gap-1"
              :class="[
                form.attending === 'yes' 
                  ? 'border-primary bg-primary/5 text-primary scale-[1.03]' 
                  : 'border-slate-100 hover:border-slate-200 text-slate-400'
              ]"
            >
              <span class="text-lg">🥂</span>
              <span class="text-xs">¡Sí, asistiré!</span>
            </button>

            <!-- No Option -->
            <button 
              type="button"
              @click="form.attending = 'no'"
              class="h-16 rounded-2xl border-2 flex flex-col items-center justify-center font-bold transition-all duration-300 gap-1"
              :class="[
                form.attending === 'no' 
                  ? 'border-red-500 bg-red-50/50 text-red-500 scale-[1.03]' 
                  : 'border-slate-100 hover:border-slate-200 text-slate-400'
              ]"
            >
              <span class="text-lg">😔</span>
              <span class="text-xs">No podré</span>
            </button>
          </div>
        </div>

        <!-- Companions Selection (STANDARD & PREMIUM) -->
        <div v-if="['STANDARD', 'PREMIUM'].includes(resolvedTier) && form.attending === 'yes'" class="space-y-2 animate-fade-in">
          <label class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">Acompañantes Adicionales</label>
          <select 
            v-model.number="form.companions_count" 
            class="select select-bordered w-full h-14 rounded-2xl border-slate-200 focus:border-primary text-slate-800 font-medium focus:ring-2 focus:ring-primary/10 transition-all bg-white"
          >
            <option :value="0">Ninguno (Vengo solo)</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }} {{ n === 1 ? 'acompañante' : 'acompañantes' }}</option>
          </select>
        </div>

        <!-- Menu Selection (PREMIUM ONLY) -->
        <div v-if="resolvedTier === 'PREMIUM' && form.attending === 'yes'" class="space-y-2 animate-fade-in">
          <label class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">Selección de Menú</label>
          <select 
            v-model="form.menu_selection" 
            class="select select-bordered w-full h-14 rounded-2xl border-slate-200 focus:border-primary text-slate-800 font-medium focus:ring-2 focus:ring-primary/10 transition-all bg-white"
          >
            <option value="Menú Tradicional">Menú Tradicional 🥩</option>
            <option value="Menú Vegetariano">Menú Vegetariano 🥗</option>
            <option value="Menú Infantil">Menú Infantil 🍟</option>
          </select>
        </div>

        <!-- Dietary Notes (PREMIUM ONLY) -->
        <div v-if="resolvedTier === 'PREMIUM' && form.attending === 'yes'" class="space-y-2 animate-fade-in">
          <label class="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">Alergias o Restricciones</label>
          <textarea 
            v-model="form.dietary_notes" 
            placeholder="Ej: Alérgico a nueces, vegetariano, etc." 
            class="textarea textarea-bordered w-full h-24 rounded-2xl border-slate-200 focus:border-primary text-slate-800 font-medium focus:ring-2 focus:ring-primary/10 transition-all bg-white py-3"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          class="btn btn-primary btn-lg w-full h-16 rounded-2xl text-lg font-black shadow-lg shadow-primary/20 mt-4"
          :disabled="loading || !form.attending"
        >
          <span v-if="loading && resolvedTier !== 'BASIC'" class="loading loading-spinner"></span>
          {{ resolvedTier === 'BASIC' ? 'Confirmar por WhatsApp 🟢' : (loading ? 'Enviando...' : 'Confirmar Asistencia') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue';
import { engineService } from '@/modules/engine/services/engineService';
import { useTelemetry } from '../composables/useTelemetry';
import { useToast } from 'vue-toastification';
import RsvpSuccessMessage from './RsvpSuccessMessage.vue';

const props = defineProps({
  slug: { type: String, required: true },
  config: { type: Object, default: () => ({}) },
  tierLevel: { type: String, default: 'BASIC' }
});

const toast = useToast();
const telemetry = useTelemetry();

const resolvedTier = computed(() => props.config?.tier || props.tierLevel);

const loading = ref(false);
const submitted = ref(false);
const form = ref({
  full_name: '',
  attending: '',
  companions_count: 0,
  menu_selection: 'Menú Tradicional',
  dietary_notes: ''
});

const handleFormSubmit = () => {
  if (resolvedTier.value === 'BASIC') {
    sendWhatsAppRSVP();
  } else {
    submitRSVP();
  }
};

const sendWhatsAppRSVP = () => {
  if (!form.value.full_name || !form.value.attending) {
    return toast.warning('Por favor completa todos los campos.');
  }
  
  const rawPhone = props.config.whatsappPhone || '';
  const cleanPhone = rawPhone.replace(/\D/g, '');
  
  if (!cleanPhone) {
    toast.error('El organizador aún no ha configurado su número de WhatsApp de confirmación.');
    return;
  }

  const isAttending = form.value.attending === 'yes';
  const attendanceText = isAttending ? '¡Sí, asistiré!' : 'Lamentablemente no podré asistir.';
  
  const text = `¡Hola! Quiero confirmar mi asistencia a tu evento.\n\nNombre: ${form.value.full_name}\nAsistencia: ${attendanceText}`;
  
  // Track telemetry metric for basic RSVP button click
  telemetry.trackRsvpSubmit(props.slug).catch(() => {});
  
  // Open WhatsApp in a new tab
  window.open(`https://api.whatsapp.com/send?phone=${cleanPhone}&text=${encodeURIComponent(text)}`, '_blank');
  
  // Mark as submitted locally to show success view
  submitted.value = true;
};

const submitRSVP = async () => {
  if (!form.value.full_name || !form.value.attending) {
    return toast.warning('Por favor completa todos los campos.');
  }

  loading.value = true;
  try {
    const isAttending = form.value.attending === 'yes';
    
    const payload = {
      full_name: form.value.full_name,
      attending: isAttending
    };

    if (['STANDARD', 'PREMIUM'].includes(resolvedTier.value) && isAttending) {
      payload.companions_count = form.value.companions_count;
    }
    if (resolvedTier.value === 'PREMIUM' && isAttending) {
      payload.menu_selection = form.value.menu_selection;
      payload.dietary_notes = form.value.dietary_notes;
    }

    // 1. Submit to DB
    await engineService.submitRSVP(props.slug, payload);

    // 2. Track Telemetry silently
    await telemetry.trackRsvpSubmit(props.slug);

    submitted.value = true;
    toast.success('¡Respuesta enviada con éxito!');
  } catch (error) {
    console.error(error);
    toast.error('Hubo un error al enviar tu respuesta. Intenta de nuevo.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-serif {
  font-family: 'Playfair Display', serif;
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
