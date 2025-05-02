from typing import Any

from fastapi import APIRouter

from webhook.core.models import HealthCheckResponse

router = APIRouter()


@router.get(
    "/health-check",
    response_model=HealthCheckResponse,
    description="Health check",
    tags=["utils"],
)
async def get_health_check() -> Any:
    return {"status": "ok"}
