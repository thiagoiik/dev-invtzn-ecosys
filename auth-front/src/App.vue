<template>
  <!-- App.vue ahora es solo un contenedor transparente. Los estilos se manejan en los Layouts. -->
  <router-view v-slot="{ Component }">
    <component :is="Component" />
  </router-view>
</template>

<script setup>
// Componente raíz limpio
</script>

<style>
/* Estilos base globales (si es necesario) */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #f8fafc; /* bg-slate-50 de Tailwind */
}
#app {
  width: 100%;
  height: 100%;
}
</style>