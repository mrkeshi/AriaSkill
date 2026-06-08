import tailwindcss from "@tailwindcss/vite";
import Icons from 'unplugin-icons/vite'

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ["@/assets/css/main.css"],

  runtimeConfig: {
    privateHeaderKey: process.env.NUXT_PRIVATE_HEADER_KEY || '',
    public: {
      baseUrl:        process.env.NUXT_PUBLIC_BASE_URL     || 'http://127.0.0.1:8000/api/',
      nodeEnv:        process.env.NUXT_PUBLIC_NODE_ENV     || 'dev',
      host:           process.env.NUXT_PUBLIC_HOST         || 'http://localhost:3000/',
      apiAddress:     process.env.NUXT_PUBLIC_API_ADDRESS  || '',
      googleClientId: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID || '',
    },
  },

  modules: [
    '@nuxt/icon',
    'nuxt-toastify',
    "@pinia/nuxt",
  ],



  // Fix: "Failed to stringify dev server logs — Cannot stringify a function"
  // Pinia setup stores return functions alongside state; devalue (Nuxt's
  // serialiser) cannot serialise functions and emits this warning during HMR.
  // renderJsonPayloads serialises only plain-data payloads and skips
  // functions, eliminating the warning without requiring store refactoring.
  experimental: {
    renderJsonPayloads: true,
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
