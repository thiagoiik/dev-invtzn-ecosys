<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 font-sans">
    <div class="max-w-6xl mx-auto space-y-12">
      <!-- Header -->
      <header class="text-center space-y-4 max-w-3xl mx-auto">
        <span class="text-xs font-black text-primary uppercase tracking-[0.3em]">Planes & Precios</span>
        <h1 class="text-4xl md:text-6xl font-black text-slate-900 tracking-tight leading-none">
          Elige el pase perfecto para tu evento
        </h1>
        <p class="text-lg text-slate-500 leading-relaxed">
          Comienza a diseñar tu invitación gratis en modo borrador y activa el pase cuando estés listo para publicarla.
        </p>
      </header>

      <!-- Grid de Tarjetas de Precios -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch pt-6">
        <!-- 1. Plan Básico -->
        <div class="bg-white rounded-[2.5rem] p-8 border border-slate-100 shadow-sm flex flex-col justify-between hover:shadow-lg transition-all duration-300 relative overflow-hidden">
          <div class="space-y-6">
            <header class="space-y-2">
              <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest">Prueba Gratuita</span>
              <h3 class="text-2xl font-black text-slate-800">Lienzo Básico</h3>
              <p class="text-slate-400 text-xs font-medium">Prueba y diseña sin prisas desde el editor.</p>
            </header>
            <div class="flex items-baseline gap-1">
              <span class="text-5xl font-black text-slate-900">$0</span>
              <span class="text-slate-400 text-sm font-bold uppercase">MXN</span>
            </div>
            <div class="w-full h-[1px] bg-slate-100"></div>
            <ul class="space-y-4 text-xs font-bold text-slate-500">
              <li class="flex items-center gap-2">✓ Portada Interactiva</li>
              <li class="flex items-center gap-2">✓ Edición ilimitada</li>
              <li class="flex items-center gap-2 text-primary font-black">✓ RSVP directo a tu WhatsApp</li>
              <li class="text-slate-300 flex items-center gap-2">✗ Sin Música de Fondo</li>
              <li class="text-slate-300 flex items-center gap-2">✗ Sin Cuenta Regresiva</li>
              <li class="text-slate-300 flex items-center gap-2">✗ Marca de agua en visualización</li>
            </ul>
          </div>
          <div class="pt-8">
            <button @click="handleAction('BASIC')" class="btn btn-outline border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300 w-full h-14 rounded-2xl font-bold">
              Comenzar Gratis
            </button>
          </div>
        </div>

        <!-- 2. Plan Standard (Destacado) -->
        <div class="bg-white rounded-[2.5rem] p-8 border-2 border-primary shadow-xl flex flex-col justify-between hover:shadow-2xl transition-all duration-300 relative overflow-hidden transform -translate-y-2">
          <div class="absolute top-0 right-0 bg-primary text-white text-[9px] font-black tracking-widest uppercase px-5 py-2 rounded-bl-2xl">
            Popular
          </div>
          <div class="space-y-6">
            <header class="space-y-2">
              <span class="text-[9px] font-black text-primary uppercase tracking-widest">Pase de Edición</span>
              <h3 class="text-2xl font-black text-slate-800">Pase Standard</h3>
              <p class="text-slate-400 text-xs font-medium">Ideal para eventos íntimos y elegantes.</p>
            </header>
            <div class="flex items-baseline gap-1">
              <span class="text-5xl font-black text-slate-900">$149</span>
              <span class="text-slate-400 text-sm font-bold uppercase">MXN</span>
            </div>
            <div class="w-full h-[1px] bg-slate-100"></div>
            <ul class="space-y-4 text-xs font-bold text-slate-600">
              <li class="flex items-center gap-2 text-primary">✓ Sin marcas de agua</li>
              <li class="flex items-center gap-2">✓ Portada Interactiva</li>
              <li class="flex items-center gap-2 text-primary font-black">✓ RSVP directo a WhatsApp</li>
              <li class="flex items-center gap-2">✓ Música de fondo (Predeterminada)</li>
              <li class="flex items-center gap-2">✓ Cuenta regresiva en vivo</li>
              <li class="flex items-center gap-2">✓ Personalización de paleta de colores</li>
            </ul>
          </div>
          <div class="pt-8">
            <button @click="handleAction('STANDARD')" class="btn btn-primary w-full h-14 rounded-2xl font-black shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform">
              Obtener Pase Standard
            </button>
          </div>
        </div>

        <!-- 3. Plan Premium -->
        <div class="bg-slate-950 rounded-[2.5rem] p-8 border border-slate-800 shadow-sm flex flex-col justify-between hover:shadow-2xl transition-all duration-300 relative overflow-hidden text-white">
          <div class="space-y-6">
            <header class="space-y-2">
              <span class="text-[9px] font-black text-purple-400 uppercase tracking-widest">Experiencia VIP</span>
              <h3 class="text-2xl font-black text-white">Pase Premium</h3>
              <p class="text-slate-400 text-xs font-medium">Control completo y personalización de lujo.</p>
            </header>
            <div class="flex items-baseline gap-1">
              <span class="text-5xl font-black text-white">$299</span>
              <span class="text-slate-500 text-sm font-bold uppercase">MXN</span>
            </div>
            <div class="w-full h-[1px] bg-slate-800"></div>
            <ul class="space-y-4 text-xs font-bold text-slate-300">
              <li class="flex items-center gap-2 text-purple-400">✓ Sin marcas de agua</li>
              <li class="flex items-center gap-2 text-purple-400">✓ Base de datos centralizada de invitados</li>
              <li class="flex items-center gap-2">✓ Música de fondo (Carga tus archivos)</li>
              <li class="flex items-center gap-2">✓ Cronograma interactivo del evento</li>
              <li class="flex items-center gap-2">✓ Apertura de sobres interactivos 3D</li>
              <li class="flex items-center gap-2">✓ Metadatos Open Graph personalizados (WhatsApp/FB)</li>
            </ul>
          </div>
          <div class="pt-8">
            <button @click="handleAction('PREMIUM')" class="btn bg-white hover:bg-slate-100 text-slate-950 border-none w-full h-14 rounded-2xl font-black hover:scale-[1.02] transition-transform">
              Obtener Pase Premium
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/modules/auth/store/auth';
import { deploymentService } from '@/modules/ecommerce/services/deploymentService';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

onMounted(() => {
  window.scrollTo(0, 0);
});

const handleAction = async (tier) => {
  if (tier === 'BASIC') {
    if (!authStore.isAuthenticated) {
      router.push({ name: 'register', query: { redirect: 'create-basic' } });
    } else {
      try {
        const res = await deploymentService.createSandbox(1);
        toast.success('¡Lienzo básico creado!');
        router.push(`/builder/${res.data.id}`);
      } catch (err) {
        toast.error('No se pudo crear el lienzo básico.');
      }
    }
  } else {
    // Si quieren comprar pase directo, redirigimos al catálogo de plantillas
    toast.info('Para comprar un pase, primero selecciona o crea un diseño borrador.');
    router.push('/catalog');
  }
};
</script>
