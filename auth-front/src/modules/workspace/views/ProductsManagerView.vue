<template>
  <div class="space-y-6">
    <!-- Header Card -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Catálogo de Productos</h2>
        <p class="text-slate-500">Administra los productos de tipo invitación, impresiones físicas y servicios.</p>
      </div>
      <button class="btn btn-primary" @click="openCreateDrawer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Producto
      </button>
    </div>

    <!-- Table List of Products -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div v-if="loading" class="flex justify-center items-center p-12">
        <span class="loading loading-spinner loading-lg text-primary"></span>
      </div>
      <div v-else-if="products.length === 0" class="p-12 text-center text-slate-400">
        <p class="italic">No se encontraron productos registrados en el sistema.</p>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
              <th class="px-6 py-4">SKU / ID</th>
              <th class="px-6 py-4">Nombre</th>
              <th class="px-6 py-4">Tipo</th>
              <th class="px-6 py-4">Tier / Nivel</th>
              <th class="px-6 py-4 text-right">Precio Base</th>
              <th class="px-6 py-4 text-center">Estado</th>
              <th class="px-6 py-4 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id" class="border-b border-slate-100 hover:bg-slate-50/55 transition-colors">
              <td class="px-6 py-4 font-mono text-xs">
                <span class="font-bold text-slate-700">{{ product.sku || 'N/A' }}</span>
                <span class="text-slate-400 block text-[10px]">ID: {{ product.id }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="font-bold text-slate-800">{{ product.name }}</div>
                <div class="text-xs text-slate-400 max-w-xs truncate">{{ product.description }}</div>
              </td>
              <td class="px-6 py-4 text-xs">
                <span :class="[
                  'badge badge-sm font-bold uppercase tracking-wider',
                  product.product_type === 'DIGITAL' ? 'bg-indigo-50 text-indigo-600' :
                  product.product_type === 'PHYSICAL' ? 'bg-pink-50 text-pink-600' :
                  'bg-teal-50 text-teal-600'
                ]">
                  {{ product.product_type }}
                </span>
              </td>
              <td class="px-6 py-4 text-xs">
                <span :class="[
                  'badge badge-sm font-black',
                  product.tier_level === 'PREMIUM' ? 'badge-primary' :
                  product.tier_level === 'STANDARD' ? 'badge-info' : 'badge-ghost'
                ]">
                  {{ product.tier_level }}
                </span>
              </td>
              <td class="px-6 py-4 text-right font-semibold text-slate-850">
                ${{ parseFloat(product.base_price).toFixed(2) }}
              </td>
              <td class="px-6 py-4 text-center">
                <div :class="['badge badge-sm font-bold', product.is_active ? 'badge-success text-white' : 'badge-ghost']">
                  {{ product.is_active ? 'Activo' : 'Inactivo' }}
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn btn-xs btn-outline btn-primary" @click="openEditDrawer(product)">
                    Editar
                  </button>
                  <button class="btn btn-xs btn-error text-white" @click="deleteProduct(product.id)">
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Right-Side Drawer (Slider Overlay) for Create/Edit -->
    <div v-if="drawerOpen" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 overflow-hidden">
        <!-- Backdrop overlay -->
        <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity" @click="closeDrawer"></div>

        <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
          <div class="pointer-events-auto w-screen max-w-md">
            <div class="flex h-full flex-col overflow-y-scroll bg-white shadow-2xl border-l border-slate-200">
              <!-- Drawer Header -->
              <div class="bg-slate-900 px-6 py-6 text-white flex justify-between items-center">
                <h2 class="text-lg font-bold">
                  {{ isEditMode ? 'Editar Producto' : 'Crear Producto' }}
                </h2>
                <button type="button" class="text-slate-400 hover:text-white text-xl font-bold" @click="closeDrawer">
                  ✕
                </button>
              </div>

              <!-- Drawer Content / Form -->
              <form @submit.prevent="saveProduct" class="flex-1 p-6 space-y-5">
                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-bold text-slate-700">Nombre del Producto</span></label>
                  <input v-model="form.name" type="text" placeholder="Ej: Invitación Premium" class="input input-bordered w-full" required />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">SKU</span></label>
                    <input v-model="form.sku" type="text" placeholder="INV-PRM-01" class="input input-bordered w-full" />
                  </div>
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">Tipo de Producto</span></label>
                    <select v-model="form.product_type" class="select select-bordered w-full">
                      <option value="DIGITAL">Invitación Digital</option>
                      <option value="PHYSICAL">Producto Físico</option>
                      <option value="SERVICE">Servicio / Boutique</option>
                    </select>
                  </div>
                </div>

                <div class="grid grid-cols-3 gap-3">
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">Precio Base</span></label>
                    <input v-model.number="form.base_price" type="number" step="0.01" class="input input-bordered w-full" required />
                  </div>
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">Costo</span></label>
                    <input v-model.number="form.cost_price" type="number" step="0.01" class="input input-bordered w-full" />
                  </div>
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">IVA Rate</span></label>
                    <input v-model.number="form.tax_rate" type="number" step="0.01" class="input input-bordered w-full" />
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">Tier Comercial</span></label>
                    <select v-model="form.tier_level" class="select select-bordered w-full">
                      <option value="BASIC">Básico / Gratis</option>
                      <option value="STANDARD">Standard</option>
                      <option value="PREMIUM">Premium</option>
                    </select>
                  </div>
                  <div class="form-control w-full">
                    <label class="label"><span class="label-text font-bold text-slate-700">Cantidad Stock</span></label>
                    <input v-model.number="form.stock_quantity" type="number" class="input input-bordered w-full" />
                  </div>
                </div>

                <div v-if="form.product_type === 'DIGITAL'" class="form-control w-full">
                  <label class="label"><span class="label-text font-bold text-slate-700">Slug de Plantilla (Lienzo Maestro)</span></label>
                  <input v-model="form.template_slug" type="text" placeholder="Ej: boda-elegante-oro" class="input input-bordered w-full" />
                  <p class="text-[10px] text-slate-400 mt-1">El slug del lienzo maestro que se clonará automáticamente al comprar o probar este producto.</p>
                </div>

                <div class="form-control w-full">
                  <label class="label"><span class="label-text font-bold text-slate-700">Descripción</span></label>
                  <textarea v-model="form.description" placeholder="Ingresa los detalles o descripción corta del producto..." class="textarea textarea-bordered w-full h-24"></textarea>
                </div>

                <!-- Checkboxes Config -->
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-3">
                  <span class="text-xs font-bold text-slate-500 uppercase tracking-widest block">Opciones del Producto</span>
                  
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="form.is_physical" type="checkbox" class="checkbox checkbox-primary checkbox-sm" />
                    <span class="text-sm font-medium text-slate-700">¿Es un Producto Físico?</span>
                  </label>

                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="form.has_template" type="checkbox" class="checkbox checkbox-primary checkbox-sm" />
                    <span class="text-sm font-medium text-slate-700">¿Genera Despliegue Automático?</span>
                  </label>

                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="form.display_pcard" type="checkbox" class="checkbox checkbox-primary checkbox-sm" />
                    <span class="text-sm font-medium text-slate-700">Destacar en Landing (pcard)</span>
                  </label>

                  <label class="flex items-center gap-3 cursor-pointer">
                    <input v-model="form.is_active" type="checkbox" class="checkbox checkbox-primary checkbox-sm" />
                    <span class="text-sm font-medium text-slate-700">Producto Activo</span>
                  </label>
                </div>

                <!-- Drawer Footer Actions -->
                <div class="pt-4 border-t border-slate-100 flex justify-end gap-3">
                  <button type="button" class="btn btn-ghost" @click="closeDrawer">Cancelar</button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span v-if="saving" class="loading loading-spinner"></span>
                    Guardar Producto
                  </button>
                </div>
              </form>

            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import invtznClient from '@/core/api/invtznClient';

