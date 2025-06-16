import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI
from middleware import LogMiddleware, setup_cors
from routes.base import router
from config.app_cfg import AppConfig

app = FastAPI(
    title=AppConfig.APP_NAME,
    description=AppConfig.APP_DESCRIPTION,
    version=AppConfig.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(LogMiddleware)
setup_cors(app)
app.include_router(router)