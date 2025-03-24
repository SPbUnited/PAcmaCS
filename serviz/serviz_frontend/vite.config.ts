import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  base: '/static/',
  build: {
    outDir: '../flask/static',
    emptyOutDir: true,
    // rollupOptions: {
    //   input: 'src/main.ts',
    //   output: {
    //     assetFileNames: '[name].[hash][extname]',
    //     entryFileNames: '[name].[hash].js',
    //   }
    // },
  },
})