const toast = useToast();
const products = ref([]);
const loading = ref(false);
const saving = ref(false);

const drawerOpen = ref(false);
const isEditMode = ref(false);
const editProductId = ref(null);

const form = ref({
  name: '',
  description: '',
  sku: '',
  product_type: 'DIGITAL',
  base_price: 299.00,
  cost_price: 0.00,
  tax_rate: 0.16,
  tier_level: 'STANDARD',
  is_physical: false,
  stock_quantity: 0,
  has_template: true,
  display_pcard: false,
  is_active: true,
  template_slug: '',
  features: {}
});

const fetchProducts = async () => {
  loading.value = true;
  try {
    const res = await invtznClient.get('products/');
    products.value = res.data;
  } catch (error) {
    toast.error('Error al cargar la lista de productos.');
  } finally {
    loading.value = false;
  }
};

const openCreateDrawer = () => {
  isEditMode.value = false;
  editProductId.value = null;
  form.value = {
    name: '',
    description: '',
    sku: '',
    product_type: 'DIGITAL',
    base_price: 299.00,
    cost_price: 0.00,
    tax_rate: 0.16,
    tier_level: 'STANDARD',
    is_physical: false,
    stock_quantity: 0,
    has_template: true,
    display_pcard: false,
    is_active: true,
    template_slug: '',
    features: {}
  };
  drawerOpen.value = true;
};

const openEditDrawer = (product) => {
  isEditMode.value = true;
  editProductId.value = product.id;
  form.value = {
    name: product.name || '',
    description: product.description || '',
    sku: product.sku || '',
    product_type: product.product_type || 'DIGITAL',
    base_price: parseFloat(product.base_price) || 0,
    cost_price: parseFloat(product.cost_price) || 0,
    tax_rate: parseFloat(product.tax_rate) || 0.16,
    tier_level: product.tier_level || 'STANDARD',
    is_physical: product.is_physical ?? false,
    stock_quantity: product.stock_quantity ?? 0,
    has_template: product.has_template ?? true,
    display_pcard: product.display_pcard ?? false,
    is_active: product.is_active ?? true,
    template_slug: product.template_slug || '',
    features: product.features || {}
  };
  drawerOpen.value = true;
};

const closeDrawer = () => {
  drawerOpen.value = false;
};

const saveProduct = async () => {
  saving.value = true;
  try {
    const payload = { ...form.value };
    if (isEditMode.value) {
      await invtznClient.put(`products/${editProductId.value}/`, payload);
      toast.success('Producto actualizado con éxito.');
    } else {
      await invtznClient.post('products/', payload);
      toast.success('Producto creado con éxito.');
    }
    drawerOpen.value = false;
    fetchProducts();
  } catch (error) {
    const errMsg = error.response?.data?.sku?.[0] || error.response?.data?.name?.[0] || 'No se pudo guardar el producto.';
    toast.error(errMsg);
  } finally {
    saving.value = false;
  }
};

const deleteProduct = async (id) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el producto #${id}?`)) {
    try {
      await invtznClient.delete(`products/${id}/`);
      toast.success('Producto eliminado con éxito.');
      fetchProducts();
    } catch (error) {
      toast.error('No se pudo eliminar el producto.');
    }
  }
};

onMounted(() => {
  fetchProducts();
});
</script>
