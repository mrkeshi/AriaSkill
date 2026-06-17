# AriaSkill

A full-stack project showcase platform where developers can publish, share, and discover software projects. Built with a Django REST API backend and a Nuxt 4 frontend.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Backend — BackCode](#backend--backcode)
  - [Apps Overview](#apps-overview)
  - [Key Features](#key-features)
  - [Setup & Run](#setup--run)
  - [Environment Variables](#environment-variables)
  - [API Documentation](#api-documentation)
- [Frontend — FrontCode](#frontend--frontcode)
  - [Directory Overview](#directory-overview)
  - [Key Features](#key-features-1)
  - [Setup & Run](#setup--run-1)
- [Running Both Together](#running-both-together)

---

## Tech Stack

| Layer      | Technology                                                                              |
|------------|-----------------------------------------------------------------------------------------|
| Backend    | Python · Django 5 · Django REST Framework · SimpleJWT · drf-spectacular                |
| Frontend   | Nuxt 4 · Vue 3 · TypeScript · Pinia · ApexCharts · Tailwind CSS                        |
| Auth       | JWT (access + refresh tokens) · Google OAuth                                            |
| Database   | SQLite (development) — swappable to PostgreSQL for production                           |
| Media      | Django media serving (`/media/`) for avatars, project images & files                    |

---

## Project Structure

```
AriaSkill/
├── BackCode/               # Django backend
│   ├── accounts/           # User auth & profile
│   │   ├── models.py       # CustomUser model
│   │   ├── serializers.py  # Auth & profile serializers
│   │   ├── views.py        # Register, login, profile endpoints
│   │   ├── urls.py         # Account URL routes
│   │   └── services/       # Activation email, string helpers
│   ├── activity/           # Activity feed & event system
│   │   ├── models.py       # Activity, ProjectDownloadLog
│   │   ├── events.py       # Django Signal definitions
│   │   ├── listeners.py    # Signal receivers → ActivityService
│   │   ├── services.py     # ActivityService (create, feed, soft-delete ...)
│   │   ├── views.py        # Activity feed endpoints
│   │   └── urls.py
│   ├── notification/       # In-app notifications
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── projects/           # Core project domain
│   │   ├── models.py       # Project, Like, Comment, Skill
│   │   ├── views.py        # CRUD, likes, comments, downloads, dashboard chart & stats
│   │   ├── serializers.py
│   │   ├── admin_views.py  # Admin-specific project management
│   │   └── urls.py
│   ├── core/               # Shared utilities
│   │   ├── renderers.py    # Custom JSON renderer
│   │   ├── pagination.py   # Page-number pagination
│   │   ├── exceptions.py   # Global exception handler
│   │   └── schema.py       # OpenAPI helpers
│   ├── config/             # Django project config
│   │   ├── settings.py
│   │   ├── urls.py         # Root URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── manage.py
│
└── FrontCode/
    └── app/
        ├── components/     # Reusable Vue components
        │   ├── Dashboard/  # Chart, activity feed, sidebar, stats cards ...
        │   ├── Project/    # Project card, comment, download box ...
        │   ├── Header/     # Navbar, notification dropdown, profile dropdown
        │   ├── Auth/       # Google OAuth button
        │   └── Ui/         # Button, Input, Textarea, FileInput ...
        ├── pages/          # File-based routing (Nuxt)
        │   ├── index.vue
        │   ├── explore.vue
        │   ├── @[slug].vue            # Public user profile
        │   ├── projects/pr-[slug].vue # Project detail
        │   └── dashboard/             # Authenticated user area
        │       ├── index.vue
        │       ├── profile.vue
        │       ├── Projects/          # Add / edit own projects
        │       ├── activities/        # Activity log
        │       ├── comments/          # My comments
        │       ├── notifications/     # Notifications
        │       └── admin/             # Staff-only management pages
        ├── stores/         # Pinia state stores
        ├── services/       # API call functions (per domain)
        ├── models/         # TypeScript DTOs / interfaces
        ├── composable/     # Vue composables
        ├── utilities/      # fetchX, ApiConfig, dateHelpers, urlHelpers
        ├── validation/     # Form validation schemas
        ├── middleware/     # Route guards (auth, dashboard)
        └── plugins/        # Nuxt plugins (ApexCharts, auth init)
```

---

## Backend — BackCode

### Apps Overview

| App            | Responsibility                                                                                                        |
|----------------|-----------------------------------------------------------------------------------------------------------------------|
| `accounts`     | Custom user model (email-based auth), registration, login, Google OAuth, profile management, account activation emails |
| `projects`     | CRUD for projects, file uploads, likes, comments, download tracking, dashboard stats & chart                          |
| `activity`     | Event-driven activity log via Django Signals; soft-delete support; `ProjectDownloadLog` for persistent download stats  |
| `notification` | In-app notifications linked to user actions                                                                           |
| `core`         | Custom JSON renderer, pagination, global exception handler, OpenAPI schema helpers                                    |
| `config`       | Django settings, root URLs, WSGI/ASGI entry points                                                                    |

### Key Features

- **Custom user model** — email is the login identifier; supports avatar, job title, bio, and social links (Instagram, Telegram, Discord, LinkedIn) ...
- **JWT authentication** — access token (7 days) and refresh token (30 days) via SimpleJWT with automatic blacklisting on rotation ...
- **Google OAuth** — one-click social login with `GOOGLE_CLIENT_ID` ...
- **Project lifecycle** — projects go through a `pending → approved → rejected` admin moderation workflow ...
- **Event-driven activity system** — Django `Signal`s defined in `activity/events.py`; receivers in `activity/listeners.py` call `ActivityService` to persist records; all activities support soft-delete ...
- **Persistent download log** — `ProjectDownloadLog` stores every download independently of the activity feed, so deleting an activity record never affects the download count shown in the dashboard chart ...
- **Dashboard chart** — `GET /api/project/dashboard/chart/` returns up to 20 days of daily download and view data; downloads are read from `ProjectDownloadLog`, not `Activity` ...
- **Admin panel** — Django admin for managing users, projects, comments, and skills with custom admin views ...
- **OpenAPI docs** — auto-generated Swagger UI at `/api/swagger/` and ReDoc at `/api/redoc/` ...

### Setup & Run

#### Prerequisites

- Python 3.11+

#### Steps

```bash
# 1. Navigate to the backend folder
cd BackCode

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file (see Environment Variables section)

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 7. Start the Django development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables

Create a `.env` file inside `BackCode/`:

```env
SECRET_KEY=your-very-strong-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GOOGLE_CLIENT_ID=your-google-client-id
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
# Frontend
FRONTEND_URL=http://localhost:3000
```

### API Documentation

| URL              | Description        |
|------------------|--------------------|
| `/api/swagger/`  | Swagger UI         |
| `/api/redoc/`    | ReDoc UI           |
| `/api/schema/`   | Raw OpenAPI JSON   |
| `/admin/`        | Django admin panel |

#### Main API Prefixes

| Prefix                | App           |
|-----------------------|---------------|
| `/api/account/`       | Auth & users  |
| `/api/project/`       | Projects      |
| `/api/activities/`    | Activity feed |
| `/api/notifications/` | Notifications |

---

## Frontend — FrontCode

### Directory Overview

```
FrontCode/app/
├── components/
│   ├── Dashboard/
│   │   ├── DownloadChartVisitProject.vue   # ApexCharts download/view chart
│   │   ├── RecentActive.vue                # Recent activity feed
│   │   ├── DataCard.vue                    # Stats summary cards
│   │   ├── NotifBox.vue                    # Notification panel
│   │   └── Sidebar.vue                     # Dashboard sidebar nav
│   ├── Project/                            # Project card, comments, download box
│   ├── Header/                             # Navbar, notification dropdown, profile dropdown
│   ├── Auth/                               # Google OAuth button
│   └── Ui/                                 # Generic UI components (Button, Input, etc.)
│
├── pages/
│   ├── index.vue                           # Landing page
│   ├── explore.vue                         # Browse all projects
│   ├── projects/filter.vue                 # Filtered project list
│   ├── @[slug].vue                         # Public user profile
│   ├── projects/pr-[slug].vue              # Single project detail
│   └── dashboard/
│       ├── index.vue                       # Dashboard home
│       ├── profile.vue                     # Edit profile
│       ├── Projects/                       # Manage own projects
│       ├── activities/                     # Activity log
│       ├── comments/                       # User comments
│       ├── notifications/                  # Notifications
│       └── admin/                          # Admin-only pages (users, projects, comments, skills)
│
├── services/
│   ├── projects/
│   │   ├── project.Service.ts              # Project CRUD, likes, downloads
│   │   └── chart.Service.ts               # Dashboard chart API call
│   ├── activity/activity.Service.ts        # Fetch & delete activities
│   ├── notification/notification.Service.ts
│   ├── user/user.Service.ts                # Login, register, profile
│   └── skills/skills.Service.ts
│
├── stores/
│   └── authStore.ts                        # Pinia store: auth state, tokens, user info
│
├── utilities/
│   ├── fetchX.ts                           # $fetch wrapper with JWT injection & auto token refresh
│   ├── ApiConfig.ts                        # Base API URL config
│   ├── dateHelpers.ts                      # Jalali / Gregorian date utilities
│   └── urlHelpers.ts
│
└── middleware/
    └── dashboardGard.global.ts             # Redirects unauthenticated users away from /dashboard
```

### Key Features

- **File-based routing** via Nuxt 4 pages directory ...
- **Pinia auth store** — manages access/refresh tokens in cookies; handles silent token refresh on 401 ...
- **`FetchX` utility** — wraps Nuxt's `$fetch` with automatic `Authorization: JWT ...` header injection and transparent refresh on expiry ...
- **ApexCharts** — interactive download & view chart on the dashboard (`DownloadChartVisitProject.vue`) ...
- **Admin section** — separate dashboard pages for managing users, projects, comments, and skills (visible only to `is_staff` / `is_superuser`) ...
- **Google OAuth** — `GoogleButton.vue` handles the Google Identity flow end-to-end ...
- **Responsive components** — built with Tailwind CSS utility classes ...
- **Skeleton loaders** — `Skeleton/Simple.vue` provides loading placeholders while data is being fetched ...

### Setup & Run

#### Prerequisites

- Node.js 18+
- `npm` or `pnpm`

#### Steps

```bash
# 1. Navigate to the frontend folder
cd FrontCode

# 2. Install dependencies
npm install
# or
pnpm install

# 3. Create a .env file (see Environment Variables below)

# 4. Start the development server
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`.

### Environment Variables

Create a `.env` file at the root of `FrontCode/`:

```env
NUXT_PUBLIC_BASE_URL="http://127.0.0.1:8000/api/"
NUXT_PUBLIC_NODE_ENV=dev
NUXT_PUBLIC_HOST="http://localhost:3000/"
NUXT_PUBLIC_API_ADDRESS=""
NUXT_PUBLIC_GOOGLE_CLIENT_ID=1071435067795-ihtdo28q33m9614s4kkequ7mdvhc8in1.apps.googleusercontent.com
NUXT_PRIVATE_HEADER_KEY=django-insecure-lcit#6($l$@ej3=%jhrd75!ne6io&g=hw5lpatk_q66@^p-ijy
NUXT_TEST=""
```

### `nuxt.config.ts`

```ts
import tailwindcss from "@tailwindcss/vite";
import Icons from 'unplugin-icons/vite'

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
```

---

## Running Both Together

Open **two** terminals for the full stack:

**Terminal 1 — Django**
```bash
cd BackCode
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 — Frontend**
```bash
cd FrontCode
npm run dev
```

Then open `http://localhost:3000` in your browser. The frontend calls the API at `http://127.0.0.1:8000/api/`.

CORS is already configured in Django to allow `http://localhost:3000` and `http://127.0.0.1:3000`.
