# Payment API

FastAPI backend for the Payflow payment system.

The API manages payments, wallets, payment gateways, Mollie webhooks, and background jobs. It uses MariaDB for persistence, Redis for the queue, Celery for asynchronous work, and Alembic for database migrations.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- Poetry
- MariaDB
- Redis
- Celery
- Gunicorn with Uvicorn workers
- Pytest
- Ruff

## Project Structure

```text
backend/
  app/
    api/
    events/
    jobs/
    listeners/
    models/
    payments/
    repositories/
    services/
    main.py
    config.py
    db.py
  alembic/
  seeders/
  tests/
  Dockerfile
  pyproject.toml
```

## Environment Variables

Copy the example file and adjust values for your environment:

```bash
cp .env.example .env
```

Important settings:

```env
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=payment
DB_USERNAME=laravel
DB_PASSWORD=secret

REDIS_HOST=localhost
REDIS_PORT=6379
CELERY_BROKER_URL=redis://localhost:6379/0

MOLLIE_API_KEY=your_api_secret_here
MOLLIE_WEBHOOK_SECRET=your_webhook_secret_here

MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=test@gmail.com
MAIL_PASSWORD=password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=test@gmail.com
MAIL_FROM_NAME=Python FastAPI Payflow
```

For Docker Compose, service names are used as hosts, for example `DB_HOST=mysql`, `REDIS_HOST=redis`, and `CELERY_BROKER_URL=redis://redis:6379/0`.

Docker Compose passes `backend/.env` to the backend and worker containers at runtime. The file is excluded from Docker image build contexts so local secrets are not copied into images.

## Run with Docker

From the project root:

```bash
docker compose up --build
```

The stack starts:

- MariaDB
- Redis
- FastAPI backend
- Celery worker
- Nginx frontend

Open the frontend:

```text
http://localhost
```

API routes are available through the frontend Nginx proxy under `/api`.

Backend API documentation is available through the same proxy:

```text
http://localhost/api/docs
http://localhost/api/redoc
```

## Local Development

Install dependencies:

```bash
poetry install
```

Start the API:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the API docs:

```text
http://localhost:8000/api/docs
http://localhost:8000/api/redoc
```

## Database Migrations

Run migrations locally:

```bash
poetry run alembic upgrade head
```

Run migrations inside Docker:

```bash
docker compose exec backend poetry run alembic upgrade head
```

## Seed Data

Run seeders locally:

```bash
poetry run python seeders/seed.py
```

Run seeders inside Docker:

```bash
docker compose exec backend poetry run python seeders/seed.py
```

## Celery Worker

Run a worker locally:

```bash
poetry run celery -A app.jobs.payment_job worker --loglevel=info
```

The Docker Compose stack starts the worker service automatically.

## Test

```bash
poetry run pytest
```

## Lint and Format

Check code with Ruff:

```bash
poetry run ruff check .
```

Format code with Ruff:

```bash
poetry run ruff format .
```

## API Endpoints

- `GET /api/health`
- `GET /api/gateways`
- `GET /api/wallets/{user_id}`
- `POST /api/payments`
- `GET /api/payments/{payment_id}`
- `POST /api/webhooks/mollie`

## Notes

- Payment creation accepts form data.
- `idempotency_key` is used to avoid duplicate payment creation.
- Successful payments trigger wallet reconciliation.
- Mollie webhook handling updates payment status.
- Background jobs require Redis and Celery.
- Do not commit real API keys, mail credentials, or webhook secrets.

## Author

Mohammad Habibi
[parsit.nl](http://www.parsit.nl)
