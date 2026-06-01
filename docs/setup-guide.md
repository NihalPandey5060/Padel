# Setup Guide

## Prerequisites

- Docker
- Docker Compose

## Start the app

```bash
docker compose up --build
```

The backend runs migrations and seeds sample data automatically on startup.

## Seed data manually

If you need to reseed the backend directly:

```bash
python manage.py seed_data
```

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run typecheck
npm run build
```

## Notes

- The database is only reachable from the backend container.
- Gemini API access stays in the backend service.
- JWTs are stored in HttpOnly cookies by the backend auth endpoints.
