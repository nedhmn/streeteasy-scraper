import logging
from typing import Any

from db.models import Address
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from webhook.api.deps import DbSessionDep
from webhook.core.models import HealthCheckResponse, WebhookPayload

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health-check",
    response_model=HealthCheckResponse,
    description="Health check",
    tags=["utils"],
)
async def get_health_check() -> Any:
    return {"status": "ok"}


@router.post(
    "/brightdata-webhook",
    description="Webhook that processes job response payloads from BrightData.",
    tags=["bright-data"],
)
async def brightdata_webhook(db_session: DbSessionDep, payload: WebhookPayload) -> None:
    logger.debug("Paylod received: %s", payload)

    job_status_code = payload.status
    job_response_id = payload.response_id

    # Get job by response_id
    result = await db_session.execute(
        select(Address).where(Address.brightdata_response_id == job_response_id)
    )
    address = result.scalar_one_or_none()

    if not address:
        raise HTTPException(status_code=404, detail="Address not found.")

    # Update job status and commit changes
    address.status = "ready_to_process" if job_status_code == 200 else "failed"
    await db_session.commit()
