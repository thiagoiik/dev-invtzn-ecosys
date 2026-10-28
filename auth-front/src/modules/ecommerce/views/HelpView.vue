<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 font-sans">
    <div class="max-w-4xl mx-auto space-y-12">
      <!-- Header -->
      <header class="text-center space-y-4 max-w-2xl mx-auto">
        <span class="text-xs font-black text-primary uppercase tracking-[0.3em]">Centro de Ayuda</span>
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-none">
          ¿Cómo podemos ayudarte hoy?
        </h1>
        <p class="text-slate-500 leading-relaxed text-sm">
          Preguntas frecuentes y soporte directo de Invitazyon para que tu evento sea perfecto.
        </p>
      </header>

      <!-- FAQ Accordion section -->
      <section class="bg-white rounded-[2.5rem] p-8 md:p-12 shadow-sm border border-slate-100 space-y-6">
        <h2 class="text-2xl font-black text-slate-800 border-b border-slate-50 pb-4 mb-4">Preguntas Frecuentes</h2>
        
        <div class="space-y-4">
          <!-- FAQ 1 -->
          <div class="collapse collapse-plus bg-slate-50 rounded-2xl border border-slate-100">
            <input type="radio" name="faq-accordion" checked="checked" /> 
            <div class="collapse-title text-base font-bold text-slate-800">
              ¿Qué es el modo borrador o Sandbox?
            </div>
            <div class="collapse-content text-slate-500 text-sm leading-relaxed">
              <p>Es un entorno gratuito de edición donde puedes personalizar tu invitación, probar música, configurar el contador y ver cómo se verá en teléfonos móviles antes de realizar un pago. El modo borrador incluye una marca de agua superior y el RSVP se realiza directo a tu WhatsApp.</p>
            </div>
          </div>

          <!-- FAQ 2 -->
          <div class="collapse collapse-plus bg-slate-50 rounded-2xl border border-slate-100">
            <input type="radio" name="faq-accordion" /> 
            <div class="collapse-title text-base font-bold text-slate-800">
              ¿Cómo activo mi invitación y quito la marca de agua?
            </div>
            <div class="collapse-content text-slate-500 text-sm leading-relaxed">
              <p>Dentro del editor (Studio) o en tu Dashboard, verás el botón "Publicar / Activar Pase". Al hacer clic, podrás realizar el pago de forma 100% segura mediante Stripe. Inmediatamente después del pago, tu invitación se publica en vivo en una URL pública de hosting dedicada, eliminando la marca de agua.</p>
            </div>
          </div>

          <!-- FAQ 3 -->
          <div class="collapse collapse-plus bg-slate-50 rounded-2xl border border-slate-100">
            <input type="radio" name="faq-accordion" /> 
            <div class="collapse-title text-base font-bold text-slate-800">
              ¿Cómo confirman asistencia mis invitados?
            </div>
            <div class="collapse-content text-slate-500 text-sm leading-relaxed">
              <p>Si tienes el plan Básico o Standard, tus invitados verán un formulario rápido en el que ingresan su nombre y, al confirmar, la invitación los redirige a tu WhatsApp con un mensaje pre-llenado. En el plan Premium, los invitados se registran en una base de datos centralizada que puedes consultar y descargar desde tu panel de control.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Contact Support Ticket Form -->
      <section class="bg-white rounded-[2.5rem] p-8 md:p-12 shadow-sm border border-slate-100 space-y-8">
        <div class="space-y-2">
          <h2 class="text-2xl font-black text-slate-800">Contactar a Soporte</h2>
          <p class="text-slate-400 text-sm font-medium">¿Tienes alguna duda técnica o comercial? Envíanos un mensaje.</p>
        </div>

        <form @submit.prevent="submitTicket" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-500 text-xs uppercase tracking-widest">Tu Nombre</span></label>
              <input v-model="ticket.name" type="text" placeholder="Ej. Ana Pérez" class="input input-bordered w-full h-12 rounded-xl focus:border-primary text-slate-800 font-medium" required />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-500 text-xs uppercase tracking-widest">Tu Email</span></label>
              <input v-model="ticket.email" type="email" placeholder="Ej. ana@gmail.com" class="input input-bordered w-full h-12 rounded-xl focus:border-primary text-slate-800 font-medium" required />
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-500 text-xs uppercase tracking-widest">Asunto</span></label>
            <input v-model="ticket.subject" type="text" placeholder="Ej. Duda sobre música de fondo" class="input input-bordered w-full h-12 rounded-xl focus:border-primary text-slate-800 font-medium" required />
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-500 text-xs uppercase tracking-widest">Mensaje</span></label>
            <textarea v-model="ticket.message" placeholder="Escribe tu mensaje en detalle..." class="textarea textarea-bordered w-full h-32 rounded-xl focus:border-primary text-slate-800 font-medium" required></textarea>
          </div>

          <button type="submit" class="btn btn-primary h-14 rounded-2xl w-full md:w-auto md:px-10 font-black shadow-lg shadow-primary/20" :disabled="submitting">
            <span v-if="submitting" class="loading loading-spinner"></span>
            Enviar Mensaje
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useToast } from 'vue-toastification';

const toast = useToast();
const submitting = ref(false);

const ticket = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
});

onMounted(() => {
  window.scrollTo(0, 0);
});

const submitTicket = () => {
  submitting.value = true;
  setTimeout(() => {
    toast.success('¡Mensaje enviado con éxito! Nos pondremos en contacto contigo en breve.');
    ticket.name = '';
    ticket.email = '';
    ticket.subject = '';
    ticket.message = '';
    submitting.value = false;
  }, 1000);
};
</script>

<style scoped>
/* Standard styling variables */
</style>
