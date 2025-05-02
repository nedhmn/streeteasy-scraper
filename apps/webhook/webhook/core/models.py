from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str


class WebhookPayload(BaseModel):
    status: int
    response_id: str
    request_url: str
