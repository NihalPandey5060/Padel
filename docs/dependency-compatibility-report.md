# Dependency Compatibility Report

## Backend

- Django 5.1.6: stable on Python 3.12 and compatible with DRF 3.15.
- Django REST Framework 3.15.2: matches Django 5.x and provides routers, serializers, and schema support.
- djangorestframework-simplejwt 5.4.0: compatible with DRF 3.15 and used for JWT login/refresh.
- django-cors-headers 4.7.0: works with Django 5.1 for browser-origin restrictions.
- psycopg[binary] 3.2.6: stable PostgreSQL 16 driver for Python 3.12.
- pytest 8.3.4 and pytest-django 4.10.0: compatible test stack for Django 5.x.
- ruff 0.9.4 and black 24.10.0: stable lint/format tools for Python 3.12.
- gunicorn 23.0.0 and whitenoise 6.9.0: production-grade ASGI/WSGI serving and static handling.

## Frontend

- Next.js 15.5.18: latest stable 15.x patch line and compatible with React 19.
- React 19.0.0 and react-dom 19.0.0: matched pair for Next.js 15.
- TypeScript 5.8.2: compatible with the Next.js 15 toolchain.
- Tailwind CSS 3.4.17: stable utility CSS release with PostCSS support.
- PostCSS 8.5.10 and Autoprefixer 10.4.21: compatible with Tailwind 3.4.
- lucide-react 0.479.0, clsx 2.1.1, tailwind-merge 3.0.2: lightweight UI helper packages with no framework overlap.

## Compatibility notes

- The frontend build and TypeScript check both passed locally.
- The backend Python sources compile cleanly.
- npm audit still reports a moderate PostCSS-related advisory in the Next.js dependency tree; the app remains pinned to the latest stable Next 15 release and builds successfully.
