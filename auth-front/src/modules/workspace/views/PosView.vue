<template>
  <div class="space-y-6">
    <!-- Banner de Estado de Conexión (Online/Offline) -->
    <div v-if="isOffline" class="flex items-center gap-3 bg-amber-500 text-white p-4 rounded-2xl shadow-md border border-amber-600 animate-pulse">
      <div class="bg-amber-600/30 p-2 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-3.536 4.978 4.978 0 011.414-3.536m0 0L5.636 5.636M8.464 15.536L5.636 18.364m0 0L3 21m3.636-15.364l2.829 2.829m-2.829-2.829L3 3" />
        </svg>
      </div>
      <div>
        <h4 class="font-bold">Modo Sin Conexión (Offline) Activo</h4>
        <p class="text-xs opacity-90">Los cobros están limitados a EFECTIVO (CASH). El catálogo se cargó desde la memoria local. Las ventas se sincronizarán al recuperar la red.</p>
      </div>
    </div>

    <div v-if="syncingQueue" class="flex items-center gap-3 bg-indigo-600 text-white p-4 rounded-2xl shadow-md border border-indigo-700">
      <span class="loading loading-spinner loading-md"></span>
      <div>
        <h4 class="font-bold">Sincronizando Ventas Locales</h4>
        <p class="text-xs opacity-90">Enviando órdenes registradas offline al servidor. Por favor no cierres la ventana.</p>
      </div>
    </div>

    <!-- Header dinámico con tienda -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Terminal Punto de Venta (POS)</h2>
        <p class="text-slate-500">
          {{ assignedStore ? `Sucursal: ${assignedStore.name}` : 'Modo Venta a Distancia' }}
        </p>
      </div>
      <div class="flex gap-3 items-center">
        <!-- Indicador de cola offline pendiente -->
        <span v-if="offlineQueueLength > 0" class="badge badge-warning font-bold p-3">
          {{ offlineQueueLength }} Ventas Offline Pendientes
        </span>
        <button v-if="activeSession && !isOffline" class="btn btn-outline btn-error" @click="closeSession">
          Cerrar Turno
        </button>
        <div class="badge badge-primary p-4 font-bold uppercase">{{ vendorMode }}</div>
      </div>
    </div>

    <!-- Pantalla de Bloqueo: Apertura de Turno (Solo para Vendedores Físicos) -->
    <div v-if="vendorMode === 'PHYSICAL' && !activeSession && !isOffline" class="flex justify-center py-20">
      <div class="card w-96 bg-white shadow-xl border border-primary/20">
        <div class="card-body text-center">
          <div class="bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold">Apertura de Caja</h3>
          <p class="text-slate-500 text-sm mb-6">Ingresa el saldo inicial para comenzar a vender en esta sucursal.</p>
          <div class="form-control">
            <input v-model="openingBalance" type="number" placeholder="$0.00" class="input input-bordered text-center text-2xl font-bold" />
          </div>
          <button class="btn btn-primary btn-block mt-6" @click="startShift" :disabled="loadingSession">
            <span v-if="loadingSession" class="loading loading-spinner"></span>
            Abrir Turno
          </button>
        </div>
      </div>
    </div>

    <!-- Interfaz de Venta (Visible si hay sesión, si es remoto, o si está offline) -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Columna Izquierda: Búsqueda y Selección de Producto -->
      <div class="md:col-span-2 space-y-6">
        <!-- Buscador -->
        <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="🔍 Buscar por nombre o SKU..." 
            class="input input-bordered w-full font-medium" 
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="prod in filteredProducts" 
            :key="prod.id"
            class="card bg-white border border-slate-200 shadow-sm cursor-pointer transition-all hover:border-primary hover:shadow-md flex flex-col justify-between"
            @click="addToCart(prod)"
          >
            <div class="card-body p-6">
              <div class="flex justify-between items-start gap-2">
                <div>
                  <h3 class="font-bold text-slate-800">{{ prod.name }}</h3>
                  <span v-if="prod.sku" class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono font-bold mt-1 inline-block">SKU: {{ prod.sku }}</span>
                  <span class="ml-1 text-[10px] px-2 py-0.5 rounded font-bold" :class="prod.is_physical ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'">
                    {{ prod.is_physical ? 'Físico (Entrega)' : 'Digital (Tier)' }}
                  </span>
                </div>
                <span class="text-primary font-black shrink-0">${{ parseFloat(prod.base_price).toFixed(2) }}</span>
              </div>
              <p class="text-sm text-slate-500 mt-2 line-clamp-2">{{ prod.description }}</p>
            </div>
          </div>
        </div>

        <div v-if="loadingProducts" class="flex justify-center py-10">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>

        <div v-if="!loadingProducts && filteredProducts.length === 0" class="text-center py-12 text-slate-400 font-medium">
          No se encontraron productos.
        </div>
      </div>

      <!-- Columna Derecha: Carrito, Cliente, Pago y Total -->
      <div class="space-y-6">
        <!-- Card de Carrito de Compras -->
        <div class="card bg-white shadow-md border border-slate-200">
          <div class="card-body p-6">
            <h3 class="text-lg font-bold text-slate-800 border-b pb-3 mb-4">Carrito de Compras</h3>
            
            <!-- Items de Carrito -->
            <div v-if="cart.length > 0" class="space-y-4 max-h-60 overflow-y-auto pr-1">
              <div v-for="item in cart" :key="item.product.id" class="flex items-center justify-between gap-2 pb-3 border-b border-slate-100 last:border-0 last:pb-0">
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-sm text-slate-800 truncate">{{ item.product.name }}</p>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-[10px] px-1.5 py-0.5 rounded font-bold" :class="item.product.is_physical ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'">
                      {{ item.product.is_physical ? 'Físico (Entrega)' : 'Digital (Tier)' }}
                    </span>
                    <p class="text-xs text-slate-500">${{ parseFloat(item.price).toFixed(2) }} c/u</p>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <button class="btn btn-xs btn-circle btn-outline btn-neutral" @click.stop="decrementQty(item)">-</button>
                  <span class="font-bold text-sm w-4 text-center">{{ item.quantity }}</span>
                  <button class="btn btn-xs btn-circle btn-outline btn-neutral" @click.stop="incrementQty(item)">+</button>
                  <button class="btn btn-xs btn-ghost btn-circle text-error ml-1" @click.stop="removeFromCart(item)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-6 text-slate-400 text-sm italic">
              El carrito está vacío.
            </div>
          </div>
        </div>

        <!-- Card de Checkout / Cliente / Pago -->
        <div class="card bg-white shadow-xl border border-slate-200 overflow-hidden">
          <!-- Panel de Comisiones Rápido -->
          <div class="bg-slate-900 p-4 text-white flex justify-between items-center">
            <span class="text-xs font-bold uppercase opacity-60">Mis Comisiones</span>
            <span class="font-black text-green-400">${{ totalCommissions.toFixed(2) }}</span>
          </div>
          
          <div class="card-body p-6">
            <h3 class="text-lg font-bold text-slate-800 border-b pb-4 mb-4">Finalizar Venta</h3>
            
            <!-- Buscador de Cliente -->
            <div class="form-control w-full mb-4">
              <label class="label justify-between items-center">
                <span class="label-text font-bold">Cliente</span>
                <button 
                  type="button" 
                  class="text-xs text-primary font-bold hover:underline"
                  @click="selectPublicCustomer"
                >
                  Público General
                </button>
              </label>
              <div class="join w-full">
                <input 
                  v-model="customerSearchId" 
                  type="text" 
                  placeholder="Buscar por ID, Nombre o Teléfono" 
                  class="input input-bordered join-item w-full font-semibold" 
                  :disabled="isOffline"
                  @keyup.enter="findCustomer"
                />
                <button 
                  class="btn btn-primary join-item animate-hover" 
                  @click="findCustomer" 
                  :disabled="searching || isOffline"
                >
                  <span v-if="searching" class="loading loading-spinner loading-xs"></span>
                  Buscar
                </button>
              </div>

              <!-- Resultados de búsqueda múltiples -->
              <div v-if="matchingCustomers.length > 1" class="mt-2 p-2 bg-white border border-slate-200 rounded-xl shadow-lg max-h-48 overflow-y-auto z-10 flex flex-col gap-1">
                <p class="text-xs font-bold text-slate-500 px-2 py-1">Selecciona un cliente:</p>
                <button 
                  v-for="c in matchingCustomers" 
                  :key="c.remote_auth_id"
                  type="button"
                  class="w-full text-left px-3 py-2 hover:bg-slate-50 rounded-lg flex justify-between items-center text-sm transition"
                  @click="selectCustomer(c)"
                >
                  <div>
                    <span class="font-bold text-slate-800">{{ c.full_name || 'Sin Nombre' }}</span>
                    <span class="text-xs text-slate-500 block">Tel: {{ c.phone_number || 'No registrado' }}</span>
                  </div>
                  <span class="badge badge-neutral text-xs">ID #{{ c.remote_auth_id }}</span>
                </button>
              </div>

              <div v-if="customer" class="mt-3 p-3 bg-green-50 border border-green-200 rounded-xl flex items-center gap-3">
                <div class="bg-green-500 text-white rounded-full p-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold text-green-800 truncate">{{ customer.full_name || 'Sin Nombre' }}</p>
                  <p class="text-xs text-green-600">ID #{{ customer.remote_auth_id }} - {{ customer.custom_role }}</p>
                </div>
                <button @click="clearCustomer" class="btn btn-xs btn-ghost btn-circle text-slate-400">×</button>
              </div>
            </div>

            <!-- Email de Recibo -->
            <div class="form-control w-full mb-4">
              <label class="label">
                <span class="label-text font-bold text-slate-700">Correo para Recibo</span>
              </label>
              <input 
                v-model="customerEmail" 
                type="email" 
                placeholder="correo@ejemplo.com" 
                class="input input-bordered w-full font-semibold" 
              />
            </div>

            <!-- Método de Pago -->
            <div class="form-control w-full mb-4">
              <label class="label">
                <span class="label-text font-bold text-slate-700">Método de Pago</span>
              </label>
              <select v-model="paymentMethod" class="select select-bordered w-full font-semibold">
                <option v-if="vendorMode !== 'REMOTE'" value="CASH">💵 Efectivo (Cierre Inmediato)</option>
                <option v-if="vendorMode !== 'REMOTE' && !isOffline" value="CARD">💳 Tarjeta (Terminal Física)</option>
                <option v-if="!isOffline" value="BANK_TRANSFER">📲 Transferencia Bancaria (Referenciada)</option>
                <option v-if="!isOffline" value="OXXO">🏪 OXXO Referenciado</option>
              </select>
            </div>

            <!-- Descuento Directo (Solo ADMIN o FRANCHISEE) -->
            <div v-if="(userRole === 'ADMIN' || userRole === 'FRANCHISEE') && !isOffline" class="form-control w-full mb-6">
              <label class="label">
                <span class="label-text font-bold text-slate-700">Descuento Directo ($)</span>
              </label>
              <input 
                v-model.number="discountAmount" 
                type="number" 
                min="0" 
                :max="subtotalAmount"
                placeholder="0.00" 
                class="input input-bordered w-full font-semibold" 
              />
            </div>

            <!-- Resumen de Costos -->
            <div class="space-y-3 mb-8">
              <div class="flex justify-between text-slate-600 text-sm">
                <span>Subtotal:</span>
                <span class="font-bold text-slate-800">${{ subtotalAmount.toFixed(2) }}</span>
              </div>
              <div v-if="discountAmount > 0" class="flex justify-between text-error text-sm">
                <span>Descuento:</span>
                <span class="font-bold">-${{ discountAmount.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-slate-600 text-sm">
                <span>Impuestos:</span>
                <span class="font-bold text-slate-800">${{ taxAmount.toFixed(2) }}</span>
              </div>
              <div class="divider my-0"></div>
              <div class="flex justify-between items-center text-xl">
                <span class="font-bold text-slate-800">Total:</span>
                <span class="font-black text-primary">${{ totalAmount.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Botón Acción -->
            <button 
              class="btn btn-primary btn-block h-16 text-lg animate-hover" 
              :disabled="cart.length === 0 || !customer || processing"
              @click="processSale"
            >
              <span v-if="processing" class="loading loading-spinner"></span>
              {{ isOffline ? 'Registrar Pago Offline (Efectivo)' : 'Registrar Venta Directa' }}
            </button>
            <p v-if="!customer" class="text-xs text-center text-slate-400 mt-4 italic">Debes seleccionar o buscar un cliente primero.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE CIERRE DE CAJA (ARQUEO) -->
    <div v-if="showCloseModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-96 bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <h3 class="text-xl font-bold text-slate-800">Cierre de Caja y Arqueo</h3>
          <p class="text-slate-500 text-sm mb-4">Por favor cuenta el dinero en efectivo de la caja física e ingrésalo a continuación.</p>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text font-bold">Efectivo Contado Real</span>
            </label>
            <input v-model="closingBalanceInput" type="number" placeholder="$0.00" class="input input-bordered text-center text-2xl font-bold" />
          </div>

          <div class="flex gap-3 mt-6">
            <button class="btn btn-outline flex-1" @click="showCloseModal = false">Cancelar</button>
            <button class="btn btn-error flex-1" @click="confirmCloseSession" :disabled="closingSession">
              <span v-if="closingSession" class="loading loading-spinner"></span>
              Cerrar Turno
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE RESUMEN DE CIERRE -->
    <div v-if="showSummaryModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-[450px] bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <div class="text-center mb-4">
            <div class="bg-red-100 text-red-600 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-800">Turno Cerrado Correctamente</h3>
            <p class="text-xs text-slate-400">ID de Sesión: #{{ closeResult?.session_id }}</p>
          </div>

          <div class="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-100 text-sm">
            <div class="flex justify-between">
              <span class="text-slate-500">Saldo Inicial:</span>
              <span class="font-bold text-slate-700">${{ parseFloat(closeResult?.opening_balance).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Ventas en el Turno:</span>
              <span class="font-bold text-slate-700">${{ parseFloat(closeResult?.total_sales_amount).toFixed(2) }}</span>
            </div>
            <div class="divider my-0"></div>
            <div class="flex justify-between font-bold text-slate-800">
              <span class="text-slate-500">Esperado en Caja:</span>
              <span>${{ parseFloat(closeResult?.expected_closing_balance).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between font-bold text-slate-800">
              <span class="text-slate-500">Reportado Real:</span>
              <span>${{ parseFloat(closeResult?.closing_balance).toFixed(2) }}</span>
            </div>
            <div class="divider my-0"></div>
            <div class="flex justify-between items-center">
              <span class="text-slate-500 font-bold">Diferencia / Arqueo:</span>
              <span class="font-black p-2 rounded-lg text-xs" :class="closeResult?.difference >= 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                {{ closeResult?.difference >= 0 ? '+' : '' }}${{ parseFloat(closeResult?.difference).toFixed(2) }}
              </span>
            </div>
          </div>

          <button class="btn btn-primary btn-block mt-6" @click="closeSummaryModal">Entendido</button>
        </div>
      </div>
    </div>

    <!-- MODAL DE PAGO WHATSAPP REMOTO -->
    <div v-if="showWhatsappModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in">
      <div class="card w-[450px] bg-white shadow-2xl border border-slate-200 animate-slide-up">
        <div class="card-body">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <span class="text-green-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.724-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.725 1.45 5.515.003 10.003-4.484 10.006-9.997.002-2.67-1.037-5.18-2.927-7.072C16.565 1.642 14.062.603 11.39.601 5.87.601 1.38 5.087 1.378 10.601c-.001 1.705.474 3.327 1.377 4.728l-.994 3.63 3.731-.978-.172-.25c.003.001.003.001.002 0z"/>
              </svg>
            </span>
            {{ paymentMethod === 'OXXO' ? 'Referencia OXXO Generada' : 'Venta Registrada Exitosamente' }}
          </h3>
          <p class="text-slate-500 text-sm mb-4">Copia el siguiente mensaje y compártelo con el cliente por WhatsApp para completar el pago remoto:</p>
          
          <div class="relative bg-slate-900 text-slate-300 p-4 rounded-xl text-sm font-mono whitespace-pre-wrap border border-slate-800 max-h-48 overflow-y-auto">
            {{ whatsappMessage }}
          </div>

          <div class="flex gap-3 mt-6">
            <button class="btn btn-outline flex-1" @click="showWhatsappModal = false">Cerrar</button>
            <button class="btn btn-success text-white flex-1 flex items-center gap-2" @click="copyWhatsappMessage">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
              </svg>
              Copiar Mensaje
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DE ÉXITO DE VENTA POS PREMIUM (IMPRESIÓN, CORREO, FACTURACIÓN) -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 animate-fade-in p-4 overflow-y-auto">
      <div class="card w-full max-w-lg bg-white shadow-2xl border border-slate-200 animate-slide-up my-auto">
        <div class="card-body p-6">
          <div class="text-center mb-6">
            <div class="bg-green-100 text-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-black text-slate-800">
              {{ successOrder?.isOffline ? 'Cobro Registrado (Offline)' : 'Cobro Completado con Éxito' }}
            </h3>
            <p class="text-xs text-slate-400 mt-1">Orden ID: {{ successOrder?.id }}</p>
          </div>

          <!-- Desglose breve -->
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 text-sm space-y-3 mb-6">
            <div class="flex justify-between">
              <span class="text-slate-500 font-medium">Cliente:</span>
              <span class="font-bold text-slate-800">{{ successOrder?.isOffline ? successOrder?.customer_name : (customer?.full_name || 'Mostrador') }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500 font-medium">Método de Pago:</span>
              <span class="badge badge-success font-black text-white text-xs">
                {{ successOrder?.isOffline ? 'CASH (Offline)' : successOrder?.payment?.payment_method || 'CASH' }}
              </span>
            </div>
            <div class="divider my-1"></div>
            <div class="flex justify-between font-bold text-base text-slate-800">
              <span>Total Pagado:</span>
              <span class="text-primary font-black">${{ parseFloat(successOrder?.total_amount).toFixed(2) }} MXN</span>
            </div>

            <!-- Seriales Digitales Asignados -->
            <div v-if="hasDigitalProducts" class="mt-4 pt-3 border-t border-slate-200">
              <span class="text-xs font-bold text-slate-500 uppercase tracking-wide block mb-2">Claves de Invitación Digital:</span>
              <div class="space-y-2">
                <div v-for="item in successOrder.items" :key="item.product">
                  <div v-if="item.serial_keys && item.serial_keys.length > 0" class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-xs font-bold text-slate-700 block mb-1">
                      {{ getProductNameById(item.product) }}:
                    </span>
                    <div class="flex flex-wrap gap-1.5">
                      <span v-for="key in item.serial_keys" :key="key" class="bg-slate-100 text-slate-800 border border-slate-200 font-mono font-bold text-xs px-2.5 py-1 rounded">
                        {{ key }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Reenvío de Recibo por Correo -->
          <div v-if="!successOrder?.isOffline" class="border-t border-slate-100 pt-4 mb-6">
            <h4 class="font-bold text-slate-800 text-sm mb-2 flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Reenviar Recibo Electrónico
            </h4>
            <div class="join w-full">
              <input 
                v-model="emailResendInput" 
                type="email" 
                placeholder="correo@alternativo.com" 
                class="input input-sm input-bordered join-item w-full"
              />
              <button 
                class="btn btn-sm btn-indigo join-item text-white bg-indigo-600 hover:bg-indigo-700" 
                @click="resendReceipt"
                :disabled="emailSending || !emailResendInput"
              >
                <span v-if="emailSending" class="loading loading-spinner loading-xs"></span>
                Enviar
              </button>
            </div>
          </div>

          <!-- Sección de Facturación CFDI 4.0 -->
          <div v-if="!successOrder?.isOffline" class="border-t border-slate-100 pt-4 mb-6">
            <div class="flex justify-between items-center mb-3">
              <h4 class="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Facturación SAT CFDI 4.0 (México)
              </h4>
              <button 
                v-if="!showCFDIForm && !billingInvoice"
                class="btn btn-xs btn-outline btn-primary"
                @click="showCFDIForm = true"
              >
                Solicitar Factura
              </button>
            </div>

            <!-- Formulario de Factura -->
            <div v-if="showCFDIForm" class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
              <div class="grid grid-cols-2 gap-3">
                <div class="form-control">
                  <label class="label py-1"><span class="label-text text-[11px] font-bold text-slate-600">RFC</span></label>
                  <input v-model="billingRFC" type="text" placeholder="XAXX010101000" class="input input-xs input-bordered font-mono font-bold uppercase" />
                </div>
                <div class="form-control">
                  <label class="label py-1"><span class="label-text text-[11px] font-bold text-slate-600">Código Postal (CP)</span></label>
                  <input v-model="billingCP" type="text" placeholder="00000" class="input input-xs input-bordered font-mono" />
                </div>
              </div>
              <div class="form-control">
                <label class="label py-1"><span class="label-text text-[11px] font-bold text-slate-600">Razón Social</span></label>
                <input v-model="billingRazonSocial" type="text" placeholder="PÚBLICO GENERAL" class="input input-xs input-bordered" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div class="form-control">
                  <label class="label py-1"><span class="label-text text-[11px] font-bold text-slate-600">Régimen Fiscal</span></label>
                  <select v-model="billingRegimen" class="select select-xs select-bordered font-medium">
                    <option value="601">601 - General de Ley Personas Morales</option>
                    <option value="605">605 - Sueldos y Salarios</option>
                    <option value="616">616 - Sin obligaciones fiscales</option>
                    <option value="626">626 - Régimen Simplificado de Confianza (RESICO)</option>
                  </select>
                </div>
                <div class="form-control">
                  <label class="label py-1"><span class="label-text text-[11px] font-bold text-slate-600">Uso de CFDI</span></label>
                  <select v-model="billingUso" class="select select-xs select-bordered font-medium">
                    <option value="G03">G03 - Gastos en general</option>
                    <option value="D01">D01 - Honorarios médicos</option>
                    <option value="S01">S01 - Sin efectos fiscales</option>
                    <option value="CP01">CP01 - Pagos</option>
                  </select>
                </div>
              </div>
              <div class="flex gap-2 pt-2 justify-end">
                <button class="btn btn-xs btn-ghost" @click="showCFDIForm = false" :disabled="billingLoading">Cancelar</button>
                <button class="btn btn-xs btn-primary text-white" @click="submitCFDI" :disabled="billingLoading">
                  <span v-if="billingLoading" class="loading loading-spinner loading-xs"></span>
                  Timbrar Factura
                </button>
              </div>
            </div>

            <!-- Información de Factura Timbrada -->
            <div v-if="billingInvoice" class="bg-indigo-50 border border-indigo-200 p-4 rounded-xl space-y-3">
              <div class="flex items-center gap-2 text-indigo-800">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="font-bold text-sm">CFDI 4.0 Timbrado Exitosamente</span>
              </div>
              <div class="text-xs text-indigo-700 font-mono space-y-1 bg-white p-2.5 rounded-lg border border-indigo-100">
                <p><span class="font-bold">RFC:</span> {{ billingInvoice.rfc }}</p>
                <p><span class="font-bold">UUID:</span> {{ billingInvoice.uuid }}</p>
              </div>
              <div class="flex gap-2">
                <a :href="billingInvoice.xml_url" target="_blank" download class="btn btn-xs bg-indigo-600 hover:bg-indigo-700 text-white border-0 flex-1">
                  📥 Descargar XML
                </a>
                <a :href="billingInvoice.pdf_url" target="_blank" download class="btn btn-xs bg-indigo-600 hover:bg-indigo-700 text-white border-0 flex-1">
                  📥 Descargar PDF
                </a>
              </div>
            </div>
          </div>

          <!-- Botones de Acción Principales -->
          <div class="flex flex-col sm:flex-row gap-3 border-t border-slate-100 pt-5 mt-4">
            <button 
              class="btn btn-neutral flex-1 h-12 text-sm flex items-center justify-center gap-2 animate-hover"
              @click="handlePrint"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-3a2 2 0 00-2-2H9a2 2 0 00-2 2v3a2 2 0 002 2zm5-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h5z" />
              </svg>
              Imprimir Ticket
            </button>
            <button 
              class="btn btn-primary flex-1 h-12 text-sm text-white animate-hover" 
              @click="closeSuccessModal"
            >
              Nueva Venta
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useToast } from 'vue-toastification';
import { catalogService } from '@/modules/ecommerce/services/catalogService';
import { crmService } from '@/modules/workspace/services/crmService';
import { orderService } from '@/modules/ecommerce/services/orderService';
import { profileService } from '@/modules/dashboard/services/profileService';

const toast = useToast();

const products = ref([]);
const loadingProducts = ref(true);

const searchQuery = ref('');
const cart = ref([]);

const customerSearchId = ref('');
const customer = ref(null);
const customerEmail = ref('');
const matchingCustomers = ref([]);
const searching = ref(false);

const processing = ref(false);

// Conexión y Offline
const isOffline = ref(!navigator.onLine);
const syncingQueue = ref(false);
const offlineQueueLength = ref(0);

// Perfil y Tienda
const vendorMode = ref('REMOTE');
const assignedStore = ref(null);
const activeSession = ref(null);
const openingBalance = ref(0);
const loadingSession = ref(false);
const userRole = ref('');

// Comisiones
const totalCommissions = ref(0);

// Descuentos y totales
const discountAmount = ref(0);

// Control de Modales
const showCloseModal = ref(false);
const showSummaryModal = ref(false);
const showWhatsappModal = ref(false);

const closingBalanceInput = ref(0);
const closingSession = ref(false);
const closeResult = ref(null);
const whatsappMessage = ref('');
const paymentMethod = ref('CASH');

// Modal de éxito y sus campos
const showSuccessModal = ref(false);
const successOrder = ref(null);
const emailResendInput = ref('');
const emailSending = ref(false);

// Facturación
const showCFDIForm = ref(false);
const billingRFC = ref('');
const billingRazonSocial = ref('');
const billingCP = ref('');
const billingRegimen = ref('601');
const billingUso = ref('G03');
const billingInvoice = ref(null);
const billingLoading = ref(false);

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value;
  const q = searchQuery.value.toLowerCase();
  return products.value.filter(p => 
    p.name.toLowerCase().includes(q) || 
    (p.sku && p.sku.toLowerCase().includes(q))
  );
});

const subtotalAmount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0);
});

const taxAmount = computed(() => {
  return cart.value.reduce((sum, item) => {
    const rate = parseFloat(item.product.tax_rate) || 0;
    return sum + (item.price * item.quantity) * rate;
  }, 0);
});

const totalAmount = computed(() => {
  const tot = subtotalAmount.value - discountAmount.value + taxAmount.value;
  return tot > 0 ? tot : 0;
});

const hasDigitalProducts = computed(() => {
  if (!successOrder.value || !successOrder.value.items) return false;
  return successOrder.value.items.some(item => {
    const prod = products.value.find(p => p.id === item.product);
    return prod && !prod.is_physical;
  });
});

// Watchers para validar limites de descuento
watch(subtotalAmount, (newSubtotal) => {
  if (discountAmount.value > newSubtotal) {
    discountAmount.value = newSubtotal;
  }
});

watch(discountAmount, (newDiscount) => {
  if (newDiscount < 0) {
    discountAmount.value = 0;
  } else if (newDiscount > subtotalAmount.value) {
    discountAmount.value = subtotalAmount.value;
  }
});

// Listener de estado de conexión
const updateOnlineStatus = () => {
  isOffline.value = !navigator.onLine;
  if (!isOffline.value) {
    syncOfflineQueue();
  } else {
    // Si pasa a offline, forzamos método de pago CASH
    paymentMethod.value = 'CASH';
    toast.warning('Te has quedado sin conexión. Los cobros se limitan a EFECTIVO.');
  }
};

const updateOfflineQueueLength = () => {
  const queue = JSON.parse(localStorage.getItem('pos_offline_queue') || '[]');
  offlineQueueLength.value = queue.length;
};

const addToCart = (product) => {
  const existing = cart.value.find(item => item.product.id === product.id);
  if (existing) {
    existing.quantity++;
  } else {
    cart.value.push({
      product,
      quantity: 1,
      price: parseFloat(product.base_price)
    });
  }
  toast.success(`Agregado al carrito: ${product.name}`);
};

const incrementQty = (item) => {
  item.quantity++;
};

const decrementQty = (item) => {
  if (item.quantity > 1) {
    item.quantity--;
  } else {
    removeFromCart(item);
  }
};

const removeFromCart = (item) => {
  cart.value = cart.value.filter(i => i.product.id !== item.product.id);
  toast.info(`Quitado del carrito: ${item.product.name}`);
};

const selectPublicCustomer = () => {
  customerSearchId.value = '';
  customer.value = {
    remote_auth_id: 1,
    full_name: 'Público General',
    custom_role: 'CLIENT',
    email: ''
  };
  customerEmail.value = '';
  matchingCustomers.value = [];
  toast.success('Cliente Mostrador (Público General) seleccionado.');
};

const clearCustomer = () => {
  customer.value = null;
  customerSearchId.value = '';
  customerEmail.value = '';
  matchingCustomers.value = [];
};

const initProfileData = async () => {
  if (isOffline.value) {
    // Modo offline básico
    vendorMode.value = 'PHYSICAL';
    userRole.value = 'VENDOR';
    paymentMethod.value = 'CASH';
    return;
  }

  try {
    const resProfile = await profileService.fetchMyProfile();
    vendorMode.value = resProfile.data.vendor_mode;
    userRole.value = resProfile.data.custom_role;
    
    // Configurar método de pago inicial por modo del vendedor
    paymentMethod.value = resProfile.data.vendor_mode === 'PHYSICAL' ? 'CASH' : 'BANK_TRANSFER';
    
    // Si tiene tienda asignada, cargar sus datos
    if (resProfile.data.assigned_store) {
      const storesRes = await crmService.fetchAllStores();
      assignedStore.value = storesRes.data.find(s => s.id === resProfile.data.assigned_store);
    }

    // Cargar comisiones
    const commRes = await crmService.fetchMyCommissions();
    totalCommissions.value = commRes.data.reduce((acc, curr) => acc + parseFloat(curr.amount), 0);

    // Cargar sesión activa
    const sessionRes = await crmService.fetchMySessions();
    activeSession.value = sessionRes.data.find(s => s.is_open);

  } catch (e) {
    console.error(e);
  }
};

const startShift = async () => {
  if (isOffline.value) {
    toast.error('No puedes abrir turno de caja sin conexión.');
    return;
  }
  if (!assignedStore.value) {
    toast.error('No tienes una sucursal asignada. Contacta al Admin.');
    return;
  }
  loadingSession.value = true;
  try {
    const res = await crmService.openCashSession(openingBalance.value, assignedStore.value.id);
    activeSession.value = res.data;
    toast.success('Turno abierto correctamente. ¡Buena venta!');
  } catch (e) {
    toast.error('Error al abrir turno.');
  } finally {
    loadingSession.value = false;
  }
};

const closeSession = () => {
  closingBalanceInput.value = 0;
  showCloseModal.value = true;
};

const confirmCloseSession = async () => {
  if (!activeSession.value) return;
  closingSession.value = true;
  try {
    const res = await crmService.closeCashSession(activeSession.value.id, closingBalanceInput.value);
    closeResult.value = res.data;
    showCloseModal.value = false;
    showSummaryModal.value = true;
    toast.success('Turno cerrado con éxito.');
  } catch (error) {
    toast.error('Error al cerrar el turno.');
  } finally {
    closingSession.value = false;
  }
};

const closeSummaryModal = () => {
  showSummaryModal.value = false;
  activeSession.value = null;
  initProfileData();
};

const copyWhatsappMessage = async () => {
  try {
    await navigator.clipboard.writeText(whatsappMessage.value);
    toast.success('¡Mensaje copiado al portapapeles!');
    showWhatsappModal.value = false;
  } catch (err) {
    toast.error('No se pudo copiar el mensaje automáticamente.');
  }
};

const fetchProducts = async () => {
  loadingProducts.value = true;
  if (isOffline.value) {
    const cached = localStorage.getItem('pos_cached_products');
    if (cached) {
      products.value = JSON.parse(cached);
      toast.info('Catálogo cargado desde la memoria caché local.');
    } else {
      toast.error('Catálogo no disponible. Conéctate a internet para cargarlo la primera vez.');
    }
    loadingProducts.value = false;
    return;
  }

  try {
    const res = await catalogService.fetchProducts();
    products.value = res.data;
    localStorage.setItem('pos_cached_products', JSON.stringify(res.data));
  } catch (e) {
    toast.error('Error al cargar productos');
  } finally {
    loadingProducts.value = false;
  }
};

const selectCustomer = (c) => {
  customer.value = c;
  customerEmail.value = c.email || '';
  customerSearchId.value = c.full_name || `${c.remote_auth_id}`;
  matchingCustomers.value = [];
  toast.success('Cliente seleccionado');
};

const findCustomer = async () => {
  if (!customerSearchId.value) return;
  searching.value = true;
  customer.value = null;
  customerEmail.value = '';
  matchingCustomers.value = [];
  try {
    const res = await crmService.searchProfile(customerSearchId.value);
    const results = res.data;
    if (Array.isArray(results)) {
      if (results.length === 0) {
        toast.error('Ningún cliente coincide con la búsqueda');
      } else if (results.length === 1) {
        selectCustomer(results[0]);
      } else {
        matchingCustomers.value = results;
        toast.info(`${results.length} clientes encontrados`);
      }
    } else if (results && typeof results === 'object') {
      selectCustomer(results);
    }
  } catch (e) {
    toast.error('Error al buscar cliente');
  } finally {
    searching.value = false;
  }
};

// Guardar venta en local storage (offline)
const queueOfflineSale = () => {
  const tempOrderId = 'OFF-' + Date.now();
  const offlineOrder = {
    id: tempOrderId,
    user: customer.value.remote_auth_id,
    customer_name: customer.value.full_name,
    customer_email: customerEmail.value,
    subtotal_amount: subtotalAmount.value,
    discount_amount: discountAmount.value,
    tax_amount: taxAmount.value,
    total_amount: totalAmount.value,
    payment_method: 'CASH',
    items: cart.value.map(item => ({
      product: item.product.id,
      quantity: item.quantity,
      price_at_sale: parseFloat(item.price),
      serial_keys: [] // Offline no podemos asignar llaves digitales
    })),
    created_at: new Date().toISOString(),
    isOffline: true
  };

  const queue = JSON.parse(localStorage.getItem('pos_offline_queue') || '[]');
  queue.push(offlineOrder);
  localStorage.setItem('pos_offline_queue', JSON.stringify(queue));
  updateOfflineQueueLength();

  successOrder.value = offlineOrder;
  showSuccessModal.value = true;
  
  toast.success('Cobro en efectivo guardado localmente (Offline).');

  // Limpiar carrito
  cart.value = [];
  discountAmount.value = 0;
  customer.value = null;
  customerSearchId.value = '';
  customerEmail.value = '';
};

// Sincronizar cola offline al volver a internet
const syncOfflineQueue = async () => {
  if (isOffline.value || syncingQueue.value) return;
  const queue = JSON.parse(localStorage.getItem('pos_offline_queue') || '[]');
  if (queue.length === 0) return;

  syncingQueue.value = true;
  let successCount = 0;

  for (let i = 0; i < queue.length; i++) {
    const offlineOrder = queue[i];
    try {
      // 1. Crear orden
      const payload = {
        user: offlineOrder.user,
        subtotal_amount: offlineOrder.subtotal_amount.toFixed(2),
        discount_amount: offlineOrder.discount_amount.toFixed(2),
        tax_amount: offlineOrder.tax_amount.toFixed(2),
        total_amount: offlineOrder.total_amount.toFixed(2),
        status: 'PENDING',
        customer_email: offlineOrder.customer_email || null,
        items: offlineOrder.items.map(item => ({
          product: item.product,
          quantity: item.quantity,
          price_at_sale: item.price_at_sale.toFixed(2)
        }))
      };

      const orderRes = await orderService.createOrder(payload);
      const serverOrderId = orderRes.data.id;

      // 2. Completar POS
      await orderService.completePosOrder(serverOrderId, 'CASH', offlineOrder.customer_email || null);
      successCount++;
    } catch (e) {
      console.error('Error sincronizando orden offline:', offlineOrder, e);
      toast.error(`No se pudo sincronizar la venta local con fecha ${new Date(offlineOrder.created_at).toLocaleDateString()}. Queda retenida.`);
    }
  }

  // Filtrar de la cola las que se sincronizaron con éxito (removiendo las primeras N exitosas)
  // En caso de que hayan fallado en orden aleatorio, lo más seguro es recrear la cola removiendo las exitosas.
  // Como lo hicimos de forma secuencial, removemos las primeras exitosas si no falló a la mitad.
  // Por simplicidad, si todas fueron exitosas vaciamos, de lo contrario dejamos solo las fallidas.
  const remainingQueue = JSON.parse(localStorage.getItem('pos_offline_queue') || '[]');
  // Si todas salieron bien:
  if (successCount === remainingQueue.length) {
    localStorage.setItem('pos_offline_queue', '[]');
  } else {
    // Quitar las exitosas (las primeras N)
    remainingQueue.splice(0, successCount);
    localStorage.setItem('pos_offline_queue', JSON.stringify(remainingQueue));
  }

  updateOfflineQueueLength();
  syncingQueue.value = false;
  if (successCount > 0) {
    toast.success(`Sincronización exitosa: ${successCount} ventas enviadas al servidor.`);
    initProfileData();
  }
};

const processSale = async () => {
  if (cart.value.length === 0 || !customer.value) return;

  if (isOffline.value) {
    queueOfflineSale();
    return;
  }

  processing.value = true;
  try {
    // 1. Crear la orden en estado PENDING con múltiples ítems
    const payload = {
      user: customer.value.remote_auth_id,
      subtotal_amount: subtotalAmount.value.toFixed(2),
      discount_amount: discountAmount.value.toFixed(2),
      tax_amount: taxAmount.value.toFixed(2),
      total_amount: totalAmount.value.toFixed(2),
      status: 'PENDING',
      customer_email: customerEmail.value || null,
      items: cart.value.map(item => ({
        product: item.product.id,
        quantity: item.quantity,
        price_at_sale: parseFloat(item.price).toFixed(2)
      }))
    };

    const orderRes = await orderService.createOrder(payload);
    const orderId = orderRes.data.id;

    // 2. Determinar flujo según el método de pago seleccionado
    if (paymentMethod.value === 'CASH' || paymentMethod.value === 'CARD') {
      // Completar cobro presencial de inmediato enviando email de recibo si se especificó
      const completeRes = await orderService.completePosOrder(orderId, paymentMethod.value, customerEmail.value || null);
      
      // La respuesta exitosa contiene la orden con seriales
      successOrder.value = completeRes.data.order;
      emailResendInput.value = customerEmail.value;
      showSuccessModal.value = true;

      toast.success(`Venta completada con éxito en ${paymentMethod.value === 'CASH' ? 'Efectivo' : 'Tarjeta'}`);
    } else if (paymentMethod.value === 'OXXO') {
      // Generar mensaje OXXO referenciado
      const referenceNumber = `73812903${String(orderId).padStart(6, '0')}`;
      const clientName = customer.value.full_name || 'Cliente';
      
      const itemsList = cart.value.map(item => `• ${item.quantity}x ${item.product.name} ($${parseFloat(item.price).toFixed(2)} c/u)`).join('\n');
      const amount = totalAmount.value.toFixed(2);
      
      whatsappMessage.value = `¡Hola, ${clientName}! Se ha registrado tu orden:\n${itemsList}\n\nSubtotal: $${subtotalAmount.value.toFixed(2)}\nDescuento: -$${discountAmount.value.toFixed(2)}\nImpuestos: $${taxAmount.value.toFixed(2)}\nTotal a pagar: $${amount} MXN\n\nPara completar tu pago referenciado de OXXO, acude a tu sucursal OXXO más cercana y proporciona el número de referencia:\n👉 ${referenceNumber}\n\nCompártenos el ticket de pago una vez realizado. ¡Muchas gracias!`;
      showWhatsappModal.value = true;
      toast.success('Orden registrada. En espera de pago por OXXO.');
    } else {
      // Transferencia bancaria estándar
      const clientName = customer.value.full_name || 'Cliente';
      const itemsList = cart.value.map(item => `• ${item.quantity}x ${item.product.name} ($${parseFloat(item.price).toFixed(2)} c/u)`).join('\n');
      const amount = totalAmount.value.toFixed(2);
      
      whatsappMessage.value = `¡Hola, ${clientName}! Se ha registrado tu orden:\n${itemsList}\n\nSubtotal: $${subtotalAmount.value.toFixed(2)}\nDescuento: -$${discountAmount.value.toFixed(2)}\nImpuestos: $${taxAmount.value.toFixed(2)}\nTotal a pagar: $${amount} MXN\n\nPor favor realiza tu transferencia a la CLABE: 012180000000000000 de ECOSYS y compártenos tu comprobante por este medio. ¡Muchas gracias!`;
      showWhatsappModal.value = true;
      toast.success('Orden registrada. En espera de transferencia.');
    }

    // Limpiar campos de venta actual
    cart.value = [];
    discountAmount.value = 0;
    customer.value = null;
    customerSearchId.value = '';
    customerEmail.value = '';
    
    // Recargar comisiones y estado de caja
    initProfileData();
  } catch (e) {
    console.error(e);
    const errorMsg = e.response?.data?.error || e.response?.data?.message || 'Error al procesar la venta.';
    toast.error(errorMsg);
  } finally {
    processing.value = false;
  }
};

const getProductNameById = (id) => {
  const prod = products.value.find(p => p.id === id);
  return prod ? prod.name : `Producto #${id}`;
};

// Reenviar Recibo Manual
const resendReceipt = async () => {
  if (!successOrder.value || !emailResendInput.value) return;
  emailSending.value = true;
  try {
    await orderService.sendReceiptEmail(successOrder.value.id, emailResendInput.value);
    toast.success(`Recibo enviado exitosamente a ${emailResendInput.value}`);
  } catch (e) {
    toast.error('Error al enviar el recibo por correo.');
  } finally {
    emailSending.value = false;
  }
};

// Timbrar Factura CFDI 4.0
const submitCFDI = async () => {
  if (!successOrder.value) return;
  billingLoading.value = true;
  try {
    const payload = {
      rfc: billingRFC.value,
      razon_social: billingRazonSocial.value,
      codigo_postal: billingCP.value,
      regimen_fiscal: billingRegimen.value,
      uso_cfdi: billingUso.value
    };
    const res = await orderService.issueCFDI(successOrder.value.id, payload);
    billingInvoice.value = res.data.invoice;
    showCFDIForm.value = false;
    toast.success('Factura CFDI 4.0 generada correctamente.');
  } catch (e) {
    console.error(e);
    const errObj = e.response?.data || {};
    // Mostrar el primer error de validación
    const keys = Object.keys(errObj);
    if (keys.length > 0) {
      toast.error(errObj[keys[0]]);
    } else {
      toast.error('Error al generar la factura CFDI.');
    }
  } finally {
    billingLoading.value = false;
  }
};

// Cierre del modal de éxito
const closeSuccessModal = () => {
  showSuccessModal.value = false;
  successOrder.value = null;
  emailResendInput.value = '';
  showCFDIForm.value = false;
  billingInvoice.value = null;
  billingRFC.value = '';
  billingRazonSocial.value = '';
  billingCP.value = '';
};

// Imprimir Ticket Courier 80mm
const handlePrint = () => {
  if (!successOrder.value) return;
  
  const printWindow = window.open('', '_blank', 'width=350,height=600');
  const storeName = assignedStore.value ? assignedStore.value.name : 'ECOSYS CENTRAL';
  const storeAddress = assignedStore.value ? assignedStore.value.address : 'Calle Principal #123';
  
  // Recopilar items
  let itemsHtml = '';
  successOrder.value.items.forEach(item => {
    const prodName = getProductNameById(item.product);
    itemsHtml += `
      <tr>
        <td colspan="2" style="font-weight:bold; padding-top:6px;">${prodName}</td>
      </tr>
      <tr>
        <td style="font-size:11px;">${item.quantity}x $${parseFloat(item.price_at_sale).toFixed(2)}</td>
        <td style="text-align:right; font-size:11px;">$${(item.quantity * item.price_at_sale).toFixed(2)}</td>
      </tr>
    `;
    if (item.serial_keys && item.serial_keys.length > 0) {
      itemsHtml += `
        <tr>
          <td colspan="2" style="font-size:9px; font-family:monospace; padding-left:10px; color:#555; word-break:break-all;">
            Claves:<br>
            ${item.serial_keys.map(k => `&nbsp;- ${k}`).join('<br>')}
          </td>
        </tr>
      `;
    }
  });

  const formattedDate = new Date(successOrder.value.created_at).toLocaleString('es-MX');

  printWindow.document.write(`
    <html>
      <head>
        <title>Ticket #${successOrder.value.id}</title>
        <style>
          @page { margin: 0; }
          body {
            font-family: 'Courier New', Courier, monospace;
            width: 72mm;
            margin: 0 auto;
            padding: 10px;
            font-size: 11px;
            color: #000;
            line-height: 1.2;
          }
          .text-center { text-align: center; }
          .header { margin-bottom: 12px; border-bottom: 1px dashed #000; padding-bottom: 8px; }
          .header h2 { margin: 0; font-size: 15px; font-weight: bold; }
          .header p { margin: 2px 0; font-size: 9px; }
          .table { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
          .table td { padding: 2px 0; vertical-align: top; }
          .totals { border-top: 1px dashed #000; padding-top: 5px; margin-bottom: 12px; }
          .totals table { width: 100%; }
          .totals td { padding: 2px 0; }
          .footer { border-top: 1px dashed #000; padding-top: 8px; font-size: 9px; margin-top: 15px; }
        </style>
      </head>
      <body>
        <div class="header text-center">
          <h2>ECOSYS</h2>
          <p>${storeName}</p>
          <p>${storeAddress}</p>
          <p>----------------------------</p>
          <p>Ticket de Venta: #${successOrder.value.id}</p>
          <p>Fecha: ${formattedDate}</p>
        </div>
        <table class="table">
          ${itemsHtml}
        </table>
        <div class="totals">
          <table>
            <tr>
              <td>Subtotal:</td>
              <td style="text-align:right;">$${parseFloat(successOrder.value.subtotal_amount).toFixed(2)}</td>
            </tr>
            <tr>
              <td>Descuento:</td>
              <td style="text-align:right;">-$${parseFloat(successOrder.value.discount_amount).toFixed(2)}</td>
            </tr>
            <tr>
              <td>Impuestos:</td>
              <td style="text-align:right;">$${parseFloat(successOrder.value.tax_amount).toFixed(2)}</td>
            </tr>
            <tr style="font-weight:bold; font-size:12px;">
              <td>TOTAL:</td>
              <td style="text-align:right;">$${parseFloat(successOrder.value.total_amount).toFixed(2)}</td>
            </tr>
          </table>
        </div>
        <div class="footer text-center">
          <p>¡Gracias por tu compra!</p>
          <p>Este recibo no es deducible.</p>
          <p>ECOSYS 2026</p>
        </div>
        \x3cscript\x3e
          window.onload = function() {
            window.print();
            setTimeout(function() { window.close(); }, 500);
          }
        \x3c/script\x3e
      </body>
    </html>
  `);
  printWindow.document.close();
};

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOfflineQueueLength();
  initProfileData();
  fetchProducts();
  syncOfflineQueue();
});

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus);
  window.removeEventListener('offline', updateOnlineStatus);
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.25s ease-out forwards;
}
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-hover {
  transition: all 0.2s ease;
}
.animate-hover:hover {
  transform: translateY(-1px);
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
