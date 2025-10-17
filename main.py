from fastapi import FastAPI

from app.api.v1 import branding
from app.core.config import config
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(branding.router, prefix="/api/v1")
