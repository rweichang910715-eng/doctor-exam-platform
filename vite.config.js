import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Large source PDFs in the project root lock up the file watcher on Windows.
    watch: { ignored: ['**/*.pdf', '**/scripts/**'] },
  },
})
