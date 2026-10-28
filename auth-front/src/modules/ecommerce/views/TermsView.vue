<template>
  <div class="min-h-screen bg-slate-50 py-16 px-6 font-sans">
    <div class="max-w-4xl mx-auto bg-white rounded-[2.5rem] p-10 md:p-16 shadow-xl border border-slate-100 space-y-10">
      <header class="space-y-4 text-center">
        <span class="text-xs font-black text-primary uppercase tracking-[0.3em]">Legal & Acuerdos</span>
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">Términos y Condiciones</h1>
        <p class="text-slate-400 font-medium text-sm">Última actualización: 26 de Mayo, 2026</p>
        <div class="w-16 h-1 bg-primary mx-auto rounded-full mt-4"></div>
      </header>

      <div class="prose prose-slate max-w-none text-slate-600 leading-relaxed space-y-8">
        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">1. Aceptación de los Términos</h2>
          <p>
            Al acceder y utilizar el sitio web y los servicios de Invitazyon.online, usted acepta expresamente estar sujeto a estos Términos y Condiciones de Uso, a nuestra Política de Privacidad y a todas las leyes y regulaciones aplicables. La aceptación de este contrato ocurre en el momento de crear su cuenta mediante el proceso de registro, reconociendo que este acuerdo constituye un contrato vinculante entre usted y Invitazyon.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">2. Licencia de Uso Personal (DRAFT / Sandbox)</h2>
          <p>
            Se concede permiso para crear borradores de forma gratuita en nuestra plataforma para uso personal y no comercial. Esto constituye el otorgamiento de una licencia de prueba limitada, no una transferencia de título. Bajo esta licencia, usted no puede:
          </p>
          <ul class="list-disc pl-6 space-y-2">
            <li>Modificar o copiar los materiales de diseño base propiedad de la plataforma.</li>
            <li>Utilizar los diseños para fines comerciales sin adquirir la respectiva licencia comercial (Pase Standard o Premium).</li>
            <li>Intentar descompilar o realizar ingeniería inversa de cualquier componente del Render Engine.</li>
          </ul>
          <p class="text-sm italic text-slate-500 mt-2">
            Aviso legal: La violación de estas restricciones resultará en la terminación inmediata de su acceso y podrá dar lugar a acciones legales por violación a los derechos de propiedad intelectual.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">3. Activación y Pagos de Pase</h2>
          <p>
            Nuestros pases digitales (Standard y Premium) otorgan el derecho de remover las marcas de agua de previsualización y activar el hosting público interactivo de su diseño durante la vigencia especificada. Los pagos se procesan de forma segura a través de Stripe y son definitivos una vez activado el servicio.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">4. Protección de Datos y Privacidad</h2>
          <p>
            El tratamiento de sus datos personales se regirá por nuestra Política de Privacidad, la cual forma parte integrante de estos Términos. Al aceptar este contrato, usted otorga su consentimiento para el tratamiento de sus datos conforme a dicha política.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">5. Limitaciones de Responsabilidad</h2>
          <p>
            En ningún caso Invitazyon o sus proveedores serán responsables de ningún daño (incluyendo, sin limitación, daños por pérdida de datos o beneficios, o debido a la interrupción del negocio) que surja del uso o de la imposibilidad de usar los diseños y servicios provistos.
          </p>
        </section>

        <section class="space-y-3">
          <h2 class="text-2xl font-bold text-slate-800">6. Jurisdicción y Ley Aplicable</h2>
          <p>
            Cualquier controversia derivada de la interpretación o ejecución de estos Términos se someterá a la jurisdicción exclusiva de los tribunales competentes de la Ciudad de México, renunciando las partes a cualquier otro fuero que pudiera corresponderles por razón de sus domicilios presentes o futuros.
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
