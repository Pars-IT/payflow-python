from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Gateway(BaseModel):
    key: str
    name: str
    default: bool


@router.get(
    "/gateways",
    response_model=List[Gateway],
    summary="List Payment Gateways",
    description="""
Returns a list of all available payment gateways that can be used for processing payments.

**Purpose:**
- Show which gateways are currently supported
- Indicate the default gateway
- Useful for frontend apps to populate payment options dynamically

**Response:**
- `key`: Unique identifier for the gateway
- `name`: Human-readable name of the gateway
- `default`: `true` if this is the default gateway
""",
)
def gateways():
    return [
        Gateway(key="ideal", name="iDEAL", default=True),
        Gateway(key="mollie", name="Mollie", default=False),
        Gateway(key="ing", name="ING", default=False),
        Gateway(key="abn-amro", name="ABN AMRO", default=False),
    ]
