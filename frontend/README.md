# Payment UI

React, Vite, and TypeScript frontend for the Payflow payment system.

The app lets a user choose a payment gateway, create a payment, check payment status, and view a wallet balance. It talks to the FastAPI backend through the `VITE_API_BASE_URL` environment variable.

## Tech Stack

- React 19
- Vite
- TypeScript
- React Router
- Tailwind CSS
- Vitest
- Testing Library

## Project Structure

```text
frontend/
  public/
  src/
    App.tsx
    StatusPage.tsx
    api.ts
    main.tsx
    test/
  index.html
  package.json
  vite.config.ts
  tsconfig.json
```

## Requirements

- Node.js 20 or newer
- npm
- Running Payflow backend API

## Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Default local value:

```env
VITE_API_BASE_URL=http://localhost:8000
```

When running the full stack with Docker Compose from the project root, this variable can be omitted. The frontend falls back to relative URLs, and Nginx proxies API calls through `/api`.

## Install

```bash
npm install
```

## Run Locally

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

Make sure the backend is also running at the URL configured in `.env`.

## Build

Create a production build:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

The build output is written to:

```text
dist/
```

## Test

Run the test suite:

```bash
npm test
```

Run tests with coverage:

```bash
npm test -- --coverage
```

## Lint

```bash
npm run lint
```

## API Calls

The frontend API client lives in `src/api.ts` and uses these backend endpoints:

- `GET /api/health`
- `GET /api/gateways`
- `GET /api/wallets/{user_id}`
- `POST /api/payments`
- `GET /api/payments/{payment_id}`

## Docker

The frontend Docker image is built from the project root by `docker-compose.yml`:

```bash
docker compose up --build
```

The production frontend is served at:

```text
http://localhost
```

## Author

Mohammad Habibi
[parsit.nl](http://www.parsit.nl)
