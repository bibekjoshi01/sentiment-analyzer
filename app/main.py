from fastapi import FastAPI

from app.config import settings
from app.api.analysis import router as api_router
from app.middleware import AuthMiddleware
from .database import engine
from app import models
from .api.auth import router as auth_router


app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(AuthMiddleware)

models.Base.metadata.create_all(bind=engine)

app.include_router(api_router)
app.include_router(auth_router)


@app.get("/health", tags=["Site"])
async def health_check():
    return {"status": "ok"}
