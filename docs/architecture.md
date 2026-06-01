# Architecture

```mermaid
flowchart LR
  user[User Browser] --> fe[Next.js Frontend]
  fe -->|REST API| be[Django REST API]
  be --> db[(PostgreSQL 16)]
  be --> gemini[Google Gemini API]

  subgraph Frontend Service
    fe
  end

  subgraph Backend Service
    be
  end

  subgraph Data Layer
    db
  end

  subgraph External Services
    gemini
  end
```

Key points:

- Frontend and backend are separate Docker services.
- The frontend only talks to the backend through REST.
- The backend is the only service with database and Gemini access.
- Admin record management is handled through Django Admin.
