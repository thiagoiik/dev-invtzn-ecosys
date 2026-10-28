<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 font-sans">
    <div class="max-w-4xl mx-auto bg-white rounded-[2.5rem] p-10 md:p-16 shadow-xl border border-slate-100 space-y-10">
      <header class="space-y-4 text-center">
        <span class="text-xs font-black text-primary uppercase tracking-[0.3em]">Seguridad & Confianza</span>
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">Política de Privacidad</h1>
        <p class="text-slate-400 font-medium text-sm">Última actualización: 26 de Mayo, 2026</p>
        <div class="w-16 h-1 bg-primary mx-auto rounded-full mt-4"></div>
      </header>

      <div class="prose prose-slate max-w-none text-slate-600 leading-relaxed space-y-8">
        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">1. Información que Recopilamos</h2>
          <p>
            Recopilamos la información personal mínima indispensable que usted nos proporciona voluntariamente al registrarse, como su correo electrónico y nombre de usuario, así como los datos del evento (nombres, fechas, textos) para poder renderizar y procesar el editor de invitaciones.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">2. Uso de la Información</h2>
          <p>
            Utilizamos su información únicamente para proveer, operar y mejorar la experiencia de edición del Studio y asegurar que su invitación pública (`/i/:slug`) se cargue de forma correcta en dispositivos móviles. Los datos de RSVP de sus invitados son de su total propiedad y no son compartidos con ningún tercero.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">3. Transacciones con Stripe</h2>
          <p>
            Toda información financiera (tarjetas de crédito, cuentas bancarias, etc.) se gestiona externamente de manera encriptada por nuestro proveedor de pagos de confianza **Stripe**. Invitazyon no guarda ni tiene acceso directo a sus datos de tarjeta bancaria.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">4. Cookies y Análisis de Telemetría</h2>
          <p>
            Utilizamos cookies técnicas de sesión esenciales. Contamos con un servicio de telemetría de visitas y confirmaciones RSVP para indicarle en su panel de administración cuántas personas han visto su invitación y cuántas han confirmado asistencia. No compartimos esta información comercialmente.
          </p>
        </section>
      </div>

      <footer class="pt-8 border-t border-slate-100 flex justify-between items-center text-xs text-slate-400 font-bold uppercase tracking-wider">
        <span>Invitazyon © 2026</span>
        <router-link to="/catalog" class="text-primary hover:underline">Volver al Catálogo</router-link>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
onMounted(() => {
  window.scrollTo(0, 0);
});
</script>
