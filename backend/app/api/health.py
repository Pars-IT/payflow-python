# app/api/health.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()


class HealthResponse(BaseModel):
    ok: bool
    timestamp: datetime


@router.get(
    "/health",
    summary="Check API Health",
    description="""
Returns the current health status of the API.

**Purpose:**
- Verify that the API server is running
- Confirm database connectivity (if applicable)
- Useful for uptime monitoring and load balancers

**Response:**
- `ok`: True if the service is healthy
- `timestamp`: Current UTC timestamp of the check
""",
    response_model=HealthResponse,
)
def health():
    return {"ok": True, "timestamp": datetime.now(timezone.utc)}
