<template>
  <div class="builder-layout">
    <!-- Topbar simplificada solo para guardar -->
    <header class="builder-header">
      <div class="left-section">
        <router-link to="/dashboard" class="back-btn flex items-center gap-1">
          <span>⬅️</span>
          <span class="hidden sm:inline">Salir</span>
        </router-link>
        <span class="logo text-xs sm:text-sm md:text-base">
          <span class="hidden md:inline">Diseño de  </span>Invitaciones
        </span>
      </div>
      <div class="center-section">
        <slot name="title"></slot>
      </div>
      <div class="right-section">
        <slot name="actions"></slot>
      </div>
    </header>


    <!-- Área de trabajo -->
    <main class="workspace">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.builder-layout {
  display: flex;
  flex-direction: column;
  height: 100dvh;
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
.right-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
.center-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 50%;
}
.workspace {

  flex: 1;
  display: flex;
  position: relative;
}

@media (max-width: 640px) {
  .builder-header {
    padding: 0 0.5rem;
  }
  .left-section {
    gap: 0.75rem;
  }
  .right-section {
    gap: 0.35rem;
  }
}
</style>
