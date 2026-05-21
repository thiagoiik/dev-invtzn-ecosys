<template>
  <div :class="['fixed inset-y-0 right-0 w-full max-w-xl md:max-w-2xl bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out border-l border-slate-200 flex flex-col', isOpen ? 'translate-x-0' : 'translate-x-full']">
    
    <!-- Header -->
    <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
      <div>
        <h3 class="font-black text-slate-800 text-lg uppercase tracking-tight flex items-center gap-2">
          📊 Métricas de Invitación
        </h3>
        <p class="text-xs text-slate-400 font-bold uppercase tracking-wider">
          Slug: <span class="text-indigo-600 font-black">/i/{{ metricsData?.slug || '...' }}</span>
        </p>
      </div>
      <button @click="$emit('close')" class="btn btn-circle btn-ghost btn-sm">✕</button>
    </div>

    <!-- Content loader -->
    <div v-if="loading" class="flex-grow flex flex-col justify-center items-center p-8 space-y-4">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="text-sm text-slate-400 font-bold uppercase tracking-wider animate-pulse">Obteniendo métricas...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="!metricsData" class="flex-grow flex flex-col justify-center items-center p-8 text-center">
      <div class="text-6xl mb-4">📭</div>
      <h3 class="text-lg font-bold text-slate-700">Sin datos de telemetría</h3>
      <p class="text-sm text-slate-400 mt-1">Aún no se han registrado interacciones para este diseño.</p>
    </div>

    <!-- Metrics Content -->
    <div v-else class="flex-1 overflow-y-auto p-6 space-y-8 bg-slate-50/30">
      
      <!-- Summary Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Card 1: Total Visits -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
          <span class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-1">Visitas Totales</span>
          <span class="text-2xl font-black text-slate-800">{{ metricsData.summary.total_visits }}</span>
          <span class="text-[10px] text-slate-400 mt-auto font-medium">Accesos registrados</span>
        </div>
        <!-- Card 2: Unique Visits -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
          <span class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-1">Visitantes Únicos</span>
          <span class="text-2xl font-black text-slate-800">{{ metricsData.summary.unique_visits }}</span>
          <span class="text-[10px] text-slate-400 mt-auto font-medium">Por IP + Navegador</span>
        </div>
        <!-- Card 3: RSVPs -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
          <span class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-1">RSVPs Recibidos</span>
          <span class="text-2xl font-black text-emerald-600">{{ metricsData.summary.total_rsvps }}</span>
          <span class="text-[10px] text-slate-400 mt-auto font-medium">Asistencia confirmada</span>
        </div>
        <!-- Card 4: RSVP Rate -->
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
          <span class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-1">Conversión RSVP</span>
          <span class="text-2xl font-black text-indigo-600">{{ metricsData.summary.rsvp_rate }}%</span>
          <span class="text-[10px] text-slate-400 mt-auto font-medium">Conversión de visitas</span>
        </div>
      </div>

      <!-- Sparkline Timeline Chart -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex justify-between items-center">
          <div>
            <h4 class="font-bold text-slate-800 text-sm">Histórico de Visitas Diarias</h4>
            <p class="text-xs text-slate-400">Tendencia de interacciones en el tiempo</p>
          </div>
          <div class="flex items-center gap-3 text-xs font-bold uppercase">
            <span class="flex items-center gap-1"><span class="w-3 h-3 bg-indigo-500 rounded-full"></span> Visitas</span>
            <span class="flex items-center gap-1"><span class="w-3 h-3 bg-emerald-500 rounded-full"></span> RSVPs</span>
          </div>
        </div>

        <div v-if="metricsData.daily && metricsData.daily.length > 0" class="relative">
          <svg class="w-full h-40 overflow-visible" viewBox="0 0 500 150" preserveAspectRatio="none">
            <!-- Grid lines -->
            <line x1="20" y1="20" x2="480" y2="20" stroke="#f1f5f9" stroke-width="1" />
            <line x1="20" y1="75" x2="480" y2="75" stroke="#f1f5f9" stroke-width="1" />
            <line x1="20" y1="130" x2="480" y2="130" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4" />

            <!-- Daily Visits Path -->
            <path :d="chartPath" fill="none" stroke="#6366f1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
            <!-- Area under Visits Path -->
            <path :d="chartAreaPath" fill="url(#gradVisits)" opacity="0.1" />

            <!-- Daily RSVPs Path -->
            <path :d="chartRsvpsPath" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            
            <!-- Tooltip indicators -->
            <g v-for="(p, idx) in chartPoints" :key="'pts-'+idx">
              <circle :cx="p.x" :cy="p.y" r="4" fill="#6366f1" stroke="white" stroke-width="2" class="cursor-pointer hover:r-6 transition-all" />
              <title>{{ p.date }}: {{ p.visits }} visitas</title>
            </g>

            <defs>
              <linearGradient id="gradVisits" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#6366f1" />
                <stop offset="100%" stop-color="#6366f1" stop-opacity="0" />
              </linearGradient>
            </defs>
          </svg>
          
          <!-- Timeline Dates Footer -->
          <div class="flex justify-between text-[9px] font-bold text-slate-400 uppercase pt-2 px-4 border-t border-slate-100">
            <span>{{ metricsData.daily[0]?.date }}</span>
            <span>{{ metricsData.daily[Math.floor(metricsData.daily.length / 2)]?.date }}</span>
            <span>{{ metricsData.daily[metricsData.daily.length - 1]?.date }}</span>
          </div>
        </div>
        <div v-else class="h-40 flex items-center justify-center text-slate-300 text-xs font-semibold uppercase">
          Insuficientes datos históricos
        </div>
      </div>

      <!-- Stats Breakdown -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Devices distribution -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h4 class="font-bold text-slate-800 text-sm uppercase tracking-wider border-b border-slate-100 pb-2">📱 Dispositivos</h4>
          <div class="space-y-3">
            <div v-for="item in metricsData.by_device" :key="item.device" class="space-y-1">
              <div class="flex justify-between text-xs font-bold text-slate-600">
                <span>{{ item.device }}</span>
                <span>{{ item.count }} ({{ getDevicePercent(item.count) }}%)</span>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div class="bg-indigo-600 h-full rounded-full transition-all duration-500" :style="{ width: `${getDevicePercent(item.count)}%` }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Browsers distribution -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h4 class="font-bold text-slate-800 text-sm uppercase tracking-wider border-b border-slate-100 pb-2">🌐 Navegadores</h4>
          <div class="space-y-3">
            <div v-for="item in metricsData.by_browser" :key="item.browser" class="space-y-1">
              <div class="flex justify-between text-xs font-bold text-slate-600">
                <span>{{ item.browser }}</span>
                <span>{{ item.count }} ({{ getDevicePercent(item.count) }}%)</span>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-full rounded-full transition-all duration-500" :style="{ width: `${getDevicePercent(item.count)}%` }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Countries distribution -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4 md:col-span-2">
          <h4 class="font-bold text-slate-800 text-sm uppercase tracking-wider border-b border-slate-100 pb-2">🌍 Ubicación Geográfica</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Countries list -->
            <div class="space-y-3 border-r border-slate-100 pr-4">
              <div class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-2">Países</div>
              <div v-for="item in metricsData.by_country.slice(0, 5)" :key="item.country" class="space-y-1">
                <div class="flex justify-between text-xs font-bold text-slate-600">
                  <span>{{ item.country || 'Desconocido' }}</span>
                  <span>{{ item.count }} visitas</span>
                </div>
                <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-indigo-500 h-full rounded-full" :style="{ width: `${(item.count / maxCountryCount) * 100}%` }"></div>
                </div>
              </div>
            </div>

            <!-- Cities list -->
            <div class="space-y-3 pl-4">
              <div class="text-[10px] text-slate-400 font-black uppercase tracking-wider mb-2">Ciudades</div>
              <div v-for="item in metricsData.by_city.slice(0, 5)" :key="item.city" class="space-y-1">
                <div class="flex justify-between text-xs font-bold text-slate-600">
                  <span>{{ item.city || 'Desconocido' }}</span>
                  <span>{{ item.count }} visitas</span>
                </div>
                <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                  <div class="bg-indigo-400 h-full rounded-full" :style="{ width: `${(item.count / maxCityCount) * 100}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Recent Log list -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h4 class="font-bold text-slate-800 text-sm uppercase tracking-wider border-b border-slate-100 pb-2">📋 Historial de Accesos Recientes</h4>
        <div class="overflow-x-auto">
          <table class="table table-xs w-full">
            <thead>
              <tr class="text-slate-400 font-bold uppercase text-[9px] tracking-wider">
                <th>Fecha / Hora</th>
                <th>Acción</th>
                <th>IP</th>
                <th>Dispositivo / Navegador</th>
                <th>Ubicación</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in metricsData.recent" :key="log.id" class="hover">
                <td class="font-semibold text-slate-600">{{ log.created_at }}</td>
                <td>
                  <span :class="['badge font-black text-[9px] uppercase tracking-wider py-1 px-2 rounded-md', log.metric_type === 'VISIT' ? 'badge-neutral bg-slate-100 border-none text-slate-600' : 'badge-success text-white']">
                    {{ log.metric_type === 'VISIT' ? 'Visita' : 'RSVP' }}
                  </span>
                </td>
                <td class="font-mono text-slate-400">{{ log.ip_address }}</td>
                <td class="text-slate-500 font-medium">
                  {{ log.device }} / {{ log.browser }}
                </td>
                <td class="text-slate-600 font-semibold">
                  {{ log.city }}, {{ log.country }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- Footer -->
    <div class="p-6 border-t border-slate-100 bg-slate-50 flex gap-4">
      <button class="btn btn-outline btn-block" @click="$emit('close')">Cerrar Métricas</button>
    </div>
  </div>

  <!-- Backdrop -->
  <div v-if="isOpen" @click="$emit('close')" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40"></div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { crmService } from '@/modules/workspace/services/crmService';

const props = defineProps(['isOpen', 'deploymentId']);
defineEmits(['close']);

const loading = ref(false);
const metricsData = ref(null);

const fetchMetrics = async () => {
  if (!props.deploymentId) return;
  loading.value = true;
  try {
    const res = await crmService.fetchDeploymentMetrics(props.deploymentId);
    metricsData.value = res.data;
  } catch (error) {
    console.error('Error fetching deployment metrics', error);
  } finally {
    loading.value = false;
  }
};

watch(() => [props.isOpen, props.deploymentId], ([newOpen, newId]) => {
  if (newOpen && newId) {
    fetchMetrics();
  } else if (!newOpen) {
    metricsData.value = null;
  }
});

// Helper for device & browser percentages
const getDevicePercent = (count) => {
  if (!metricsData.value || !metricsData.value.summary.total_visits) return 0;
  const total = metricsData.value.summary.total_visits;
  return Math.round((count / total) * 100);
};

// Max values for relative bars sizing
const maxCountryCount = computed(() => {
  if (!metricsData.value || !metricsData.value.by_country.length) return 1;
  return Math.max(...metricsData.value.by_country.map(c => c.count), 1);
});

const maxCityCount = computed(() => {
  if (!metricsData.value || !metricsData.value.by_city.length) return 1;
  return Math.max(...metricsData.value.by_city.map(c => c.count), 1);
});

// --- Dynamic SVG Sparkline Computation ---
const chartPoints = computed(() => {
  if (!metricsData.value || !metricsData.value.daily || metricsData.value.daily.length === 0) {
    return [];
  }
  const daily = metricsData.value.daily;
  const maxVisits = Math.max(...daily.map(d => d.visits), 10);
  const width = 500;
  const height = 150;
  const padding = 20;

  return daily.map((d, index) => {
    const x = padding + (index * (width - 2 * padding)) / Math.max(daily.length - 1, 1);
    const y = height - padding - (d.visits * (height - 2 * padding)) / maxVisits;
    return { x, y, date: d.date, visits: d.visits };
  });
});

const chartPath = computed(() => {
  const pts = chartPoints.value;
  return pts.length > 0 ? `M ${pts.map(p => `${p.x},${p.y}`).join(' L ')}` : '';
});

const chartAreaPath = computed(() => {
  const pts = chartPoints.value;
  if (pts.length === 0) return '';
  const height = 150;
  const padding = 20;
  const firstX = pts[0].x;
  const lastX = pts[pts.length - 1].x;
  return `M ${firstX},${height - padding} L ${pts.map(p => `${p.x},${p.y}`).join(' L ')} L ${lastX},${height - padding} Z`;
});

const chartRsvpsPath = computed(() => {
  if (!metricsData.value || !metricsData.value.daily || metricsData.value.daily.length === 0) {
    return '';
  }
  const daily = metricsData.value.daily;
  const maxVisits = Math.max(...daily.map(d => d.visits), 10);
  const width = 500;
  const height = 150;
  const padding = 20;

  const points = daily.map((d, index) => {
    const x = padding + (index * (width - 2 * padding)) / Math.max(daily.length - 1, 1);
    const y = height - padding - (d.rsvps * (height - 2 * padding)) / maxVisits;
    return `${x},${y}`;
  });

  return points.length > 0 ? `M ${points.join(' L ')}` : '';
});
</script>

<style scoped>
/* Scoped overrides if needed, Tailwind classes handle the layout */
</style>
