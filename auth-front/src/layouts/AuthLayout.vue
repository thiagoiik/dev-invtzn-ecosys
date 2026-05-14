<template>
  <div class="min-h-screen bg-slate-100 flex flex-col justify-center items-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
      <h2 class="text-3xl font-extrabold text-slate-900 tracking-tight">
        INVITAZYON
      </h2>
      <p class="mt-2 text-sm text-slate-600">
        Tu plataforma de invitaciones digitales
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-xl sm:rounded-xl sm:px-10 border border-slate-200">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
// AuthLayout: Contenedor minimalista para Login y Registro
</script>

<style scoped>
/* Tailwind maneja los estilos aquí */
</style>
