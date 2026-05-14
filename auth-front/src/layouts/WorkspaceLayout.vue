<template>
  <div class="workspace-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="logo">ECOSYS ADMIN</div>
      <nav class="nav-menu">
        <router-link to="/workspace/crm" class="nav-item">👥 CRM & Clientes</router-link>
        <router-link to="/workspace/pos" class="nav-item">🛒 POS / Ventas</router-link>
        <router-link to="/dashboard" class="nav-item back-btn">⬅️ Volver a B2C</router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="topbar">
        <h2>Panel de Administración</h2>
        <div class="user-info">
          Staff ID: {{ authStore.user?.id || '...' }}
        </div>
      </header>
      
      <div class="content-area">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/modules/auth/store/auth';
const authStore = useAuthStore();
</script>

<style scoped>
.workspace-layout {
  display: flex;
  height: 100vh;
  background-color: #f1f5f9;
}
.sidebar {
  width: 250px;
  background: #0f172a;
  color: white;
  display: flex;
  flex-direction: column;
}
.logo {
  font-size: 1.5rem;
  font-weight: 800;
  padding: 1.5rem;
  border-bottom: 1px solid #1e293b;
  text-align: center;
  letter-spacing: 2px;
}
.nav-menu {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}
.nav-item {
  color: #94a3b8;
  text-decoration: none;
  padding: 1rem 1.5rem;
  font-weight: 500;
  transition: all 0.2s;
}
.nav-item:hover, .nav-item.router-link-active {
  background: #1e293b;
  color: white;
  border-left: 4px solid #3b82f6;
}
.back-btn {
  margin-top: auto;
  color: #ef4444;
}
.back-btn:hover {
  background: transparent;
  color: #f87171;
  border-left: none;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.topbar {
  background: white;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  border-bottom: 1px solid #e2e8f0;
}
.user-info {
  font-weight: bold;
  color: #475569;
}
.content-area {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
