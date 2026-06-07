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
   
   modules: ['@nuxt/icon',
     'nuxt-toastify',
     "@pinia/nuxt"
   ],




   vite: {
     plugins: [tailwindcss()],
   },



 });
