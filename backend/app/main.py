# app/main.py

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.gateways import router as gateways_router
from app.api.payment import router as payment_router
from app.api.wallet import router as wallet_router
from app.api.mollie_webhook import router as mollie_router
from app.events import register_events
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Payment API with Python FastAPI",
    description="""
Payment management system with multiple PSPs.

**Features:**
- Create and view payments
- Receive webhooks and update payment status
- Manage user wallets
- Full operation logging

**Supported Payment Gateways:**
- iDEAL (default)
- Mollie
- ING
- ABN AMRO
""",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# register all routers
app.include_router(health_router, prefix="/api")
app.include_router(gateways_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(wallet_router, prefix="/api")
app.include_router(mollie_router, prefix="/api")

register_events()
