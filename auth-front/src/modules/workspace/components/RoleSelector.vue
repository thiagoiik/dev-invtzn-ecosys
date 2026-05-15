<template>
  <div class="form-control w-full">
    <label class="label">
      <span class="label-text font-bold text-xs uppercase text-slate-500">Rol del Usuario</span>
    </label>
    <select 
      class="select select-bordered w-full font-bold" 
      :value="modelValue" 
      @change="$emit('update:modelValue', $event.target.value)"
      :disabled="loading"
    >
      <option value="CLIENT">Cliente (B2C)</option>
      <option value="VENDOR">Vendedor (POS)</option>
      <option value="ADMIN">Administrador (Full)</option>
    </select>
  </div>
</template>

<script setup>
defineProps(['modelValue', 'loading']);
defineEmits(['update:modelValue']);
</script>
