import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom', // Necesario para simular el navegador
    globals: true,        // Permite usar describe, it, expect sin importarlos cada vez
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});