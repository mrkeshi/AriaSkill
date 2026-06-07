# AriaSkill

A full-stack project showcase platform where developers can publish, share, and discover software projects. Built with a Django REST API backend and a Nuxt 3 frontend.

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
- [Async Email with Celery & Redis](#async-email-with-celery--redis)
- [Running Both Together](#running-both-together)

---

## Tech Stack

| Layer      | Technology                                                                              |
|------------|-----------------------------------------------------------------------------------------|
| Backend    | Python · Django 5 · Django REST Framework · SimpleJWT · drf-spectacular                |
| Frontend   | Nuxt 3 · Vue 3 · TypeScript · Pinia · ApexCharts · Tailwind CSS                        |
| Auth       | JWT (access + refresh tokens) · Google OAuth                                            |
| Database   | SQLite (development) — swappable to PostgreSQL for production                           |
| Task Queue | Celery · Redis (async email delivery, background jobs)                                  |
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
│   │   ├── celery.py       # Celery app configuration
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
| `config`       | Django settings, root URLs, Celery app definition, WSGI/ASGI entry points                                             |

### Key Features

- **Custom user model** — email is the login identifier; supports avatar, job title, bio, and social links (Instagram, Telegram, Discord, LinkedIn) ...
- **JWT authentication** — access token (7 days) and refresh token (30 days) via SimpleJWT with automatic blacklisting on rotation ...
- **Google OAuth** — one-click social login with `GOOGLE_CLIENT_ID` ...
- **Project lifecycle** — projects go through a `pending → approved → rejected` admin moderation workflow ...
- **Event-driven activity system** — Django `Signal`s defined in `activity/events.py`; receivers in `activity/listeners.py` call `ActivityService` to persist records; all activities support soft-delete ...
- **Persistent download log** — `ProjectDownloadLog` stores every download independently of the activity feed, so deleting an activity record never affects the download count shown in the dashboard chart ...
- **Dashboard chart** — `GET /api/project/dashboard/chart/` returns up to 20 days of daily download and view data; downloads are read from `ProjectDownloadLog`, not `Activity` ...
- **Async email delivery** — account activation and password-reset emails are dispatched as Celery tasks through a Redis broker, keeping API responses fast ...
- **Admin panel** — Django admin for managing users, projects, comments, and skills with custom admin views ...
- **OpenAPI docs** — auto-generated Swagger UI at `/api/swagger/` and ReDoc at `/api/redoc/` ...

### Setup & Run

#### Prerequisites

- Python 3.11+
- Redis (running locally or via Docker)

#### Steps

```bash
# 1. Navigate to the backend folder
cd BackCode

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt \
    django-cors-headers drf-spectacular drf-spectacular-sidecar \
    Pillow python-dotenv celery redis django-celery-results

# 4. Create a .env file (see Environment Variables section)

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (optional, for admin access)
python manage.py createsuperuser

# 7. Start the Django development server
python manage.py runserver

# 8. In a separate terminal — start the Celery worker
celery -A config worker --loglevel=info
```

The API will be available at `http://127.0.0.1:8000/`.

### Environment Variables

Create a `.env` file inside `BackCode/`:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id-here

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery / Redis
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
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

- **File-based routing** via Nuxt 3 pages directory ...
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

# 3. Configure the API base URL
#    Edit app/utilities/ApiConfig.ts if your backend runs on a different port:
#    export const baseURL = "http://127.0.0.1:8000/api/"

# 4. Start the development server
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`.

Add a runtime config to `nuxt.config.ts` if not already present:

```ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      baseUrl: process.env.NUXT_PUBLIC_BASE_URL || 'http://127.0.0.1:8000/api/',
    },
  },
})
```

And a `.env` at the root of `FrontCode/`:

```env
NUXT_PUBLIC_BASE_URL=http://127.0.0.1:8000/api/
```

---

## Async Email with Celery & Redis

Account activation and password-reset emails are sent asynchronously so the API never blocks waiting for an SMTP response.

### How it works

```
User registers / resets password
        │
        ▼
Django view calls  send_activation_email.delay(user_id)
        │                   (Celery task)
        ▼
Task is pushed to ──► Redis (message broker)
        │
        ▼
Celery worker picks up the task
        │
        ▼
Worker renders email template + sends via SMTP
```

### Setup

**1. Install Redis**

```bash
# macOS
brew install redis && brew services start redis

# Ubuntu / Debian
sudo apt install redis-server && sudo systemctl start redis

# Docker (quickest)
docker run -d -p 6379:6379 redis:7-alpine
```

**2. Add Celery config to `config/settings.py`**

```python
CELERY_BROKER_URL      = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND  = os.environ.get('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT  = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

**3. Create `config/celery.py`**

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**4. Register Celery in `config/__init__.py`**

```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

**5. Define an email task (example in `accounts/tasks.py`)**

```python
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_email(user_id: int):
    from accounts.models import CustomUser
    user = CustomUser.objects.get(pk=user_id)
    send_mail(
        subject='Activate your AriaSkill account',
        message=f'Hi {user.username}, click the link to activate your account.',
        from_email='noreply@ariaskill.com',
        recipient_list=[user.email],
    )
```

**6. Start the Celery worker**

```bash
# from inside BackCode/ with the venv active
celery -A config worker --loglevel=info
```

> **Tip:** In production, run the worker as a system service (systemd / Supervisor) and point `CELERY_BROKER_URL` to your production Redis instance.

---

## Running Both Together

Open **four** terminals for the full stack:

**Terminal 1 — Redis**
```bash
redis-server
# or: docker run -d -p 6379:6379 redis:7-alpine
```

**Terminal 2 — Django**
```bash
cd BackCode
source venv/bin/activate
python manage.py runserver
```

**Terminal 3 — Celery Worker**
```bash
cd BackCode
source venv/bin/activate
celery -A config worker --loglevel=info
```

**Terminal 4 — Nuxt Frontend**
```bash
cd FrontCode
npm run dev
```

Then open `http://localhost:3000` in your browser. The frontend calls the API at `http://127.0.0.1:8000/api/`, and any email tasks are processed in the background by the Celery worker through Redis.

CORS is already configured in Django to allow `http://localhost:3000` and `http://127.0.0.1:3000`.
