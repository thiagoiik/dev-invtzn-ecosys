import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Necesitas importar 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})