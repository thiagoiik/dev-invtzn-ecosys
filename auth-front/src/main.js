import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import Toast from "vue-toastification"; // Importación nueva
import "vue-toastification/dist/index.css"; // Estilos de la librería

import './assets/style.css'; // Estilos globales Tailwind + DaisyUI

import App from './App.vue';
import router from './core/router'; // <-- 1. Importamos el router

// 1. Inicializamos la aplicación
const app = createApp(App);

// 2. Creamos la instancia de Pinia
const pinia = createPinia();

// 3. Registramos el plugin ANTES de usar Pinia en la app
pinia.use(piniaPluginPersistedstate);

// 4. Inyectamos Pinia a la app
app.use(pinia);

// 5. Inyectamos el router
app.use(router); // <-- 2. REGISTRAR EL ROUTER ANTES DE MONTAR

// Agreggamos Toas para notificaciones
app.use(Toast, {
    // Configuración opcional por defecto
    position: "top-right",
    timeout: 3000,
    closeOnClick: true
});

// 6. Montamos la aplicación
app.mount('#app');