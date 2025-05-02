from fastapi import FastAPI

from webhook.api.routes import router
from webhook.core.config import settings

app = FastAPI(title=settings.TITLE)

app.include_router(router, prefix=settings.API_V1_PREFIX)
