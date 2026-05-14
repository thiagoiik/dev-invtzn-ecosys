<template>
  <div class="builder-layout">
    <!-- Topbar simplificada solo para guardar -->
    <header class="builder-header">
      <div class="left-section">
        <router-link to="/dashboard" class="back-btn">⬅️ Salir</router-link>
        <span class="logo">ECOSYS BUILDER</span>
      </div>
      <div class="right-section">
        <slot name="actions"></slot>
      </div>
    </header>

    <!-- Área de trabajo -->
    <main class="workspace">
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
.builder-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background-color: #1e293b;
}
.builder-header {
  height: 60px;
  background-color: #0f172a;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  z-index: 10;
}
.left-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.back-btn {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 500;
}
.back-btn:hover {
  color: white;
}
.logo {
  font-weight: bold;
  letter-spacing: 2px;
  color: #38bdf8;
}
.workspace {
  flex: 1;
  display: flex;
  position: relative;
}
</style>
