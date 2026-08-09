import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    // force a single copy of React (fixes "Invalid hook call / more than one copy of React")
    dedupe: ['react', 'react-dom'],
  },
})
