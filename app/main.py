from fastapi import FastAPI
from app.config import settings
from app.api.analysis import router as api_router
from .database import engine
from app import models


app = FastAPI(title=settings.app_name, version=settings.app_version)
models.Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
