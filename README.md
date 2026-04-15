# Payflow Python

Dockerized payment application with a React frontend, FastAPI backend, MariaDB database, Redis queue, and Celery worker.

Payflow lets a user select a payment gateway, create a payment, check payment status, receive Mollie webhooks, and keep wallet balances in sync through background jobs.

## Services

- `frontend`: React, Vite, TypeScript app served by Nginx
- `backend`: FastAPI API served by Gunicorn and Uvicorn workers
- `worker`: Celery worker for payment background jobs
- `mysql`: MariaDB database
- `redis`: Redis queue backend

## Project Structure

```text
payflow-python/
  backend/
    app/
    alembic/
    seeders/
    tests/
    Dockerfile
    README.md
  frontend/
    src/
    public/
    Dockerfile
    README.md
  docker/
    mysql/
    nginx/
  docker-compose.yml
  docker-compose-aws.yml
  .env.example
```

## Requirements

- Docker
- Docker Compose

For local development without Docker, see:

- `backend/README.md`
- `frontend/README.md`

## Environment Files

The Docker stack uses environment files in two places.

Root `.env` is used by the MariaDB container:

```bash
cp .env.example .env
```

Example root values:

```env
MYSQL_DATABASE=payment
MYSQL_USER=laravel
MYSQL_PASSWORD=secret
MYSQL_ROOT_PASSWORD=root
```

Backend settings live in `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

For Docker Compose, backend service hosts should use container names:

```env
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=payment
DB_USERNAME=laravel
DB_PASSWORD=secret

REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
```

Docker Compose passes this file to the backend and worker containers at runtime. It is intentionally excluded from Docker build contexts so secrets are not baked into images.

Frontend settings live in `frontend/.env`:

```bash
cp frontend/.env.example frontend/.env
```

For local frontend development:

```env
VITE_API_BASE_URL=http://localhost:8000
```

In the Dockerized production frontend, this variable can be omitted. The app falls back to relative URLs, and Nginx proxies `/api` to the backend service.

## Run the Full Stack

Build and start all services:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

Stop the stack:

```bash
docker compose down
```

Stop the stack and remove database volume data:

```bash
docker compose down -v
```

## URLs

Frontend:

```text
http://localhost
```

Backend API through Nginx:

```text
http://localhost/api
```

Swagger UI:

```text
http://localhost/api/docs
```

ReDoc:

```text
http://localhost/api/redoc
```

Health check:

```text
http://localhost/api/health
```

When running the backend directly outside Docker, API docs are available at:

```text
http://localhost:8000/api/docs
http://localhost:8000/api/redoc
```

## Database Setup

Run Alembic migrations after the containers are up:

```bash
docker compose exec backend poetry run alembic upgrade head
```

Seed initial data:

```bash
docker compose exec backend poetry run python seeders/seed.py
```

## Useful Docker Commands

View service status:

```bash
docker compose ps
```

Follow all logs:

```bash
docker compose logs -f
```

Follow backend logs:

```bash
docker compose logs -f backend
```

Follow worker logs:

```bash
docker compose logs -f worker
```

Open a shell in the backend container:

```bash
docker compose exec backend bash
```

## API Endpoints

- `GET /api/health`
- `GET /api/gateways`
- `GET /api/wallets/{user_id}`
- `POST /api/payments`
- `GET /api/payments/{payment_id}`
- `POST /api/webhooks/mollie`

## Testing

Run backend tests:

```bash
docker compose exec backend poetry run pytest
```

Run frontend tests locally from `frontend/`:

```bash
npm test
```

## Production Notes

- Replace all example secrets before deploying.
- Do not commit real Mollie keys, SMTP passwords, or webhook secrets.
- `docker-compose-aws.yml` is provided for an AWS-style deployment where internal database and Redis ports are not published.
- The frontend container serves static files with Nginx and proxies `/api` requests to the backend container.
- The Celery worker must stay running for background payment jobs.

## Author

Mohammad Habibi
[parsit.nl](http://www.parsit.nl)
