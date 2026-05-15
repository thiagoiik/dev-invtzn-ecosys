<template>
  <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
    <h4 class="text-xs font-black uppercase text-slate-400 mb-3 tracking-widest">Gestión de Billetera</h4>
    
    <div class="flex items-center justify-between mb-4">
      <span class="text-sm font-medium text-slate-600">Saldo Actual:</span>
      <span class="text-lg font-black text-slate-900">${{ currentBalance }}</span>
    </div>

    <div class="space-y-3">
      <div class="join w-full">
        <input 
          v-model="amount" 
          type="number" 
          placeholder="Monto ($)" 
          class="input input-bordered join-item w-full input-sm font-bold" 
        />
        <select v-model="type" class="select select-bordered join-item select-sm">
          <option value="ADD">Abonar</option>
          <option value="SUB">Descontar</option>
        </select>
      </div>

      <select v-model="reason" class="select select-bordered w-full select-sm">
        <option value="BANK_DEPOSIT">Depósito Bancario</option>
        <option value="REFUND">Reembolso / Ajuste</option>
        <option value="PURCHASE">Cargo Directo</option>
      </select>

      <button 
        class="btn btn-primary btn-sm btn-block" 
        @click="handleTransaction"
        :disabled="loading || !amount"
      >
        <span v-if="loading" class="loading loading-spinner loading-xs"></span>
        Aplicar Transacción
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { crmService } from '@/modules/workspace/services/crmService';
import { useToast } from 'vue-toastification';

const props = defineProps(['profileId', 'currentBalance']);
const emit = defineEmits(['updated']);
const toast = useToast();

const amount = ref('');
const type = ref('ADD');
const reason = ref('BANK_DEPOSIT');
const loading = ref(false);

const handleTransaction = async () => {
  loading.value = true;
  try {
    const finalAmount = type.value === 'ADD' ? amount.value : -amount.value;
    await crmService.addWalletLog(props.profileId, finalAmount, reason.value, 'Ajuste manual desde CRM');
    toast.success('Billetera actualizada');
    amount.value = '';
    emit('updated');
  } catch (e) {
    toast.error('Error al actualizar billetera');
  } finally {
    loading.value = false;
  }
};
</script>
