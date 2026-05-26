<template>
  <div class="min-h-screen bg-slate-50 relative">
    
    <!-- NOTE: Redundant watermark markups removed; fully handled inside RenderEngineMaster component -->

    <!-- PANTALLA DE CARGA PREMIUM -->
    <DataLoaderLoader v-if="loading" />
 
    <!-- PANTALLA DE ERROR / EXPIRED / INACTIVE -->
    <div v-else-if="errorMsg || ['EXPIRED', 'INACTIVE'].includes(status)" class="min-h-screen">
      <ExpiredEventScreen v-if="['EXPIRED', 'INACTIVE'].includes(status)" :status="status" />
      
      <div v-else class="min-h-screen flex items-center justify-center p-4">
        <div class="alert alert-error shadow-lg max-w-md rounded-3xl">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <div>
            <h3 class="font-bold text-lg text-white">Invitación no disponible</h3>
            <p class="text-sm text-white/80">{{ errorMsg }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- MOTOR DE RENDER INTELIGENTE -->
    <EnvelopeWrapper v-else :type="customData.envelope_type || customData.envelope">
      <RenderEngineMaster 
        :status="status" 
        :customData="customData" 
        :slug="route.params.slug" 
        :deploymentId="deploymentId"
        :tierLevel="tierLevel"
        @purchase="goToCheckout"
      />
    </EnvelopeWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { engineService } from '@/modules/engine/services/engineService';
import { useAuthStore } from '@/modules/auth/store/auth';
import DataLoaderLoader from '@/modules/engine/components/DataLoaderLoader.vue';
import ExpiredEventScreen from '@/modules/engine/components/ExpiredEventScreen.vue';
import RenderEngineMaster from '@/modules/engine/components/RenderEngineMaster.vue';
import EnvelopeWrapper from '@/modules/engine/components/EnvelopeWrapper.vue';

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const errorMsg = ref('');
const customData = ref({});
const status = ref('');
const deploymentId = ref(null);
const tierLevel = ref('BASIC');
const productId = ref(null);

const authStore = useAuthStore();

const goToCheckout = () => {
  if (deploymentId.value) {
    localStorage.setItem('claimed_deployment_id', deploymentId.value);
  }
  
  const targetProductId = productId.value || 1;
  
  if (authStore.isAuthenticated) {
    router.push({ name: 'checkout', params: { id: targetProductId } });
  } else {
    router.push({ 
      name: 'register', 
      query: { redirect: `/checkout/${targetProductId}` } 
    });
  }
};

onMounted(async () => {
  const slug = route.params.slug;
  try {
    const response = await engineService.fetchDeploymentBySlug(slug);
    status.value = response.data.status;
    deploymentId.value = response.data.id;
    tierLevel.value = response.data.tier_level || 'BASIC';
    productId.value = response.data.product_id || null;
    
    if (['EXPIRED', 'INACTIVE'].includes(status.value)) {
      // El template se encargará de mostrar ExpiredEventScreen basándose en el status
      return;
    }

    customData.value = response.data.custom_data || {};
    
    // Registrar métrica de visita de forma no bloqueante
    try {
      engineService.submitMetric(slug, 'VISIT').catch(() => {});
    } catch (err) {}
  } catch (err) {
    errorMsg.value = 'No se encontró la invitación (URL inválida).';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Tailwind handles the layout */
</style>
