<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 font-sans">
    <div class="max-w-4xl mx-auto bg-white rounded-[2.5rem] p-10 md:p-16 shadow-xl border border-slate-100 space-y-10">
      <header class="space-y-4 text-center">
        <span class="text-xs font-black text-primary uppercase tracking-[0.3em]">Garantía Transparente</span>
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">Política de Devoluciones</h1>
        <p class="text-slate-400 font-medium text-sm">Última actualización: 26 de Mayo, 2026</p>
        <div class="w-16 h-1 bg-primary mx-auto rounded-full mt-4"></div>
      </header>

      <div class="prose prose-slate max-w-none text-slate-600 leading-relaxed space-y-8">
        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">Garantía de Satisfacción y Pruebas Gratis</h2>
          <p>
            En <strong>Invitazyon</strong>, creemos en la transparencia absoluta. Por esta razón, ofrecemos un entorno de pruebas sandbox (borrador gratuito) completo e ilimitado para que usted pueda armar, personalizar y visualizar su invitación antes de realizar cualquier tipo de pago.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">1. Condiciones de Devolución para Pases Digitales</h2>
          <p>
            Debido a que nuestros pases digitales (Standard y Premium) otorgan acceso inmediato al hosting en vivo, la eliminación instantánea de marcas de agua, y el desbloqueo de módulos avanzados de música e itinerarios de forma irrevocable, no se ofrecen reembolsos una vez activado el pase en vivo, a menos que:
          </p>
          <ul class="list-disc pl-6 space-y-2">
            <li>Exista un fallo técnico grave y persistente en el Render Engine que impida de forma absoluta la visualización pública de la invitación y que no pueda ser resuelto por nuestro equipo de soporte técnico dentro de las 48 horas posteriores al reporte.</li>
            <li>Se detecte un cobro duplicado o erróneo por parte de la pasarela de pagos Stripe.</li>
          </ul>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">2. Productos Físicos e Impresos</h2>
          <p>
            Para pedidos que involucren impresiones físicas (como invitaciones en papel de boutique, sobres de lujo, etc.):
          </p>
          <ul class="list-disc pl-6 space-y-2">
            <li>Se admitirá una cancelación y reembolso del 100% del costo físico únicamente si el pedido aún no ha sido enviado al taller de impresión.</li>
            <li>Una vez impresos los productos personalizados, no se admiten devoluciones por tratarse de piezas únicas hechas a la medida, a menos que existan defectos de fabricación evidentes o discrepancias graves con respecto a los textos aprobados.</li>
          </ul>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">3. Cómo Solicitar Asistencia</h2>
          <p>
            Si experimenta cualquier inconveniente con su pago o la carga de sus recursos interactivos, por favor póngase en contacto inmediato con nuestro equipo a través de la pestaña de <router-link to="/ayuda" class="text-primary hover:underline">Soporte y Ayuda</router-link>, o bien escribiendo directamente a nuestro WhatsApp oficial de soporte. Estaremos encantados de resolver su caso.
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
