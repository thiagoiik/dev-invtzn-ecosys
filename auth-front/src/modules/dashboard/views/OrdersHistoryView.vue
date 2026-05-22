<template>
  <div v-if="authStore.user" class="space-y-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">Mis Pedidos</h1>
        <p class="text-slate-500 mt-1">Revisa tu historial de compras, descarga tus facturas y da seguimiento a tus envíos.</p>
      </div>
      <router-link to="/catalog" class="btn btn-ghost bg-white hover:bg-slate-50 border border-slate-200 rounded-2xl shadow-sm px-6 h-14 font-bold text-slate-700">
        🛍️ Seguir Comprando
      </router-link>
    </div>

    <!-- Filtros de Estado -->
    <div class="flex flex-wrap gap-2 border-b border-slate-200 pb-4">
      <button 
        v-for="filter in filters" 
        :key="filter.value"
        @click="activeFilter = filter.value"
        :class="[
          'px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300',
          activeFilter === filter.value 
            ? 'bg-primary text-white shadow-lg shadow-primary/20' 
            : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-100'
        ]"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Spinner de Carga -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="flex flex-col items-center gap-4">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="text-sm font-bold text-slate-400">Cargando tus compras...</p>
      </div>
    </div>

    <!-- Vista Vacía -->
    <div v-else-if="filteredOrders.length === 0" class="bg-white p-16 rounded-[2.5rem] shadow-sm border border-slate-100 text-center">
      <div class="text-6xl mb-6">📦</div>
      <h3 class="text-2xl font-black text-slate-800">No encontramos pedidos</h3>
      <p class="text-slate-500 mt-2 mb-8 max-w-md mx-auto">Parece que aún no tienes transacciones registradas en esta sección o no coinciden con el filtro seleccionado.</p>
      <router-link to="/catalog" class="btn btn-primary rounded-2xl shadow-lg shadow-primary/20 px-8 h-14 font-black">
        Explorar Catálogo
      </router-link>
    </div>

    <!-- Listado de Pedidos -->
    <div v-else class="space-y-8">
      <div 
        v-for="order in filteredOrders" 
        :key="order.id"
        class="bg-white rounded-[2.5rem] p-6 sm:p-8 shadow-sm hover:shadow-xl transition-all duration-500 border border-slate-100 flex flex-col gap-6"
      >
        <!-- Info Principal del Pedido -->
        <div class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-100">
          <div class="space-y-1">
            <div class="flex items-center gap-3">
              <span class="text-xl font-black text-slate-900">Pedido #{{ order.id }}</span>
              <span :class="[
                'badge font-black text-[10px] tracking-widest px-2.5 py-1.5 rounded-lg border-none uppercase',
                order.origin === 'POS' ? 'bg-indigo-50 text-indigo-600' : 'bg-pink-50 text-pink-600'
              ]">
                {{ order.origin === 'POS' ? 'Punto de Venta / B2B' : 'Tienda Online' }}
              </span>
            </div>
            <p class="text-xs font-bold text-slate-400">
              Realizado el {{ formatDate(order.created_at) }}
            </p>
          </div>

          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="text-xs text-slate-400 font-bold">Total Pagado</p>
              <p class="text-2xl font-black text-primary">{{ formatPrice(order.total_amount) }}</p>
            </div>
            <div :class="[
              'badge font-black text-xs tracking-widest px-4 py-3 rounded-xl border-none uppercase',
              order.status === 'COMPLETED' ? 'bg-success/10 text-success' : 
              order.status === 'REFUNDED' ? 'bg-error/10 text-error' : 'bg-warning/10 text-warning'
            ]">
              {{ order.status === 'COMPLETED' ? 'Completado' : 
                 order.status === 'REFUNDED' ? 'Reembolsado' : 'Pendiente' }}
            </div>
          </div>
        </div>

        <!-- Conceptos / Items de la Orden -->
        <div>
          <h3 class="text-sm font-black text-slate-400 uppercase tracking-widest mb-4">Artículos Adquiridos</h3>
          <div class="divide-y divide-slate-100">
            <div v-for="item in order.items" :key="item.product" class="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 first:pt-0 last:pb-0">
              <div class="flex items-start gap-4">
                <div class="w-12 h-12 bg-slate-50 rounded-xl flex items-center justify-center text-xl font-bold text-slate-600 border border-slate-100 flex-shrink-0">
                  {{ item.product_is_physical ? '📦' : '💎' }}
                </div>
                <div>
                  <h4 class="font-bold text-slate-800 text-base">{{ item.product_name || `Producto #${item.product}` }}</h4>
                  <p class="text-sm text-slate-500 font-medium">
                    Cantidad: <strong class="text-slate-700">{{ item.quantity }}</strong> &middot; Unitario: <strong class="text-slate-700">{{ formatPrice(item.price_at_sale) }}</strong>
                  </p>
                  
                  <!-- Claves de activación (Digitales) -->
                  <div v-if="!item.product_is_physical && item.serial_keys && item.serial_keys.length > 0" class="mt-3 space-y-2">
                    <p class="text-xs font-black text-slate-400 uppercase tracking-widest">Tus claves de activación:</p>
                    <div class="flex flex-wrap gap-2">
                      <div 
                        v-for="key in item.serial_keys" 
                        :key="key"
                        class="bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 flex items-center gap-2 group/key cursor-pointer hover:bg-primary/5 hover:border-primary/30 transition-colors"
                        @click="copyToClipboard(key)"
                        title="Click para copiar"
                      >
                        <code class="text-xs font-bold text-slate-700 font-mono">{{ key }}</code>
                        <span class="text-[10px] text-slate-400 group-hover/key:text-primary transition-colors">📋</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="text-right">
                <p class="font-black text-slate-800 text-lg">{{ formatPrice(item.price_at_sale * item.quantity) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Estatus de Envío Físico (Si aplica) -->
        <div v-if="hasPhysical(order)" class="bg-slate-50 border border-slate-100 rounded-3xl p-6 space-y-6">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <span class="text-xl">🚚</span>
              <div>
                <h4 class="font-bold text-slate-800">Estatus de Envío Físico</h4>
                <p class="text-xs text-slate-400 font-semibold">Producción y despacho de invitaciones impresas</p>
              </div>
            </div>
            
            <div v-if="order.tracking_number" class="bg-white border border-slate-200 rounded-xl px-4 py-2 flex items-center gap-3">
              <div>
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-wider">Número de Guía</p>
                <code class="text-xs font-black text-slate-700 font-mono">{{ order.tracking_number }}</code>
              </div>
              <a 
                :href="'https://www.google.com/search?q=' + encodeURIComponent(order.tracking_number)" 
                target="_blank" 
                class="btn btn-xs btn-primary rounded-lg font-bold"
              >
                Rastrear
              </a>
            </div>
            <div v-else class="bg-amber-50 border border-amber-200/50 text-amber-700 rounded-xl px-4 py-2 text-xs font-bold">
              Guía pendiente de generación
            </div>
          </div>

          <!-- Barra de Progreso Visual de Envío -->
          <div class="pt-2">
            <ul class="steps steps-vertical md:steps-horizontal w-full text-slate-600">
              <li :class="['step text-xs font-bold', getStepIndex(order.fulfillment_status) >= 0 ? 'step-primary' : '']">Pendiente</li>
              <li :class="['step text-xs font-bold', getStepIndex(order.fulfillment_status) >= 1 ? 'step-primary' : '']">En Producción</li>
              <li :class="['step text-xs font-bold', getStepIndex(order.fulfillment_status) >= 2 ? 'step-primary' : '']">Enviado</li>
              <li :class="['step text-xs font-bold', getStepIndex(order.fulfillment_status) >= 3 ? 'step-primary' : '']">Entregado</li>
            </ul>
          </div>
        </div>

        <!-- Sección de Facturación SAT CFDI 4.0 -->
        <div class="border-t border-slate-100 pt-6 flex flex-wrap items-center justify-between gap-6">
          <div class="flex items-center gap-3">
            <span class="text-xl">📄</span>
            <div>
              <h4 class="font-bold text-slate-800">Facturación Electrónica SAT</h4>
              <p class="text-xs text-slate-400 font-semibold" v-if="order.invoice">
                Folio UUID: <span class="font-mono text-slate-500">{{ order.invoice.uuid }}</span>
              </p>
              <p class="text-xs text-slate-400 font-semibold" v-else>
                Solicita tu factura CFDI 4.0 oficial después de tu pago.
              </p>
            </div>
          </div>

          <!-- Acciones de Facturación -->
          <div class="flex flex-wrap items-center gap-3">
            <template v-if="order.invoice">
              <div class="badge badge-success font-black text-[10px] tracking-widest px-3 py-2 rounded-lg border-none uppercase text-white mr-2">
                Facturado
              </div>
              
              <!-- Descargar PDF -->
              <a 
                v-if="order.invoice.pdf_url" 
                :href="order.invoice.pdf_url" 
                target="_blank" 
                class="btn btn-sm btn-ghost bg-slate-50 hover:bg-slate-100 rounded-xl font-bold text-slate-700"
              >
                📕 PDF
              </a>
              
              <!-- Descargar XML -->
              <a 
                v-if="order.invoice.xml_url" 
                :href="order.invoice.xml_url" 
                target="_blank" 
                class="btn btn-sm btn-ghost bg-slate-50 hover:bg-slate-100 rounded-xl font-bold text-slate-700"
              >
                💻 XML
              </a>
              
              <!-- Reenviar Correo -->
              <button 
                @click="handleResendInvoice(order)"
                class="btn btn-sm btn-primary btn-outline rounded-xl font-bold"
                :disabled="resendingInvoiceId === order.id"
              >
                <span v-if="resendingInvoiceId === order.id" class="loading loading-spinner loading-xs"></span>
                📧 Reenviar Email
              </button>
            </template>

            <!-- Solicitar Factura -->
            <template v-else-if="order.status === 'COMPLETED'">
              <button 
                @click="openBillingModal(order)"
                class="btn btn-sm btn-primary rounded-xl font-bold shadow-lg shadow-primary/10"
              >
                ✍️ Solicitar Factura SAT
              </button>
            </template>
            
            <template v-else>
              <span class="text-xs text-slate-400 font-bold italic">Disponible al confirmarse el pago</span>
            </template>

            <!-- Soporte -->
            <a 
              :href="'mailto:soporte@invitazyon.online?subject=Ayuda con Pedido %23' + order.id"
              class="btn btn-sm btn-ghost text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl font-bold ml-2"
            >
              ❔ Ayuda
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Facturación SAT CFDI 4.0 -->
    <dialog id="billing_modal" class="modal modal-bottom sm:modal-middle" :class="{ 'modal-open': selectedOrder }">
      <div v-if="selectedOrder" class="modal-box rounded-[2.5rem] max-w-xl p-8 border border-slate-100 shadow-2xl bg-white text-slate-800">
        <div class="flex justify-between items-start border-b border-slate-100 pb-4 mb-6">
          <div>
            <h3 class="font-black text-2xl text-slate-900">Solicitar Factura SAT</h3>
            <p class="text-xs text-slate-400 font-bold mt-1 uppercase tracking-wider">
              Pedido #{{ selectedOrder.id }} &middot; Total {{ formatPrice(selectedOrder.total_amount) }}
            </p>
          </div>
          <button @click="closeBillingModal" class="btn btn-sm btn-circle btn-ghost text-slate-400 hover:text-slate-700">✕</button>
        </div>

        <form @submit.prevent="submitBilling" class="space-y-4">
          <!-- RFC -->
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-600">RFC (México)</span></label>
            <input 
              v-model="billingForm.rfc" 
              type="text" 
              placeholder="XAXX010101000" 
              class="input input-bordered w-full rounded-xl focus:border-primary focus:ring-1 focus:ring-primary font-mono uppercase" 
              maxlength="13"
              required 
            />
            <p v-if="validationErrors.rfc" class="text-xs text-error font-bold mt-1">{{ validationErrors.rfc }}</p>
          </div>

          <!-- Razón Social -->
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-600">Nombre o Razón Social (Exacto SAT)</span></label>
            <input 
              v-model="billingForm.razon_social" 
              type="text" 
              placeholder="Juan Pérez Pérez o INVITAZYON SA DE CV" 
              class="input input-bordered w-full rounded-xl focus:border-primary focus:ring-1 focus:ring-primary uppercase" 
              required 
            />
            <p class="text-[10px] text-slate-400 font-semibold mt-1">Escríbelo en MAYÚSCULAS sin régimen societario (ej: sin S.A. de C.V.) según Constancia Fiscal.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Código Postal -->
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-600">Código Postal</span></label>
              <input 
                v-model="billingForm.codigo_postal" 
                type="text" 
                placeholder="06600" 
                class="input input-bordered w-full rounded-xl focus:border-primary focus:ring-1 focus:ring-primary font-mono" 
                maxlength="5"
                required 
              />
              <p v-if="validationErrors.codigo_postal" class="text-xs text-error font-bold mt-1">{{ validationErrors.codigo_postal }}</p>
            </div>

            <!-- Régimen Fiscal -->
            <div class="form-control">
              <label class="label"><span class="label-text font-bold text-slate-600">Régimen Fiscal</span></label>
              <select v-model="billingForm.regimen_fiscal" class="select select-bordered w-full rounded-xl" required>
                <option disabled value="">Selecciona una opción</option>
                <option v-for="option in regimenOptions" :key="option.value" :value="option.value">
                  {{ option.value }} - {{ option.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Uso de CFDI -->
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-600">Uso de CFDI</span></label>
            <select v-model="billingForm.uso_cfdi" class="select select-bordered w-full rounded-xl" required>
              <option disabled value="">Selecciona una opción</option>
              <option v-for="option in usoOptions" :key="option.value" :value="option.value">
                {{ option.value }} - {{ option.label }}
              </option>
            </select>
          </div>

          <!-- Correo de Envío (Opcional, pre-rellena el del cliente) -->
          <div class="form-control">
            <label class="label"><span class="label-text font-bold text-slate-600">Enviar factura a este correo</span></label>
            <input 
              v-model="billingForm.customer_email" 
              type="email" 
              placeholder="cliente@ejemplo.com" 
              class="input input-bordered w-full rounded-xl focus:border-primary focus:ring-1 focus:ring-primary" 
              required
            />
            <p class="text-[10px] text-slate-400 font-semibold mt-1">Los archivos PDF y XML oficiales serán enviados automáticamente a esta dirección al timbrar.</p>
          </div>

          <!-- Acciones -->
          <div class="flex gap-4 pt-6 border-t border-slate-100 mt-6">
            <button 
              type="button" 
              @click="closeBillingModal" 
              class="btn btn-ghost flex-1 rounded-xl font-bold" 
              :disabled="billingLoading"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn btn-primary flex-1 rounded-xl font-black shadow-lg shadow-primary/20"
              :disabled="billingLoading"
            >
              <span v-if="billingLoading" class="loading loading-spinner loading-sm"></span>
              {{ billingLoading ? 'Timbrando...' : 'Generar Factura SAT' }}
            </button>
          </div>
        </form>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/modules/auth/store/auth';
import { orderService } from '@/modules/ecommerce/services/orderService';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const toast = useToast();

// Estados
const orders = ref([]);
const loading = ref(true);
const billingLoading = ref(false);
const resendingInvoiceId = ref(null);
const activeFilter = ref('ALL');

// Filtro de Órdenes
const filters = [
  { label: 'Todos', value: 'ALL' },
  { label: 'Pendientes de Pago', value: 'PENDING' },
  { label: 'Completados', value: 'COMPLETED' }
];

const selectedOrder = ref(null);
const billingForm = ref({
  rfc: '',
  razon_social: '',
  codigo_postal: '',
  regimen_fiscal: '',
  uso_cfdi: '',
  customer_email: ''
});

const validationErrors = ref({
  rfc: '',
  codigo_postal: ''
});

// Opciones del SAT
const regimenOptions = [
  { value: '601', label: 'General de Ley Personas Morales' },
  { value: '603', label: 'Personas Morales con Fines no Lucrativos' },
  { value: '605', label: 'Sueldos y Salarios e Ingresos Asimilados a Salarios' },
  { value: '606', label: 'Arrendamiento' },
  { value: '612', label: 'Personas Físicas con Actividades Empresariales y Profesionales' },
  { value: '616', label: 'Sin obligaciones fiscales' },
  { value: '621', label: 'Incorporación Fiscal' },
  { value: '626', label: 'Régimen Simplificado de Confianza (RESICO)' }
];

const usoOptions = [
  { value: 'G03', label: 'Gastos en general' },
  { value: 'G01', label: 'Adquisición de mercancías' },
  { value: 'D01', label: 'Honorarios médicos, dentales y gastos hospitalarios' },
  { value: 'D02', label: 'Gastos médicos por incapacidad o discapacidad' },
  { value: 'S01', label: 'Sin efectos fiscales' },
  { value: 'CP01', label: 'Pagos' }
];

// Cargar pedidos
const fetchOrders = async () => {
  loading.value = true;
  try {
    const res = await orderService.getMyOrders();
    // Ordenar de más recientes a más antiguos
    orders.value = res.data.sort((a, b) => b.id - a.id);
  } catch (error) {
    toast.error('Error al cargar tu historial de pedidos.');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchOrders();
});

// Cómputo filtrado
const filteredOrders = computed(() => {
  if (activeFilter.value === 'ALL') return orders.value;
  return orders.value.filter(o => o.status === activeFilter.value);
});

// Métodos auxiliares
const hasPhysical = (order) => {
  return order.items?.some(item => item.product_is_physical);
};

const getStepIndex = (status) => {
  const steps = ['PENDING', 'IN_PRODUCTION', 'SHIPPED', 'DELIVERED'];
  return steps.indexOf(status);
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatPrice = (amount) => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(amount);
};

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
  toast.success('¡Clave copiada al portapapeles!');
};

// Modal de Facturación
const openBillingModal = (order) => {
  selectedOrder.value = order;
  billingForm.value = {
    rfc: '',
    razon_social: '',
    codigo_postal: '',
    regimen_fiscal: '',
    uso_cfdi: 'G03',
    customer_email: order.customer_email || authStore.user?.email || ''
  };
  validationErrors.value = {
    rfc: '',
    codigo_postal: ''
  };
};

const closeBillingModal = () => {
  selectedOrder.value = null;
};

// Envío de Factura
const submitBilling = async () => {
  // Resetear errores
  validationErrors.value.rfc = '';
  validationErrors.value.codigo_postal = '';

  // Validaciones cliente
  const rfcRegex = /^[A-Z&Ñ]{3,4}\d{6}[A-Z\d]{3}$/i;
  if (!rfcRegex.test(billingForm.value.rfc)) {
    validationErrors.value.rfc = 'Formato de RFC inválido. Debe tener 12 o 13 caracteres alfanuméricos válidos.';
    return;
  }

  const cpRegex = /^\d{5}$/;
  if (!cpRegex.test(billingForm.value.codigo_postal)) {
    validationErrors.value.codigo_postal = 'El código postal debe ser numérico de 5 dígitos.';
    return;
  }

  billingLoading.value = true;
  try {
    const payload = {
      rfc: billingForm.value.rfc.toUpperCase().trim(),
      razon_social: billingForm.value.razon_social.toUpperCase().trim(),
      codigo_postal: billingForm.value.codigo_postal.trim(),
      regimen_fiscal: billingForm.value.regimen_fiscal,
      uso_cfdi: billingForm.value.uso_cfdi,
      customer_email: billingForm.value.customer_email.trim()
    };

    const res = await orderService.issueCFDI(selectedOrder.value.id, payload);
    
    toast.success('¡Factura emitida con éxito y enviada por correo!');
    
    // Actualizar el pedido en la lista local para reflejar la factura
    const idx = orders.value.findIndex(o => o.id === selectedOrder.value.id);
    if (idx !== -1 && res.data.invoice) {
      orders.value[idx].invoice = res.data.invoice;
      // Sincronizar el correo en la orden si se actualizó
      if (payload.customer_email) {
        orders.value[idx].customer_email = payload.customer_email;
      }
    }

    closeBillingModal();
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.response?.data?.message || 'Error al emitir la factura. Revisa los datos fiscales.';
    toast.error(errorMsg);
  } finally {
    billingLoading.value = false;
  }
};

// Reenviar Factura por Correo
const handleResendInvoice = async (order) => {
  const currentEmail = order.customer_email || authStore.user?.email || '';
  const email = prompt('¿A qué correo deseas reenviar la factura PDF y XML?', currentEmail);
  
  if (email === null) return; // Cancelado por el usuario
  
  const emailTrimmed = email.trim();
  if (!emailTrimmed) {
    toast.warning('Debes proporcionar un correo válido.');
    return;
  }

  resendingInvoiceId.value = order.id;
  try {
    await orderService.resendInvoice(order.id, emailTrimmed);
    toast.success(`Factura encolada para reenviarse a: ${emailTrimmed}`);
    
    // Actualizar correo de contacto del pedido localmente
    const idx = orders.value.findIndex(o => o.id === order.id);
    if (idx !== -1) {
      orders.value[idx].customer_email = emailTrimmed;
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || 'Error al solicitar el reenvío de la factura.';
    toast.error(errorMsg);
  } finally {
    resendingInvoiceId.value = null;
  }
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
