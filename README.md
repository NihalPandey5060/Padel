# Padel Discovery AI

Padel Discovery AI is a full-stack MVP for finding padel courts, coaches, and tournaments. It combines a Next.js frontend, a Django REST backend, PostgreSQL, and optional Gemini-powered natural language search.

## Tech stack

- Backend: Python 3.12+, Django 5.x, Django REST Framework, SimpleJWT
- Frontend: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS
- Database: PostgreSQL 16 (dev fallback: SQLite)
- Deployment: Static export for frontend (preferred) or Docker for full SSR; backend as Docker web service or any WSGI host
- AI: Google Gemini (optional, backend-only)

## What it does

- Browse courts, coaches, and tournaments.
- Search using plain language like “indoor courts near me” or “coaches with beginner lessons”.
- Open detail pages for each listing.
- Use Django Admin to manage records.

## How it works

1. The user opens the Next.js frontend.
2. The frontend calls the Django API for courts, coaches, tournaments, and search results.
3. When a user types a natural-language search, the backend extracts filters.
4. If `GEMINI_API_KEY` is set, Gemini helps interpret the query.
5. If Gemini is unavailable, the backend falls back to built-in heuristic parsing.
6. The backend queries PostgreSQL and returns paginated results.
7. The frontend renders the matching cards and detail pages.

## Architecture

```mermaid
flowchart LR
	user[User Browser] --> fe[Next.js Frontend]
	fe -->|REST API| be[Django REST API]
	be --> db[(PostgreSQL 16)]
	be --> gemini[Google Gemini API]
```

Only the backend talks to the database and Gemini. The frontend only talks to the backend.

## Run

```bash
docker compose up --build
```



## Environment

Copy `.env.example` to `.env` and set:

- `DJANGO_SECRET_KEY` for Django
- `GEMINI_API_KEY` to enable AI search parsing

The app still runs without Gemini; it just uses local parsing rules.

## Seed data

Sample courts, coaches, and tournaments are seeded automatically when the backend starts. You can also run:

```bash
python manage.py seed_data
```

## Docs

