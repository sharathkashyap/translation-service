from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import logging.config
import os
from datetime import datetime

from src.core.config import get_settings
from src.translation.router import router as translation_router
from src.core.exceptions import TranslationException

# Setup logging
if os.path.exists("logging.ini"):
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Translation engine: {settings.TRANSLATION_ENGINE}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    description="Professional translation service with Google, OpenAI, and local GPU support",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler
@app.exception_handler(TranslationException)
async def translation_exception_handler(request, exc: TranslationException):
    return {
        "error": exc.__class__.__name__,
        "message": exc.message,
        "timestamp": datetime.utcnow().isoformat()
    }


# Health check
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "translation_engine": settings.TRANSLATION_ENGINE,
        "timestamp": datetime.utcnow().isoformat()
    }


# Include routers
app.include_router(translation_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "current_engine": settings.TRANSLATION_ENGINE,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )
