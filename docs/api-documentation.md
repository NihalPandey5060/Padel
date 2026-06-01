# API Documentation

OpenAPI is exposed by Django REST Framework at:

- `/api/schema/`

## Endpoints

- `GET /api/courts/`
- `GET /api/courts/{id}/`
- `GET /api/coaches/`
- `GET /api/coaches/{id}/`
- `GET /api/tournaments/`
- `GET /api/tournaments/{id}/`
- `POST /api/search/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

## Search payload

```json
{
  "query": "Beginner padel courts in Bangalore under ₹800",
  "filters": {
    "city": "Bangalore",
    "max_price": 800,
    "category": "courts"
  },
  "page": 1,
  "page_size": 8
}
```

## Search response

The response returns a paginated combined results list. Each result includes a `type` field so the frontend can render courts, coaches, and tournaments in one stream.
