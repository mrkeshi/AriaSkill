# AriaSkill

A full-stack project showcase platform where developers can publish, share, and discover software projects. Built with a Django REST API backend and a Nuxt 4 frontend.

---

## Quick Setup (3 Minutes)

### Backend

cd BackCode
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

Backend runs at:
http://127.0.0.1:8000/

---

### Frontend

cd FrontCode
npm install
npm run dev

Frontend runs at:
http://localhost:3000/

---

## Tech Stack

Backend: Python, Django 5, DRF, SimpleJWT, drf-spectacular  
Frontend: Nuxt 4, Vue 3, TypeScript, Pinia, Tailwind CSS  
Auth: JWT + Google OAuth  
Database: SQLite (dev)  
Media: Django media handling

---

## Environment Variables

### Django (.env)

SECRET_KEY=your-very-strong-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

GOOGLE_CLIENT_ID=your-google-client-id

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

FRONTEND_URL=http://localhost:3000


### Nuxt (.env)

NUXT_PUBLIC_BASE_URL="http://127.0.0.1:8000/api/"
NUXT_PUBLIC_NODE_ENV=dev
NUXT_PUBLIC_HOST="http://localhost:3000/"
NUXT_PUBLIC_API_ADDRESS=""
NUXT_PUBLIC_GOOGLE_CLIENT_ID=1071435067795-ihtdo28q33m9614s4kkequ7mdvhc8in1.apps.googleusercontent.com

NUXT_PRIVATE_HEADER_KEY=django-insecure-lcit#6($l$@ej3=%jhrd75!ne6io&g=hw5lpatk_q66@^p-ijy
NUXT_TEST=""

---

## nuxt.config.ts (Fixed)

import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  css: ["@/assets/css/main.css"],

  runtimeConfig: {
    privateHeaderKey: process.env.NUXT_PRIVATE_HEADER_KEY || '',
    public: {
      baseUrl: process.env.NUXT_PUBLIC_BASE_URL || 'http://127.0.0.1:8000/api/',
      nodeEnv: process.env.NUXT_PUBLIC_NODE_ENV || 'dev',
      host: process.env.NUXT_PUBLIC_HOST || 'http://localhost:3000/',
      apiAddress: process.env.NUXT_PUBLIC_API_ADDRESS || '',
      googleClientId: process.env.NUXT_PUBLIC_GOOGLE_CLIENT_ID || '',
    },
  },

  modules: [
    '@nuxt/icon',
    'nuxt-toastify',
    '@pinia/nuxt',
  ],

  experimental: {
    renderJsonPayloads: true,
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