- [Setup guide](docs/setup-guide.md)
- [API documentation](docs/api-documentation.md)
- [Security review](docs/security-review.md)
- [Dependency compatibility report](docs/dependency-compatibility-report.md)
- [Architecture diagram](docs/architecture.md)
- [Test instructions](docs/setup-guide.md#testing)

---

**This README — Full Project Guide**

What follows expands the quick start above to cover everything you need for development, deployment, and maintenance: local dev, Docker Compose, Render (static frontend + backend), environment variables, database guidance, API reference, tests, and troubleshooting.

## Quick Local Development

1. Create a local environment file:

```bash
cp .env.example .env
# Edit .env and set DJANGO_SECRET_KEY
```

2. Backend (Python):

```bash
cd backend
python -m pip install -r requirements.lock
python manage.py migrate
python manage.py seed_data   # optional: seeds demo data
python manage.py runserver
```

3. Frontend (Next.js):

```bash
cd frontend
npm ci
npm run dev
# Open http://localhost:3000
```

Notes:
- Backend falls back to SQLite when `DATABASE_URL` is not set.
- Frontend reads `NEXT_PUBLIC_API_BASE_URL` (build-time) or `API_INTERNAL_URL` (server-side) to call the backend.

## Docker & Docker Compose (local / production-like)

- `docker-compose.yml` defines three services: `db` (Postgres), `backend` (Django), `frontend` (Next). To run them locally:

```bash
docker compose up --build
```

- The backend Dockerfile runs migrations and seeds data on startup. Change that behavior if you need a different migration strategy in production.

## Deploying the Frontend as a Static Site (Render)

If you choose to deploy a static export (recommended when you must avoid server runtime):

- Build command on Render (Static Site):

```
npm ci && npm run build && npx next export
```

- Publish directory: `out`
- Build environment variable (set in Render Build settings):
	- `NEXT_PUBLIC_API_BASE_URL=https://<your-backend>.onrender.com`

After deployment, the static site will call the backend URL baked at build time.

Limitations: `next export` only works for fully static pages. Server-rendered pages, API routes, or server components will not work as expected.

### Render Static Site — Exact Settings

- Service type: Static Site
- Root directory: `frontend`
- Build command: `npm ci && npm run build && npx next export`
- Publish directory: `out`
- Build environment variables (Render > Build settings):
	- `NEXT_PUBLIC_API_BASE_URL=https://<your-backend>.onrender.com`
- Runtime env: not required for static sites (the API base is baked at build time)

Local preview of the exported site:

```bash
cd frontend
npm ci
npm run build
npx next export
npx serve out -l 3000
# open http://localhost:3000
```

## Deploying Backend on Render (Web Service)

- Service type: Web Service
- Environment: Docker (recommended) or Dockerfile path `backend/Dockerfile`
- Health check path: `/api/courts/` or `/api/schema/`
- Env vars (set these in Render): see the Environment Variables section below

If you use Docker, the container will run migrations and seed data on start (as the Dockerfile is currently configured).

## Environment Variables (full list)

Set these for the Backend service (Render environment):

- `DATABASE_URL` — postgresql://user:pass@host:port/dbname (use the **Internal** URL on Render)
- `DJANGO_SECRET_KEY` — long random secret
- `DJANGO_DEBUG` — `false` in production
- `DJANGO_ALLOWED_HOSTS` — comma-separated hosts (e.g., `localhost,127.0.0.1,<your-backend>.onrender.com`)
- `CORS_ALLOWED_ORIGINS` — comma-separated origins allowed by CORS (e.g., `https://<your-frontend>.onrender.com`)
- `CSRF_TRUSTED_ORIGINS` — comma-separated CSRF origins (same as above)
- `GEMINI_API_KEY` — optional, enables Google Gemini-based parsing
- `GEMINI_MODEL` — optional, default `gemini-1.5-flash`

Frontend build/runtime (Static Site):

- `NEXT_PUBLIC_API_BASE_URL` — full URL to backend (used by client code at build-time)
- `API_INTERNAL_URL` — optional server-side URL resolution (server-rendered pages prefer this)

Local `.env` example (copy `.env.example`):

```
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=1
GEMINI_API_KEY=
DATABASE_URL=postgresql://padel:padel@localhost:5432/padel_discovery
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Database: Render Postgres guidance

- Create a PostgreSQL instance on Render.
- Use the **Internal Database URL** for `DATABASE_URL` on the backend service.
- The app supports `postgres://` and automatically rewrites it to `postgresql://` in `settings.py`.

## API Reference (important endpoints)

- `GET /api/courts/` — paginated list of courts
- `GET /api/coaches/` — paginated list of coaches
- `GET /api/tournaments/` — paginated list of tournaments
- `GET /api/courts/{id}/`, `GET /api/coaches/{id}/`, `GET /api/tournaments/{id}/` — detail objects
- `POST /api/search/` — body: `{ query: string, filters?: object, page?: number, page_size?: number }` — returns combined paginated search results and filter summary
- `POST /api/auth/login/` — admin login (sets HttpOnly JWT cookie)
- `POST /api/auth/refresh/` — refresh token endpoint

The backend exposes an OpenAPI schema at `/api/schema/` (useful for automated clients).

## Admin

- Create a Django superuser after database migrations have run:

```bash
python manage.py createsuperuser
```

Visit `/admin/` to manage courts/coaches/tournaments.

## Tests & Quality

- Backend tests (pytest):

```bash
cd backend
pytest
```

- Frontend checks:

```bash
cd frontend
npm run typecheck
npm run build
```

## Troubleshooting

- Frontend build errors about TypeScript deprecations: adjust `frontend/tsconfig.json` `ignoreDeprecations` to a compatible value for your TypeScript/Next version (we set a compatible value already).
- CORS/CSRF errors: ensure `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` match your frontend origin (including https://).
- Database connection errors on Render: ensure the backend `DATABASE_URL` is set to the Internal DB URL and backend service is in the same region.

## Security notes

- Keep `DJANGO_SECRET_KEY` and `GEMINI_API_KEY` secret — store them only in Render environment variables or a secure vault.
- The backend enforces that Gemini is used for filter extraction only (no direct DB access via the model), and the frontend never receives API keys.

## Optional: `render.yaml` (one-click)

I can add a `render.yaml` with static site + backend definitions, and placeholders for env vars; tell me if you want that and I will create and push it.

---

If you want, I will now:
- add an `export` npm script to `frontend/package.json` and commit it so static builds are simpler, and/or
- create a `render.yaml` you can use to create services on Render automatically.
Which would you like me to do next?
