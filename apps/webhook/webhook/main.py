import logging

from fastapi import FastAPI
from utils.logging import setup_logger

from webhook.api.routes import router
from webhook.core.config import settings

setup_logger("webhook.log", level=logging.DEBUG)

app = FastAPI(title=settings.TITLE)

app.include_router(router, prefix=settings.API_V1_PREFIX)
