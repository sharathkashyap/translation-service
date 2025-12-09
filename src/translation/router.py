from fastapi import APIRouter, HTTPException, status
from src.translation.service import TranslationService
from src.translation.schemas import (
    TranslateRequest,
    TranslateResponse,
    BatchTranslateRequest,
    BatchTranslateResponse,
    SupportedLanguagesResponse,
    EngineHealthResponse
)
from src.core.exceptions import TranslationException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/translate", tags=["translation"])


@router.post("/", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate text from source to target language
    
    **Parameters:**
    - **text**: Text to translate (max 5000 characters)
    - **source_language**: Source language code (e.g., 'en', 'es', 'fr')
    - **target_language**: Target language code (e.g., 'es', 'en', 'fr')
    """
    try:
        return await TranslationService.translate(request)
    except TranslationException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/batch", response_model=BatchTranslateResponse)
async def batch_translate(request: BatchTranslateRequest):
    """
    Batch translate multiple texts
    
    **Parameters:**
    - **texts**: List of texts to translate (1-100 items)
    - **source_language**: Source language code
    - **target_language**: Target language code
    """
    try:
        return await TranslationService.batch_translate(request)
    except TranslationException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """Get list of supported languages"""
    try:
        result = await TranslationService.get_supported_languages()
        return SupportedLanguagesResponse(
            languages=result["languages"],
            engine=result["engine"],
            total=result["total"]
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health", response_model=EngineHealthResponse)
async def health_check():
    """Check translation engine health"""
    try:
        result = await TranslationService.health_check()
        return EngineHealthResponse(
            healthy=result["healthy"],
            engine=result["engine"],
            timestamp=result["timestamp"],
            response_time_ms=result.get("response_time_ms", 0)
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Translation engine is unavailable"
        )
