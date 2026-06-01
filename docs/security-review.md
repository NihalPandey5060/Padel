# Security Review

Implemented controls:

- ORM-only database access through Django and DRF; no raw SQL path exists in the app.
- Gemini is isolated to the backend service and only extracts filters, never SQL or code.
- Gemini input is constrained with a narrow prompt and output is validated with DRF serializers.
- Credentials and API keys are loaded from environment variables.
- JWTs are set in HttpOnly cookies instead of localStorage.
- CORS is restricted to the frontend origin.
- CSRF trust is limited to the frontend origin.
- Search input is validated before it reaches the database layer.
- Django Admin is the only place for record management.

Residual notes:

- Public browsing endpoints are intentionally unauthenticated.
- The frontend uses backend-issued cookies for admin login flow.
- The project uses seeded demo data only; no sensitive user data is stored.
