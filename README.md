# Django E-commerce Demo

A Django-based e-commerce application with product browsing, search, category filtering, sorting, pagination, product detail pages, and cart-related functionality.

## Stack

- Python / Django
- PostgreSQL
- Redis (configured in Docker Compose)
- Docker Compose for local services

## Run locally with Docker Compose

1. Install Docker Desktop / Docker Compose.
2. Copy the example environment file and replace the placeholders with local-only values:

   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   # macOS/Linux
   cp .env.example .env
   ```

3. Generate a fresh Django secret key. One option is:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Put the generated value into `.env` as `DJANGO_SECRET_KEY`. Set `DB_PASSWORD` to a local PostgreSQL password. Do not commit `.env`.

4. Start the services:

   ```bash
   docker compose up --build
   ```

5. In another terminal, apply database migrations:

   ```bash
   docker compose exec web python manage.py migrate
   ```

6. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Environment variables

See `.env.example` for the required variables. Docker Compose uses the `db` service as the database host. The default Compose configuration is intended for local development, not production deployment.

## Security notes

- Use a unique secret key and database password in your local `.env`.
- Keep `DJANGO_DEBUG=true` only for local development. Set it to `false` in deployed environments and configure `DJANGO_ALLOWED_HOSTS`.
- The app has not been represented here as production-hardened; review Django's deployment checklist, authentication/cart flows, and automated tests before deployment.
